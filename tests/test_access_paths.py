"""Tests for the field-sensitive def/use engine (crossslice/intra/access_paths.py):
access paths as variables, and the def-use slice that follows them."""
import glob
import os

import pytest
from helpers import FIXTURES, analyze_function, find_stmt, names, path_names, relevant_exprs

from crossslice.intra import general_code_analyzer as g
from crossslice.intra.access_paths import walk_defs_uses_fields, written_positions
from crossslice.intra.relevant_dataflow import find_relevant_dataflow
from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC


def parts(entries):
    return path_names(entries, parts=True)


def stmt(function, expression):
    return find_stmt(analyze_function("access_paths", function)["statements"], expression)


# ---------------------------------------------------------------------------
# Writes
# ---------------------------------------------------------------------------
def test_pointer_write_defines_pointee_not_pointer():
    s = stmt("writes", "*len = x;")
    assert names(s["left_side"]) == []
    assert parts(s["left_side"]) == ["len[]", "len{*}"]
    assert names(s["right_side"]) == ["len", "x"]


def test_field_write_defines_path_and_parts_of_prefixes():
    s = stmt("writes", "s->gb.x = 1;")
    assert names(s["left_side"]) == []
    assert sorted(parts(s["left_side"])) == ["s->gb.x", "s->gb{*}", "s[]{*}", "s{*}"]
    assert names(s["right_side"]) == ["s"]
    assert path_names(s["right_side"]) == []          # the address is computed, nothing read


def test_compound_assignment_and_increment_read_the_path_too():
    s = stmt("writes", "s->gb.x += 1;")
    assert path_names(s["left_side"]) == ["s->gb.x"]
    assert sorted(parts(s["right_side"])) == ["s->gb", "s->gb.x", "s->gb.x{*}", "s[]"]
    s = stmt("writes", "s->n++;")
    assert path_names(s["left_side"]) == ["s->n"]
    assert "s->n" in path_names(s["right_side"])


def test_canonical_forms():
    ids = {}
    for expr in ("(*s).y = 2;", "s[0].y = 3;"):
        s = stmt("writes", expr)
        assert path_names(s["left_side"]) == ["s->y"]      # (*s).y, s[0].y: index-insensitive
        ids[expr] = [e["var_id"] for e in s["left_side"] if e["id_type"] == "access_path"][0]
    assert len(set(ids.values())) == 1, "(*s).y and s[0].y are the same object"
    s = stmt("reads", "int w = *&x;")
    assert names(s["right_side"]) == ["x"] and path_names(s["right_side"]) == []


def test_subscript_write_is_index_insensitive_and_reads_the_index():
    s = stmt("writes", "a[i] = x;")
    assert names(s["left_side"]) == []                 # the scalar engine defined `a` here
    assert parts(s["left_side"]) == ["a[]", "a{*}"]
    assert sorted(names(s["right_side"])) == ["a", "i", "x"]


def test_struct_value_field_write():
    s = stmt("writes", "v.q = 2;")
    assert parts(s["left_side"]) == ["v.q", "v{*}"]
    assert names(s["right_side"]) == ["v"]


def test_write_through_pointer_chain_reads_the_intermediate_pointer():
    s = stmt("writes", "s->next->n = 4;")
    assert path_names(s["left_side"]) == ["s->next->n"]
    assert sorted(path_names(s["right_side"])) == ["s->next", "s[]"]
    s = stmt("writes", "s->buf[i] = 'c';")
    assert path_names(s["left_side"]) == ["s->buf[]"]
    assert sorted(path_names(s["right_side"])) == ["s->buf", "s[]"]
    assert "i" in names(s["right_side"])


# ---------------------------------------------------------------------------
# Reads
# ---------------------------------------------------------------------------
def test_subscript_read_is_a_use_not_a_def():
    s = stmt("reads", "int x = a[i];")
    assert names(s["left_side"]) == ["x"]
    assert sorted(names(s["right_side"])) == ["a", "i"]
    assert parts(s["right_side"]) == ["a[]", "a[]{*}"]


def test_read_uses_path_part_and_prefixes():
    s = stmt("reads", "int z = s->gb.x +(*s).gb.size;")
    assert sorted(path_names(s["right_side"])) == ["s->gb", "s->gb.size", "s->gb.x", "s[]"]
    assert "s->gb.x{*}" in parts(s["right_side"])
    assert names(s["right_side"]) == ["s", "s"]


def test_address_of_path_is_a_read():
    s = stmt("reads", "struct gb *g = &s->gb;")
    assert names(s["left_side"]) == ["g"]
    assert sorted(parts(s["right_side"])) == ["s->gb", "s->gb{*}", "s[]"]
    s = stmt("reads", "int *q = &a[i];")              # &a[i] is a + i: the array itself
    assert sorted(names(s["right_side"])) == ["a", "i"]
    assert parts(s["right_side"]) == ["a{*}"]


def test_sizeof_operand_has_no_path_entries():
    s = stmt("reads", "int k = sizeof(s->gb);")
    assert names(s["right_side"]) == ["s"]
    assert parts(s["right_side"]) == []


def test_bare_identifier_in_value_flow_position_uses_its_parts():
    assert parts(stmt("calls", "consume(s);")["right_side"]) == ["s{*}"]
    assert parts(stmt("calls", "consume(v);")["right_side"]) == ["v{*}"]
    assert parts(stmt("reads", "int y = *len;")["right_side"]) == ["len[]", "len[]{*}"]
    assert parts(stmt("calls", "if(s == 0)return;")["right_side"]) == []   # a comparison reads no contents


# ---------------------------------------------------------------------------
# Calls
# ---------------------------------------------------------------------------
def test_writer_table():
    assert written_positions("memcpy", 3, []) == {0}
    assert written_positions("scanf", 3, []) == {1, 2}
    assert written_positions("sscanf", 4, []) == {2, 3}
    assert written_positions("unknown", 2, ["unknown"]) == {0, 1}   # the scalar engine's rule
    assert written_positions("unknown", 2, []) == frozenset()


def test_scanf_defines_the_variable():
    s = stmt("calls", 'scanf("%d", &x);')
    assert names(s["left_side"]) == ["x"]
    assert names(s["right_side"]) == ["scanf"]


def test_writer_through_pointer_defines_the_pointee():
    s = stmt("calls", "gets(buf);")
    assert parts(s["left_side"]) == ["buf[]", "buf{*}"]
    assert names(s["right_side"]) == ["gets", "buf"]
    s = stmt("calls", "memcpy(s->buf + s->n, buf, 4);")
    assert sorted(parts(s["left_side"])) == ["s->buf[]", "s->buf{*}", "s[]{*}", "s{*}"]
    assert "s->buf" in path_names(s["right_side"]) and "s->buf{*}" not in parts(s["right_side"])
    assert "buf{*}" in parts(s["right_side"])          # the source is read
    s = stmt("calls", "memset(s, 0, sizeof(*s));")
    assert parts(s["left_side"]) == ["s[]", "s{*}"]
    s = stmt("calls", 'sscanf(buf, "%d", &s->n);')
    assert path_names(s["left_side"]) == ["s->n"]


def test_address_argument_of_unknown_callee_is_a_read():
    s = stmt("calls", "init_get_bits(&s->gb, s->buf, 8);")
    assert s["left_side"] == []
    assert sorted(path_names(s["right_side"])) == ["s->buf", "s->gb", "s[]"]


# ---------------------------------------------------------------------------
# The slice follows the paths
# ---------------------------------------------------------------------------
def slice_of(function, seed, level=2):
    stmts = analyze_function("access_paths", function)["statements"]
    find_stmt(stmts, seed)["change_status"] = "changed"
    find_relevant_dataflow(stmts, level=level)
    return relevant_exprs(stmts)


def test_out_parameter_write_reaches_its_read():
    assert slice_of("out_param", "*len = n;") == {"*len = n;", "return *len;"}


def test_field_write_reaches_reads_of_that_field_only():
    rel = slice_of("field_flow", "s->gb.x = n;")
    assert "int a = s->gb.x;" in rel and "return a;" in rel
    assert "int b = s->y;" not in rel and "int c = s->n;" not in rel and "s->y = 7;" not in rel


def test_whole_object_writes_and_reads():
    rel = slice_of("whole_object", "memset(s, 0, sizeof(*s));")
    assert {"int b = s->y;", "consume(s);"} <= rel          # everything read through s
    assert "v.q = 1;" not in rel
    rel = slice_of("whole_object", "v.q = 1;")
    assert "u = v;" in rel and "return u.q;" in rel           # a struct copy reads every field
    assert "int b = s->y;" not in rel


def test_buffer_write_reaches_the_pointer_handed_on():
    rel = slice_of("buffer_flow", "memcpy(s->buf + s->n, src, n);")
    assert "init(s->buf);" in rel
    assert "if(s->buf)return 1;" in rel                      # a pointer read, over-approximated
    assert "return s->y;" not in rel
    assert "s->n = n;" not in rel                            # a later write does not depend on it


def test_bare_pointer_argument_depends_on_field_writes_a_comparison_does_not():
    rel = slice_of("bare_pointer", "s->n = n;")
    assert "consume(s);" in rel
    assert "if(s)n = 1;" not in rel


def test_scanf_result_flows_on():
    assert slice_of("scanf_flow", 'scanf("%d", &x);') == {'scanf("%d", &x);', "y = x;", "return y;"}


def test_array_element_write_reaches_later_element_reads_and_the_array_passed_on():
    rel = slice_of("array_flow", "a[i] = 1;")
    assert {"int after = a[j];", "sum(a);", "return after;"} <= rel
    assert "int before = a[j];" not in rel


def test_macro_call_without_semicolon_keeps_the_error_node_identifiers():
    # `LOCK(t, 0) i++;` parses as an update_expression whose operand is the
    # call, with `i` in an ERROR node: still a use of i, as in the scalar engine
    s = stmt("macro_tail", "LOCK(t, 0)i++;")
    assert "i" in names(s["right_side"])
    s = stmt("macro_tail", "LOCK(1)listp = &p5s;")
    assert "listp" in names(s["right_side"])


# ---------------------------------------------------------------------------
# Relation to the scalar engine
# ---------------------------------------------------------------------------
def _scalar_sets(walker, node, sm, scope):
    d, u = [], []
    walker(node, g.field_role_map, d, u, role="use", scope_manager=sm, stmt_scope=scope,
           call_role_map=g.ctf_mapping.get("call_role_map", []), id_type_str="variable")
    keep = ("variable", "function_call")
    return ({(e["name"], e["var_id"]) for e in d if e["id_type"] in keep},
            {(e["name"], e["var_id"]) for e in u if e["id_type"] in keep})


def test_scalar_entries_match_the_scalar_engine():
    """On every statement of the fixtures and example projects, the scalar
    entries are those of the scalar engine, except where that engine was
    wrong: a subscript read defined the array, and every identifier argument
    of scanf/fgets/gets was a definition."""
    files = sorted(glob.glob(str(FIXTURES / "*.c")) +
                   glob.glob(str(FIXTURES.parent.parent / "examples" / "**" / "*.c"), recursive=True))
    assert len(files) > 20
    checked = differing = 0
    writers = tuple(f"{w}(" for w in ("scanf", "sscanf", "fgets", "gets", "memcpy", "memset", "strcpy",
                                       "snprintf", "sprintf", "strncpy", "memmove", "fread", "strtol"))
    for f in files:
        root = SourceCodeParserC(f).get_top_level_node()
        for fnode in [c for c in root.named_children if c.type == "function_definition"]:
            body = fnode.child_by_field_name("body")
            if body is None:
                continue
            sm = g.ScopeManager()
            func_scope = sm.enter_scope(fnode.id)
            decl = fnode.child_by_field_name("declarator")
            while decl is not None and decl.type != "function_declarator":
                inner = decl.child_by_field_name("declarator")
                if inner is None:
                    break
                decl = inner
            if decl is not None:
                for pname, pid in g.extract_parameter_identifiers(decl.child_by_field_name("parameters")):
                    sm.declare(pname, pid.id)
            for child in body.named_children:
                g.register_declarations(child, sm)
            nodes = []
            g.collect_statements(body, g.ctf_mapping["statement_types"], nodes)
            for node in nodes:
                scope = sm.get_scope_for_node(node, fallback=func_scope)
                old = _scalar_sets(g.walk_defs_uses_scalar, node, sm, scope)
                new = _scalar_sets(walk_defs_uses_fields, node, sm, scope)
                checked += 1
                if old == new:
                    continue
                differing += 1
                text = g.clean_string(g.get_node_text_without_comments(node))
                assert "[" in text or any(w in text for w in writers), \
                    f"unexpected scalar difference in {os.path.basename(f)}: {text}\n{old}\n{new}"
    assert checked > 300 and differing > 0


def test_scalar_engine_selectable(monkeypatch):
    monkeypatch.setattr(g, "_DEFUSE_ENGINE", "scalar")
    g_analysis = g.create_ast_json(str(FIXTURES / "fields.c"), 2)
    s = find_stmt(g_analysis["statements"], "s->field = x;")
    assert s["left_side"] == [] and parts(s["right_side"]) == []
