"""Text rendering helpers: splitting an enriched commit into sections, and the
sliced-body renderer's handling of brace-less control flow."""
from crossslice.commit import split_sections
from crossslice.cross.enrich import CrossFunctionEnricher

SAMPLE = """Context for merged statement of old file: kv.c with new file: kv.c:
int kv_put(kv_store *s, const char *key, const char *value) {
+ size_t key_len = strlen(key);
}


==== Cross-function context ====

-- called function: find_slot — kv.c:18 [gtags_unique] --
int find_slot(const kv_store *s, const char *key) {
   return -1;
}
   [reads: key, s; writes: -]

-- called macro: KV_ERR_KEYLEN — kv.h:10 [gtags_unique, new version] --
#define KV_ERR_KEYLEN  -3

-- caller of kv_put: main — main.c:14 --
int main(void) {
>      if(kv_put(store, key, value)== KV_OK)printf("ok\\n");
}
-- 2nd-level context (summaries) --
  hash_key — kv.c:9 [gtags_unique]: unsigned long hash_key(const char *k)
"""


def test_split_sections():
    s = split_sections(SAMPLE)
    assert [x["kind"] for x in s] == ["change", "callee", "macro", "caller", "ring2"]
    assert s[0]["file"] == "kv.c" and s[0]["body"].startswith("int kv_put")
    assert s[1]["name"] == "find_slot" and s[1]["line"] == 18 and s[1]["method"] == "gtags_unique"
    assert s[1]["body"].endswith("[reads: key, s; writes: -]")
    assert s[2]["version"] == "new" and s[2]["name"] == "KV_ERR_KEYLEN"
    assert s[3]["of"] == "kv_put" and s[3]["name"] == "main" and s[3]["file"] == "main.c"
    assert "hash_key" in s[4]["body"]
    assert split_sections("") == []


def test_braceless_if_is_printed_once():
    stmts = [
        {"name": "int f(int a) {", "type": "function_definition"},
        {"type": "if_statement", "expression": "if(a > 0)return a;", "scope_depth": 1,
         "relevant_to_dataflow": True},
        {"type": "return_statement", "expression": "return a;", "scope_depth": 1,
         "relevant_to_dataflow": True},
        {"type": "return_statement", "expression": "return 0;", "scope_depth": 1,
         "relevant_to_dataflow": True},
    ]
    out = CrossFunctionEnricher._render_sliced(stmts).split("\n")
    assert out[1].strip() == "if(a > 0)"
    assert out[2].strip() == "return a;" and out[2].index("r") > out[1].index("i")
    assert out[3].strip() == "return 0;"
    assert sum("return a;" in line for line in out) == 1


def test_written_bases_heuristics():
    wb = CrossFunctionEnricher._written_bases
    assert wb("*out_value = NULL;") == {"out_value"}
    assert wb("*(p) += 2;") == {"p"}
    assert wb("s->count++;") == {"s"}
    assert wb("++s->count;") == {"s"}
    assert wb("(*p)++;") == {"p"}
    assert wb("s->entries[idx].value = NULL;") == {"s"}
    assert wb("buf[i++] = c;") == {"buf"}
    assert wb("memcpy(e->key, key, key_len + 1);") == {"e"}
    assert wb("n = read(fd, buf, sizeof buf);") == {"buf"}
    assert wb("snprintf((char *)out, n, \"%d\", v);") == {"out"}
    assert wb("parse(&x, y);") == {"x"}
    assert wb("if(2 *(s->count + 1)> s->cap)kv_grow(s);") == set()   # multiplication, not a deref write
    assert wb("x = a & b;") == set()
    assert wb("n = s->len;") == set()
    assert wb("if (*p == 3) return;") == set()
    assert wb("ok = s->entries[idx].in_use;") == set()


def test_modref_summary_aliases_and_pointer_types():
    stmts = [
        {"name": "int f(kv_store *s, int *out) {", "type": "function_definition",
         "parameters": [{"name": "s", "var_id": "S"}, {"name": "out", "var_id": "O"}]},
        {"type": "declaration", "expression": "kv_entry *e = &s->entries[0];",
         "left_side": [{"name": "e", "var_id": "E"}], "right_side": [{"name": "s", "var_id": "S"}]},
        {"type": "expression_statement", "expression": "e->in_use = 1;",
         "left_side": [], "right_side": [{"name": "e", "var_id": "E"}]},
        {"type": "expression_statement", "expression": "*out = e->in_use;",
         "left_side": [], "right_side": [{"name": "out", "var_id": "O"}, {"name": "e", "var_id": "E"}]},
        {"type": "return_statement", "expression": "return 0;", "left_side": [], "right_side": []},
    ]
    sm = CrossFunctionEnricher._modref_summary(stmts, {"S", "O"})
    assert sm["params_written"] == ["out*", "s*"] and sm["params_read"] == ["out", "s"]


def _if(cond, cons, alt, start, end, depth=1, alt_start=None):
    parts = [{"part_nname": "condition", "expression": cond},
             {"part_nname": "consequence", "expression": cons}]
    if alt is not None:
        parts.append({"part_nname": "alternative", "expression": alt, "start": alt_start})
    return {"type": "if_statement", "expression": f"if{cond}{cons} {alt or ''}".strip(), "parts": parts,
            "start": start, "end": end, "scope_depth": depth, "relevant_to_dataflow": True}


def _stmt(expr, start, depth):
    return {"type": "expression_statement", "expression": expr, "start": start,
            "end": [start[0], start[1] + len(expr)], "scope_depth": depth, "relevant_to_dataflow": True}


def test_else_headers_from_alternative_parts():
    render = CrossFunctionEnricher._render_sliced
    head = {"name": "void f(int a) {", "type": "function_definition"}
    # braced then and else
    out = render([head,
                  _if("(a)", "{ x(); }", "else { y(); }", [1, 4], [5, 5], alt_start=[3, 6]),
                  _stmt("x();", [2, 8], 2), _stmt("y();", [4, 8], 2)]).split("\n")
    assert out[1:5] == ["   if(a) {", "     x();", "   } else {", "     y();"]
    # brace-less then and else: no closing brace, bodies indented
    out = render([head,
                  _if("(a)", "x();", "else y();", [1, 4], [2, 13], alt_start=[2, 4]),
                  _stmt("x();", [1, 10], 1), _stmt("y();", [2, 9], 1)]).split("\n")
    assert out[1:5] == ["   if(a)", "     x();", "   else", "     y();"]
    # else-if chain: the chained if is a sibling starting at the alternative
    out = render([head,
                  _if("(a)", "{ x(); }", "else if(b) { y(); } else { z(); }", [1, 4], [7, 5], alt_start=[3, 6]),
                  _stmt("x();", [2, 8], 2),
                  _if("(b)", "{ y(); }", "else { z(); }", [3, 11], [7, 5], alt_start=[5, 6]),
                  _stmt("y();", [4, 8], 2), _stmt("z();", [6, 8], 2)]).split("\n")
    assert out[1:7] == ["   if(a) {", "     x();", "   } else if(b) {", "     y();", "   } else {", "     z();"]
    # an else branch with nothing relevant adds no header
    stmts = [head, _if("(a)", "{ x(); }", "else { y(); }", [1, 4], [5, 5], alt_start=[3, 6]),
             _stmt("x();", [2, 8], 2), dict(_stmt("y();", [4, 8], 2), relevant_to_dataflow=False)]
    assert "else" not in render(stmts)


def test_closing_braces_and_braceless_nesting():
    render = CrossFunctionEnricher._render_sliced
    head = {"name": "int f(kv_store *s) {", "type": "function_definition"}
    # a braced loop closes before the statement that follows it
    loop = {"type": "for_statement", "expression": "for(i = 0; i < n; i++){ x(); }", "start": [1, 4],
            "end": [3, 5], "scope_depth": 1, "relevant_to_dataflow": True}
    out = render([head, loop, _stmt("x();", [2, 8], 2), _stmt("return -1;", [4, 4], 1)]).split("\n")
    assert out[1:] == ["   for(i = 0; i < n; i++) {", "     x();", "   }", "   return -1;", "}"]
    # brace-less chain: for -> if -> body, each level indented one step further
    loop = {"type": "for_statement", "expression": "for(i = 0; i < n; i++)if(a)free(p);", "start": [1, 4],
            "end": [3, 15], "scope_depth": 1, "relevant_to_dataflow": True}
    out = render([head, loop, _if("(a)", "free(p);", None, [2, 8], [3, 15]),
                  _stmt("free(p);", [3, 12], 1), _stmt("free(s);", [4, 4], 1)]).split("\n")
    assert out[1:] == ["   for(i = 0; i < n; i++)", "     if(a)", "       free(p);", "   free(s);", "}"]
    # an else block is closed too, and `...` stays inside the block it belongs to
    out = render([head,
                  _if("(a)", "{ x(); }", "else { y(); z(); }", [1, 4], [6, 5], alt_start=[3, 6]),
                  _stmt("x();", [2, 8], 2), _stmt("y();", [4, 8], 2),
                  dict(_stmt("z();", [5, 8], 2), relevant_to_dataflow=False),
                  _stmt("w();", [7, 4], 1)]).split("\n")
    assert out[1:] == ["   if(a) {", "     x();", "   } else {", "     y();", "   ...", "   }", "   w();", "}"]
    # do { } while (c);
    do = {"type": "do_statement", "expression": "do{ x(); } while(c);", "start": [1, 4], "end": [3, 15],
          "scope_depth": 1, "relevant_to_dataflow": True}
    out = render([head, do, _stmt("x();", [2, 8], 2)]).split("\n")
    assert out[1:] == ["   do {", "     x();", "   } while(c);", "}"]


def test_definition_ranking_prefers_functions_and_real_code():
    from crossslice.cross.resolve import _definition_score as score
    fn = {"is_macro": False, "signature": "static inline unsigned int get_bits(GetBitContext *s, int n)"}
    alias = {"is_macro": True, "signature": "#define get_bits            bits_read_nz"}
    stub = {"is_macro": True, "signature": "#define av_log(a, ...) while(0)"}
    void0 = {"is_macro": True, "signature": "#define av_assert1(cond) ((void)0)"}
    real = {"is_macro": True, "signature": "#define FFMIN(a,b) ((a) > (b) ? (b) : (a))"}
    assert score(fn, "libavcodec/get_bits.h") > score(alias, "libavcodec/get_bits.h")
    assert score(real, "libavutil/common.h") > score(alias, "libavcodec/get_bits.h")
    assert score(real, "libavutil/common.h") > score(void0, "libavutil/avassert.h")
    assert score(fn, "libavutil/log.c") > score(stub, "libavcodec/tableprint_vlc.h")
    assert score(stub, "libavutil/x.h") < score(real, "libavutil/x.h")


def test_def_closure_and_endif():
    from crossslice.cross.context import _close_defs
    head = {"name": "int f(int k) {", "type": "function_definition",
            "parameters": [{"name": "k", "var_id": "K"}]}
    n_def = {"type": "expression_statement", "expression": "n = k == 0 ? 6 : 5;", "start": [1, 4], "end": [1, 22],
             "scope_depth": 1, "left_side": [{"name": "n", "var_id": "N"}], "right_side": [{"name": "k", "var_id": "K"}]}
    loop = {"type": "for_statement", "expression": "for(i = 0; i < n; i++){ x(i); }", "start": [2, 4], "end": [4, 5],
            "scope_depth": 1, "left_side": [{"name": "i", "var_id": "I"}],
            "right_side": [{"name": "i", "var_id": "I"}, {"name": "n", "var_id": "N"}], "relevant_to_dataflow": True}
    body = {"type": "expression_statement", "expression": "x(i);", "start": [3, 8], "end": [3, 13], "scope_depth": 2,
            "left_side": [], "right_side": [{"name": "i", "var_id": "I"}], "relevant_to_dataflow": True}
    pre = {"type": "preproc_if", "expression": "#if !UNCHECKED_BITSTREAM_READER y(); #endif", "start": [5, 0],
           "end": [7, 6], "scope_depth": 1, "parts": [{"part_nname": "condition", "expression": "!UNCHECKED_BITSTREAM_READER"}],
           "left_side": [], "right_side": [], "relevant_to_dataflow": True}
    y = {"type": "expression_statement", "expression": "y();", "start": [6, 4], "end": [6, 8], "scope_depth": 1,
         "left_side": [], "right_side": [], "relevant_to_dataflow": True}
    after = {"type": "expression_statement", "expression": "z();", "start": [8, 4], "end": [8, 8], "scope_depth": 1,
             "left_side": [], "right_side": [], "relevant_to_dataflow": True}
    stmts = [head, n_def, loop, body, pre, y, after]
    _close_defs(stmts)
    assert n_def["relevant_to_dataflow"] is True                     # the def of the kept use `n`
    out = CrossFunctionEnricher._render_sliced(stmts, header="static int f(int k)").split("\n")
    assert out[0] == "static int f(int k) {"
    assert out[1:] == ["   n = k == 0 ? 6 : 5;", "   for(i = 0; i < n; i++) {", "     x(i);", "   }",
                       "   #if !UNCHECKED_BITSTREAM_READER", "   y();", "   #endif", "   z();", "}"]


def test_macro_write_effects(tmp_path):
    from crossslice.cross.enrich import macro_write_effects, macro_text, add_macro_writes
    assert macro_write_effects("#define CLOSE_READER(name, gb) (gb)->index = name ## _index") == ([1], set())
    aa = "#define AA(j) do { float tmp0 = ptr[-1-j] * csa_table[j][0] + ptr[j] * csa_table[j][1]; ptr[j] = tmp0; } while (0)"
    assert macro_write_effects(aa) == ([], {"ptr"})
    assert macro_write_effects("#define FFMIN(a,b) ((a) > (b) ? (b) : (a))") == ([], set())
    assert macro_write_effects("#define EXTRABYTES 24") is None
    h = tmp_path / "m.h"
    h.write_text("#define CLOSE_READER(name, gb) \\\n    (gb)->index = name ## _index\nint x;\n")
    assert macro_text(str(h), 0) == "#define CLOSE_READER(name, gb) (gb)->index = name ## _index"
    stmts = [
        {"name": "int f(GetBitContext *s, int n) {", "type": "function_definition",
         "parameters": [{"name": "s", "var_id": "S"}, {"name": "n", "var_id": "N"}]},
        {"type": "expression_statement", "expression": "CLOSE_READER(re, s);", "left_side": [], "right_side": [],
         "calls_info": [{"function_name": "CLOSE_READER", "arguments": [
             {"name": "re", "arg_pos": 0}, {"name": "s", "arg_pos": 1}]}]},
        {"type": "expression_statement", "expression": "ptr = s->buf + 18;", "left_side": [{"name": "ptr", "var_id": "P"}],
         "right_side": [{"name": "s", "var_id": "S"}], "calls_info": []},
        {"type": "expression_statement", "expression": "AA(0);", "left_side": [], "right_side": [],
         "calls_info": [{"function_name": "AA", "arguments": [{"name": "0", "arg_pos": 0}]}]},
    ]
    summary = {"params_read": ["s"], "params_written": [], "returns": []}
    aa_h = tmp_path / "aa.h"
    aa_h.write_text(aa + "\n")
    lookup = {"CLOSE_READER": [(str(h), 0)], "AA": [(str(aa_h), 0)]}
    add_macro_writes(stmts, summary, lambda name: lookup.get(name, []), {})
    assert summary["params_written"] == ["s*"]             # through the macro parameter and through the alias ptr


def test_reaching_definitions_not_every_assignment():
    from crossslice.cross.context import _close_defs
    head = {"name": "int f(int a) {", "type": "function_definition", "parameters": [{"name": "a", "var_id": "A"}]}
    def st(expr, start, end, depth, L=(), R=(), type="expression_statement", rel=None):
        d = {"type": type, "expression": expr, "start": start, "end": end, "scope_depth": depth,
             "left_side": [{"name": n, "var_id": n.upper()} for n in L],
             "right_side": [{"name": n, "var_id": n.upper()} for n in R]}
        if rel: d["relevant_to_dataflow"] = True
        return d
    stmts = [head,
             st("for(i = 0; i < 3; i++) x(i);", [1, 4], [2, 10], 1, L=("i",), R=("i",), type="for_statement"),
             st("x(i);", [2, 8], [2, 13], 1, R=("i",)),
             st("int t;", [3, 4], [3, 10], 1, L=("t",)),
             st("t = 5;", [4, 4], [4, 10], 1, L=("t",)),
             st("if(a) t = 1; else t = 0;", [5, 4], [8, 10], 1, R=("a",), type="if_statement"),
             st("t = 1;", [6, 8], [6, 14], 1, L=("t",)),
             st("t = 0;", [8, 8], [8, 14], 1, L=("t",)),
             st("for(i = 0; i < n; i++) y(tab[t]);", [9, 4], [10, 14], 1, L=("i",), R=("i", "n"), type="for_statement", rel=True),
             st("y(tab[t]);", [10, 8], [10, 18], 1, R=("t",), rel=True)]
    _close_defs(stmts)
    rel = [s["expression"] for s in stmts[1:] if s.get("relevant_to_dataflow")]
    assert "t = 1;" in rel and "t = 0;" in rel and "t = 5;" in rel      # both branches + the unconditional def
    assert "int t;" not in rel                                          # stops at the reaching unconditional def
    assert "for(i = 0; i < 3; i++) x(i);" not in rel                     # the loop's own i: no history pulled in


def test_loop_headers_from_parts():
    line = CrossFunctionEnricher._stmt_line
    f = {"type": "for_statement", "expression": "for(i = 0; i < 2; i++)g->table_select[i] = get_bits(&s->gb, 5);",
         "scope_depth": 1, "parts": [{"part_nname": "initializer", "expression": "i = 0"},
                                     {"part_nname": "condition", "expression": "i < 2"},
                                     {"part_nname": "update", "expression": "i++"},
                                     {"part_nname": "body", "expression": "g->table_select[i] = get_bits(&s->gb, 5);"}]}
    assert line(f).strip() == "for(i = 0; i < 2; i++)"
    w = {"type": "while_statement", "expression": "while((c = *key++)){ h = h + c; }", "scope_depth": 1,
         "parts": [{"part_nname": "condition", "expression": "((c = *key++))"},
                   {"part_nname": "body", "expression": "{ h = h + c; }"}]}
    assert line(w).strip() == "while((c = *key++)) {"
