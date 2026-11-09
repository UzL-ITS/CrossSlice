"""
Cross-function (inter-procedural) commit context enrichment.

Consumes the intra-procedural pipeline's internals (merged, relevance-sliced
statement lists per changed function) and expands the context one level across
the function boundary:

  downward: callees invoked from relevant statements are resolved via the
            gtags -> tree-sitter -> clangd cascade and their bodies are sliced
            seeded at parameters and returns (macros: definition text);
  upward:   callers of the changed functions are located via gtags references,
            and the call-site neighborhood in each caller is sliced.

Both program versions (parent and target commit) are handled; results present
in both with identical definitions are emitted once.
"""

import os
import re
import sys
from collections import defaultdict
from typing import Dict, List, Optional, Tuple


from crossslice.cross.gtags_handler import GtagsHandler
from crossslice.cross.resolve import (
    CallSite, CallerSite, ResolvedTarget, TargetResolver, Worktree,
)
from crossslice.intra.general_code_analyzer import create_ast_json, create_ast_json_region
from crossslice.intra.relevant_dataflow import find_relevant_dataflow
from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC

# statement types rendered header-only (their full expression is the whole block)
_CONTROL_FLOW_TYPES = {
    "if_statement", "for_statement", "while_statement", "do_statement",
    "switch_statement", "case_statement", "preproc_if", "preproc_ifdef",
    "preproc_else", "preproc_elif",
}

_IDENT_RE = re.compile(r"^[A-Za-z_]\w*$")
_MACRO_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]{2,}$")
_MACRO_STOPLIST = {"NULL", "TRUE", "FALSE", "EOF", "INT_MAX", "INT_MIN",
                   "SIZE_MAX", "UINT_MAX", "LONG_MAX", "CHAR_BIT", "EXIT_FAILURE",
                   "EXIT_SUCCESS", "STDIN_FILENO", "STDOUT_FILENO", "STDERR_FILENO"}


def _bare_name(signature_like: str) -> str:
    """'static inline int get_bits_count(const GetBitContext *s)' -> 'get_bits_count'"""
    m = re.search(r"(\w+)\s*\(", signature_like or "")
    return m.group(1) if m else (signature_like or "").strip()


def _pos_le(a, b):
    return (a[0], a[1]) <= (b[0], b[1])


def _hot_arg_positions(call: dict, stmt: dict) -> List[int]:
    """Argument positions whose expression contains at least one variable
    occurrence (constants and string literals don't seed the callee slice)."""
    var_positions = [v.get("position_start") for v in
                     stmt.get("left_side", []) + stmt.get("right_side", [])
                     if v.get("position_start") and v.get("id_type") != "function_call"]
    hot = []
    for arg in call.get("arguments", []):
        ps, pe = arg.get("position_start"), arg.get("position_end")
        if ps is None or pe is None:
            continue
        if any(_pos_le(ps, vp) and _pos_le(vp, pe) for vp in var_positions):
            hot.append(arg["arg_pos"])
    return hot


def _result_used(call: dict, stmt: dict) -> bool:
    """Whether the call's return value is consumed at this site.

    A lone call as the whole expression statement with no definitions means
    the result is discarded — the callee's returns need not seed the slice.
    """
    if stmt.get("type") != "expression_statement":
        return True
    if stmt.get("left_side"):
        return True
    expr = (stmt.get("expression") or "").strip().rstrip(";").strip()
    return not expr.startswith(call.get("function_name", "") + "(") and \
        not expr.startswith(call.get("function_name", "") + " (")


_HEADS_CACHE: Dict[str, Dict[int, str]] = {}
# `#define INTFLOAT float`: an object-like macro naming a type; `(INTFLOAT)(x)`
# parses as a call but is a cast. `#define zcopy memcpy` (an alias) stays a call.
_TYPE_MACRO_RE = re.compile(
    r"^#\s*define\s+[A-Za-z_]\w*\s+(?:(?:unsigned|signed|const|volatile|struct|union|enum)\s+)*"
    r"(?:int|float|double|char|short|long|void|bool|_Bool|\w+_t)(?:\s*\*+)?\s*$")


def is_type_macro(define_line: str) -> bool:
    return bool(_TYPE_MACRO_RE.match((define_line or "").strip()))


_DEFINE_FN_RE = re.compile(r"#\s*define\s+([A-Za-z_]\w*)\(([^)]*)\)\s*(.*)$", re.S)


def macro_text(abs_file: str, line0: int) -> str:
    """The `#define` at line0 with its backslash continuations joined."""
    try:
        lines = open(abs_file, errors="replace").read().split("\n")
    except OSError:
        return ""
    chunk, i = [], line0
    while i < len(lines):
        chunk.append(lines[i].rstrip())
        if not lines[i].rstrip().endswith("\\"):
            break
        i += 1
    return " ".join(l.rstrip("\\").strip() for l in chunk)


def macro_write_effects(text: str):
    """For a function-like macro: (positions of the parameters it writes through,
    the caller's variables it writes through by name). None for other text."""
    m = _DEFINE_FN_RE.match(text.strip())
    if not m:
        return None
    params = [p.strip() for p in m.group(2).split(",") if p.strip() and p.strip() != "..."]
    written = CrossFunctionEnricher._written_bases(m.group(3))
    return [i for i, p in enumerate(params) if p in written], written - set(params)


def add_macro_writes(stmts: List[dict], summary: dict, lookup, cache: dict) -> None:
    """Credit the writes a called macro makes (`CLOSE_READER(re, gb)` writes
    `(gb)->index`; `AA(0)` writes through the caller's `ptr`) to the caller's
    parameters. `lookup(name)` returns the (abs_file, line0) of a name's
    function-like macro definitions; `cache` memoizes the effects per name."""
    params = [p.get("name") for p in stmts[0].get("parameters", []) if p.get("name")]
    if not params:
        return
    aliases = CrossFunctionEnricher._param_aliases(stmts, set(params))
    written = set(summary.get("params_written", []))

    def credit(base):
        target = base if base in params else aliases.get(base)
        if target:
            written.add(target + "*")

    for s in stmts[1:]:
        if s.get("type") in _CONTROL_FLOW_TYPES:
            continue
        for c in s.get("calls_info", []):
            name = c.get("function_name", "")
            if not _IDENT_RE.match(name) or name in params:
                continue
            if name not in cache:
                effects = None
                for abs_file, line0 in (lookup(name) or [])[:3]:
                    e = macro_write_effects(macro_text(abs_file, line0))
                    if e:
                        effects = (sorted(set((effects[0] if effects else []) + e[0])),
                                   (effects[1] if effects else set()) | e[1])
                cache[name] = effects
            effects = cache[name]
            if not effects:
                continue
            args = c.get("arguments") or []
            for pos in effects[0]:
                arg = next((a for a in args if isinstance(a, dict) and a.get("arg_pos") == pos),
                           args[pos] if pos < len(args) else None)
                text = arg.get("name", "") if isinstance(arg, dict) else (arg or "")
                m = CrossFunctionEnricher._ARG_BASE_RE.match(str(text))
                if m:
                    credit(m.group(1))
            for base in effects[1]:
                credit(base)
    summary["params_written"] = sorted(written)


def macro_definitions(gtags, root: str, name: str):
    """(abs_file, line0) of every function-like macro definition of `name` in the index."""
    out = []
    for d in gtags.find_function_definition_detailed(name):
        if re.match(rf"#\s*define\s+{re.escape(name)}\s*\(", d.get("code_line", "")):
            f = d["file_path"]
            out.append((f if os.path.isabs(f) else os.path.join(root, f), d["line_number"] - 1))
    return out


def _definition_head(abs_file: str, line0: int) -> Optional[str]:
    """`static int f(int a)`: the head of the definition starting at line0,
    joined onto one line (tree-sitter), cached per file."""
    heads = _HEADS_CACHE.get(abs_file)
    if heads is None:
        heads = {}
        try:
            for node, _name, s0, _e0 in SourceCodeParserC(abs_file).collect_function_definitions():
                if node.type == "function_definition":
                    head = node.text.decode("utf-8", errors="replace").split("{")[0]
                    heads[s0] = " ".join(p.strip() for p in head.split("\n") if p.strip())[:200]
        except Exception:
            pass
        _HEADS_CACHE[abs_file] = heads
    return heads.get(line0)


class CrossFunctionEnricher:

    def __init__(self, repo_path: str, old_commit: str, new_commit: str,
                 slice_level: int = 2, max_callees: int = 12,
                 max_callers_per_fn: int = 4, cross_depth: int = 1,
                 audit_lsp: bool = False, debug: bool = False,
                 cache_dir: Optional[str] = None):
        self.repo_path = repo_path
        # per-commit GNU Global indexes are shared with the graph store
        # (crossslice.paths); None disables the cache
        self.cache_dir = cache_dir
        self.old_commit = old_commit
        self.new_commit = new_commit
        self.slice_level = slice_level
        self.max_callees = max_callees
        self.max_callers_per_fn = max_callers_per_fn
        self.cross_depth = cross_depth  # 1: sliced ring-1 bodies; >=2: + ring-2 summaries
        self.debug = debug
        self.audit_lsp = audit_lsp
        self.last_results = None
        self.resolution_failures: Dict[str, str] = {}
        self.lsp_audit: List[dict] = []

    # ------------------------------------------------------------------
    # 1. collect targets from the merged intra-procedural statements
    # ------------------------------------------------------------------

    def _collect_targets(self, internals) -> Tuple[Dict[str, List[CallSite]],
                                                   Dict[str, List[CallSite]],
                                                   List[str]]:
        old_sites: Dict[str, List[CallSite]] = defaultdict(list)
        new_sites: Dict[str, List[CallSite]] = defaultdict(list)
        changed_fns: List[str] = []

        for entry in internals:
            mapping = entry["mapping"]
            rel_old = mapping.get("old_relative_path")
            rel_new = mapping.get("new_relative_path")

            for data in (entry.get("old_data"), entry.get("new_data")):
                if data and data.get("statements"):
                    first = data["statements"][0]
                    if first.get("type") == "function_definition":
                        name = _bare_name(first.get("name", ""))
                        if name and name not in changed_fns:
                            changed_fns.append(name)

            for stmt in entry.get("merged", []):
                status = stmt.get("change_status")
                relevant = stmt.get("relevant_to_dataflow") or (status and status != "matched")
                if not relevant:
                    continue

                def add(calls, sites, rel_file, src_stmt):
                    if not rel_file:
                        return
                    from_cf = src_stmt.get("type") in _CONTROL_FLOW_TYPES
                    for call in calls or []:
                        name = call.get("function_name", "")
                        if not _IDENT_RE.match(name):
                            continue  # function pointers / complex callees: Phase 3
                        r, c = call.get("position_start", [0, 0])
                        sites[name].append(CallSite(
                            callee=name,
                            arg_count=len(call.get("arguments", [])),
                            rel_file=rel_file, line=r, col=c,
                            hot_arg_positions=_hot_arg_positions(call, src_stmt),
                            result_used=_result_used(call, src_stmt),
                            from_control_flow=from_cf,
                        ))

                def add_object_macros(src_stmt, sites, rel_file):
                    # bare ALL_CAPS identifiers in *changed* statements are
                    # likely object-like macro uses (RETURN_FALSE, E_WARNING)
                    if not rel_file or status in (None, "matched"):
                        return
                    called = {c.get("function_name") for c in src_stmt.get("calls_info", [])}
                    for v in src_stmt.get("left_side", []) + src_stmt.get("right_side", []):
                        name = v.get("name", "")
                        if not _MACRO_NAME_RE.match(name) or name in _MACRO_STOPLIST \
                                or name in called:
                            continue
                        r, c = v.get("position_start", [0, 0])
                        sites[name].append(CallSite(
                            callee=name, arg_count=-1, rel_file=rel_file,
                            line=r, col=c, object_macro=True, result_used=False,
                        ))

                if status in ("deleted", "moved_from"):
                    add(stmt.get("calls_info"), old_sites, rel_old, stmt)
                    add_object_macros(stmt, old_sites, rel_old)
                elif status == "inserted":
                    add(stmt.get("calls_info"), new_sites, rel_new, stmt)
                    add_object_macros(stmt, new_sites, rel_new)
                elif status == "changed":
                    new_stmt = stmt.get("new_statement") or stmt
                    add(new_stmt.get("calls_info"), new_sites, rel_new, new_stmt)
                    add_object_macros(new_stmt, new_sites, rel_new)
                    old_stmt = stmt.get("old_statement") or {}
                    add(old_stmt.get("calls_info"), old_sites, rel_old, old_stmt)
                else:  # matched-but-relevant, moved
                    add(stmt.get("calls_info"), old_sites, rel_old, stmt)
                    add(stmt.get("calls_info"), new_sites, rel_new, stmt)

        # functions changed by the commit itself are already in the diff
        for sites in (old_sites, new_sites):
            for fn in changed_fns:
                sites.pop(fn, None)

        def cap(sites):
            return dict(sorted(sites.items(),
                               key=lambda kv: -len(kv[1]))[: self.max_callees])

        return cap(old_sites), cap(new_sites), changed_fns

    # ------------------------------------------------------------------
    # 2. per-version analysis inside a worktree
    # ------------------------------------------------------------------

    def _analyze_callee(self, wt_root: str, tgt: ResolvedTarget,
                        sites: Optional[List[CallSite]] = None) -> Optional[dict]:
        abs_file = os.path.join(wt_root, tgt.rel_file)
        if tgt.is_macro:
            try:
                parser = SourceCodeParserC(abs_file)
                for node, name, s, e in parser.collect_function_definitions():
                    if node.type == "preproc_function_def" and s == tgt.line:
                        tgt.code = node.text.decode("utf-8", errors="replace").rstrip("\\\n ")
                        break
            except Exception:
                pass
            if not tgt.code:
                # object-like macro: take the #define line + backslash continuations
                try:
                    lines = open(abs_file, errors="replace").read().split("\n")
                    chunk, i = [], tgt.line
                    while i < len(lines):
                        chunk.append(lines[i])
                        if not lines[i].rstrip().endswith("\\"):
                            break
                        i += 1
                    tgt.code = "\n".join(chunk).strip()
                except Exception:
                    tgt.code = tgt.signature
            return {"target": tgt, "rendered": tgt.code, "kind": "macro"}

        try:
            data = create_ast_json(abs_file, tgt.line)
        except Exception as e:
            if self.debug:
                print(f"[cross] callee analysis failed for {tgt.name}: {e}")
            return None
        if not data or not data.get("statements"):
            return None

        stmts = data["statements"]
        params = stmts[0].get("parameters", [])
        param_ids = {p.get("var_id") for p in params if p.get("var_id")}

        # selective seeding from the call sites: only parameters bound to
        # argument expressions that carry variables, and returns only when
        # some site consumes the result. Control-flow statements aggregate all
        # calls of their subtree, so their sites carry no per-call binding —
        # a callee reachable only through such aggregates (or without binding
        # info) falls back to full seeding.
        leaf_sites = [s for s in (sites or [])
                      if not s.from_control_flow and s.hot_arg_positions is not None]
        if leaf_sites:
            hot_positions = set()
            for s in leaf_sites:
                hot_positions.update(s.hot_arg_positions)
            seed_param_ids = {p.get("var_id") for i, p in enumerate(params)
                              if i in hot_positions and p.get("var_id")}
            seed_returns = any(s.result_used for s in leaf_sites)
        else:
            seed_param_ids = param_ids
            seed_returns = True

        for s in stmts[1:]:
            touched = {v.get("var_id") for v in s.get("left_side", []) + s.get("right_side", [])}
            if (touched & seed_param_ids) or \
                    (seed_returns and s.get("type") == "return_statement"):
                s["change_status"] = "changed"
        find_relevant_dataflow(stmts, level=self.slice_level)

        rendered = self._render_sliced(stmts, header=tgt.signature)
        summary = self._summarize(stmts, param_ids)

        # candidate calls for a further expansion ring: calls in the sliced
        # (relevant) statements of this callee
        ring2_calls: Dict[str, List[CallSite]] = {}
        for s in stmts[1:]:
            if not s.get("relevant_to_dataflow") or s.get("type") in _CONTROL_FLOW_TYPES:
                continue
            for c in s.get("calls_info", []):
                cname = c.get("function_name", "")
                if not _IDENT_RE.match(cname) or cname == tgt.name:
                    continue
                r0, c0 = c.get("position_start", [0, 0])
                ring2_calls.setdefault(cname, []).append(CallSite(
                    callee=cname, arg_count=len(c.get("arguments", [])),
                    rel_file=tgt.rel_file, line=r0, col=c0))

        return {"target": tgt, "rendered": rendered, "kind": "function",
                "summary": summary, "ring2_calls": ring2_calls}

    def _analyze_caller(self, wt_root: str, site: CallerSite) -> Optional[dict]:
        abs_file = os.path.join(wt_root, site.rel_file)
        try:
            if site.caller_header:   # attributed by resolve.enclosing_header: no function_definition node
                data = create_ast_json_region(abs_file, site.caller_start_line)
            else:
                data = create_ast_json(abs_file, site.caller_start_line)
        except Exception:
            return None
        if not data or not data.get("statements"):
            return None
        stmts = data["statements"]

        # seed: the most specific statement covering the reference line
        best = None
        for s in stmts[1:]:
            s0, e0 = s.get("start", [0, 0])[0], s.get("end", [0, 0])[0]
            if s0 <= site.line <= e0:
                if best is None or (e0 - s0) < (best.get("end", [0, 0])[0] - best.get("start", [0, 0])[0]):
                    best = s
        if best is None:
            return None
        best["change_status"] = "changed"
        find_relevant_dataflow(stmts, level=self.slice_level)
        return {"site": site, "rendered": self._render_sliced(stmts, mark_line=site.line,
                                       header=_definition_head(abs_file, site.caller_start_line)
                                       or site.caller_header or None)}

    # ------------------------------------------------------------------
    # rendering helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _stmt_line(stmt: dict, mark: bool = False) -> str:
        expr = stmt.get("expression", "")
        stype = stmt.get("type", "")
        if stype.startswith("preproc"):
            # header only: '#if <condition>' — the guarded statements are
            # rendered separately as children
            cond = next((p.get("expression") for p in stmt.get("parts", [])
                         if p.get("part_nname") == "condition"), None)
            directive = {"preproc_if": "#if", "preproc_ifdef": "#ifdef",
                         "preproc_elif": "#elif", "preproc_else": "#else"}.get(stype, "#if")
            expr = f"{directive} {cond}".strip() if cond or stype == "preproc_else" \
                else expr.split(" ")[0] + " ..."
        elif stype == "if_statement" and any(p.get("part_nname") == "condition"
                                             for p in stmt.get("parts", [])):
            # header from the IR parts: `if(cond)` plus ` {` when the then-branch
            # is a block; the branches' statements are rendered as children and
            # the else branch gets its own header (see _render_sliced)
            parts = {p.get("part_nname"): p for p in stmt.get("parts", [])}
            cons = (parts.get("consequence") or {}).get("expression") or ""
            expr = "if" + (parts["condition"].get("expression") or "")
            if cons.lstrip().startswith("{"):
                expr += " {"
        elif stype in ("for_statement", "while_statement", "switch_statement", "do_statement") \
                and any(p.get("part_nname") == "body" for p in stmt.get("parts", [])):
            # header from the IR parts; the body's statements are rendered as children
            parts = {p.get("part_nname"): (p.get("expression") or "") for p in stmt.get("parts", [])}
            cond = parts.get("condition", "")
            if stype == "for_statement":
                expr = f"for({parts.get('initializer', '')}; {cond}; {parts.get('update', '')})"
            elif stype == "do_statement":
                expr = "do"
            else:
                expr = stype.split("_")[0] + (cond if cond.startswith("(") else f"({cond})")
            if parts.get("body", "").lstrip().startswith("{"):
                expr += " {"
        elif stype in _CONTROL_FLOW_TYPES and "{" in expr:
            # header only: the block's statements are rendered as children;
            # a brace-less `while (c) stmt;` keeps its full text
            expr = expr.split("{")[0].rstrip() + " {"
        indent = "  " * max(stmt.get("scope_depth", stmt.get("scope_level", 1)), 1)
        prefix = ">" if mark else " "
        return f"{prefix}{indent}{expr}"

    @classmethod
    def _render_sliced(cls, stmts: List[dict], mark_line: Optional[int] = None,
                       header: Optional[str] = None) -> str:
        """Render the relevant statements of a function, one per line: control
        flow as headers with their closing braces, `...` for statements left
        out, `} else {` / `} else if (c) {` from the if statements' `alternative`
        parts (the IR lists both branches' statements flat), and brace-less
        bodies indented under their header."""
        lines = [(header or stmts[0].get("name", "")).rstrip(" {") + " {"]
        body = stmts[1:]
        relevant = [i for i, s in enumerate(body) if s.get("relevant_to_dataflow")]
        last_idx = -1
        blocks: List[dict] = []   # open blocks, outermost first: end, close, extra, indent, if_ref
        state = {"base": 0, "pending": 0}   # extra indentation: enclosing block's, + brace-less headers

        def pos(p):
            return tuple(p) if p else None

        def within(p, a, b):
            return p is not None and a is not None and a <= p and (b is None or p <= b)

        def indent(stmt, extra):
            return " " + "  " * max(stmt.get("scope_depth", stmt.get("scope_level", 1)), 1) + "  " * extra

        def ends_before(block, start):
            return start is not None and block["end"] is not None and block["end"] < start

        def pop_block(stmt, start):
            """Close the innermost block: a `}` line, or the else header of an if
            whose else branch begins at `stmt`. Returns the chain prefix for a
            `} else if` on `stmt`'s own line."""
            blk = blocks.pop()
            state["base"] = blocks[-1]["extra"] if blocks else 0
            state["pending"] = 0
            ref = blk.get("if_ref")
            if ref and not ref["emitted"] and start is not None and start >= ref["alt_start"]:
                ref["emitted"] = True
                close = "} " if blk["close"] else ""
                if stmt.get("type") == "if_statement" and start[0] == ref["alt_start"][0] \
                        and ref["alt_expr"].startswith("else if"):
                    return close + "else ", blk["extra"]           # chained `} else if(c) {`
                lines.append(blk["indent"] + close + ("else {" if ref["alt_braced"] else "else"))
                if ref["alt_braced"]:
                    blocks.append({"end": ref["end"], "close": "}", "extra": blk["extra"],
                                   "indent": blk["indent"], "if_ref": None})
                    state["base"], state["pending"] = blk["extra"], 0
                else:
                    state["pending"] = blk["extra"] - state["base"] + 1
            elif blk["close"]:
                lines.append(blk["indent"] + blk["close"])
            return "", None

        for k, i in enumerate(relevant):
            s = body[i]
            stype = s.get("type")
            start, end = pos(s.get("start")), pos(s.get("end"))
            gap = body[last_idx + 1:i]
            # statements left out: `...` inside the block they belong to
            closing = [blk for blk in blocks if ends_before(blk, start)]
            limit = closing[0]["end"] if closing else None
            gap_pos = [pos(g.get("start")) for g in gap]
            if gap and (limit is None or any(gp is None or gp < limit for gp in gap_pos)):
                lines.append("   ...")
            chain, force_extra = "", None
            while blocks and ends_before(blocks[-1], start):
                c, fx = pop_block(s, start)
                if c:
                    chain, force_extra = c, fx
            if gap and limit is not None and any(gp is not None and gp >= limit for gp in gap_pos):
                lines.append("   ...")

            extra = force_extra if force_extra is not None else state["base"] + state["pending"]
            mark = mark_line is not None and start is not None and start[0] == mark_line
            line = cls._stmt_line(s, mark=mark)
            line = line[0] + "  " * extra + line[1:]
            if chain:
                line = line.replace("if", chain + "if", 1)

            parts = {p.get("part_nname"): p for p in s.get("parts", []) if p.get("part_nname")}
            alt = parts.get("alternative")
            alt_start = pos(alt.get("start")) if alt else None
            nxt = body[relevant[k + 1]] if k + 1 < len(relevant) else None
            if stype == "if_statement" and "condition" in parts:
                cons = (parts.get("consequence") or {}).get("expression") or ""
                braced = cons.lstrip().startswith("{")
                if_ref = None
                if alt_start:
                    alt_expr = (alt.get("expression") or "").strip()
                    if_ref = {"end": end, "alt_start": alt_start, "alt_expr": alt_expr,
                              "alt_braced": alt_expr[4:].lstrip().startswith("{"), "emitted": False}
                if braced or if_ref:
                    blocks.append({"end": alt_start or end, "close": "}" if braced else None,
                                   "extra": extra, "indent": indent(s, extra), "if_ref": if_ref})
                if braced:
                    state["base"], state["pending"] = extra, 0
                elif nxt is not None and (start is None or pos(nxt.get("start")) is None
                                          or within(pos(nxt.get("start")), start, alt_start or end)):
                    state["pending"] += 1          # the then-statement comes next: indent it
            elif stype in ("preproc_if", "preproc_ifdef"):
                # `#if` ... `#endif`: a block that does not change the C scope depth
                blocks.append({"end": end, "close": "#endif", "extra": extra,
                               "indent": indent(s, extra), "if_ref": None})
            elif stype.startswith("preproc"):
                pass                                       # `#else` / `#elif`: closed by the #endif
            elif stype in _CONTROL_FLOW_TYPES:
                expr = s.get("expression", "")
                if line.rstrip().endswith("{"):
                    close = "}"
                    if stype == "do_statement":                     # do { ... } while (c);
                        close = "} " + expr.rsplit("}", 1)[-1].strip()
                    blocks.append({"end": end, "close": close, "extra": extra,
                                   "indent": indent(s, extra), "if_ref": None})
                    state["base"], state["pending"] = extra, 0
                else:
                    # brace-less `while (c) stmt;`: the text ends with the body statement,
                    # which follows as its own line — print the header alone, and
                    # indent the next line only when it is that body statement
                    child = (nxt.get("expression") or "").strip() if nxt else ""
                    if child and line.rstrip().endswith(child) and line.strip() != child:
                        line = line.rstrip()[:-len(child)].rstrip()
                    if nxt is not None and (start is None or pos(nxt.get("start")) is None
                                            or within(pos(nxt.get("start")), start, end)):
                        state["pending"] += 1
            else:
                state["pending"] = 0
            lines.append(line)
            last_idx = i

        if last_idx < len(body) - 1:
            lines.append("   ...")
        while blocks:
            pop_block({}, None)
        lines.append("}")
        return "\n".join(lines)

    # Writes through a parameter. The def/use engine demotes the base of a
    # pointer/field/index write to a use, so they are detected syntactically,
    # on non-control-flow statements (block statements are listed separately):
    #   *p = ..            p->f = ..  p.f = ..  p[i] = ..  (*p).f = ..   (+ compound assignment)
    #   p->f++  (*p)++  ++p->f  p[i]--
    #   memcpy(p, ..), strcpy(p->buf, ..), read(fd, p, n), ...   (library writers)
    #   f(&p)              (address taken in a call: an out-parameter)
    # and through local aliases of a parameter: `e = &s->entries[i]; e->v = ..`
    # is a write to s.
    _ID = r"[A-Za-z_]\w*"
    _ASSIGN = r"(?:[-+*/%|&^]|<<|>>)?=(?!=)"
    _DEREF_WRITE_RE = re.compile(rf"(?:^|[;{{(,])\s*\*\s*\(?\s*({_ID})\s*\)?\s*{_ASSIGN}")
    _FIELD_WRITE_RE = re.compile(
        rf"(?:^|[;{{(,])\s*\(?\s*\*?\s*\(?\s*({_ID})\s*\)?\s*(?:->|\.|\[)[^=<>!;{{}}()]*?{_ASSIGN}")
    _INCDEC_RES = (
        re.compile(rf"(?:\+\+|--)\s*\*\s*\(?\s*({_ID})"),                                 # ++*p
        re.compile(rf"(?:\+\+|--)\s*\(?\s*({_ID})\s*\)?\s*(?:->|\.|\[)"),                # ++p->f, ++p[i]
        re.compile(rf"\(\s*\*\s*({_ID})\s*\)\s*(?:\+\+|--)"),                             # (*p)++
        re.compile(rf"(?:^|[;{{(,=])\s*({_ID})\s*(?:->|\.)[\w\s.>-]*?(?:\+\+|--)"),         # p->f++
        re.compile(rf"(?:^|[;{{(,=])\s*({_ID})\s*(?:->|\.)?[\w.>-]*\[[^\]]*\]\s*(?:\+\+|--)"),  # p[i]++
    )
    _WRITER_CALLS = {  # library calls that write through an argument: name -> argument index
        "memcpy": 0, "memmove": 0, "memset": 0, "strcpy": 0, "strncpy": 0, "strcat": 0,
        "strncat": 0, "sprintf": 0, "snprintf": 0, "vsprintf": 0, "vsnprintf": 0, "strlcpy": 0,
        "strlcat": 0, "fgets": 0, "gets": 0, "fread": 0, "getline": 0, "bzero": 0, "bcopy": 1,
        "read": 1, "pread": 1, "recv": 1, "recvfrom": 1, "wmemcpy": 0, "wmemset": 0,
    }
    _CALL_RE = re.compile(rf"\b({_ID})\s*\(")
    _ADDR_ARG_RE = re.compile(rf"[(,]\s*&\s*({_ID})\b")
    _ARG_BASE_RE = re.compile(rf"\s*(?:\([^()]*\)\s*)*[&*]?\s*\(?\s*({_ID})")
    _ALIAS_RE = re.compile(
        rf"^\s*(?:(?:const|static|struct|union|unsigned|signed|volatile|register)\s+)*(?:{_ID}\s+)?[\s*]*"
        rf"({_ID})\s*=\s*(?:\(\s*[^()]*\)\s*)?&?\s*\(?\s*({_ID})\b(?!\s*\()")

    @classmethod
    def _call_args(cls, expr: str, open_paren: int) -> List[str]:
        """Top-level arguments of the call whose '(' is at `open_paren`."""
        depth, start, args = 0, open_paren + 1, []
        for i in range(open_paren, len(expr)):
            ch = expr[i]
            if ch in "([{":
                depth += 1
            elif ch in ")]}":
                depth -= 1
                if depth == 0:
                    args.append(expr[start:i])
                    break
            elif ch == "," and depth == 1:
                args.append(expr[start:i])
                start = i + 1
        return args

    @classmethod
    def _written_bases(cls, expr: str) -> set:
        """Identifiers written through (pointer, field, index, library writer,
        address taken in a call) in one statement's text."""
        bases = set()
        text = " " + expr
        for rx in (cls._DEREF_WRITE_RE, cls._FIELD_WRITE_RE, *cls._INCDEC_RES):
            bases.update(m.group(1) for m in rx.finditer(text))
        for m in cls._CALL_RE.finditer(text):
            idx = cls._WRITER_CALLS.get(m.group(1))
            if idx is None:
                continue
            args = cls._call_args(text, m.end() - 1)
            if idx < len(args):
                b = cls._ARG_BASE_RE.match(args[idx])
                if b:
                    bases.add(b.group(1))
        bases.update(m.group(1) for m in cls._ADDR_ARG_RE.finditer(text))
        return bases

    @classmethod
    def _param_aliases(cls, stmts: List[dict], param_names: set) -> dict:
        """Local aliases of a parameter's object: `e = &s->entries[i]`, `p = s + 1`,
        `q = s->name` (chains of two)."""
        alias: dict = {}
        plain = [s for s in stmts[1:] if s.get("type") not in _CONTROL_FLOW_TYPES]
        for _ in range(2):
            for s in plain:
                m = cls._ALIAS_RE.match(s.get("expression", ""))
                if not m:
                    continue
                lhs, rhs = m.group(1), m.group(2)
                if lhs in param_names:
                    continue
                target = rhs if rhs in param_names else alias.get(rhs)
                if target:
                    alias[lhs] = target
        return alias

    @classmethod
    def _modref_summary(cls, stmts: List[dict], param_ids: set) -> dict:
        """params_read: parameters whose value is used; params_written: `p*` for
        parameters whose pointed-to object is written (through p, an alias of p,
        a library writer or an out-argument); params_rebound: by-value parameters
        the function reassigns locally (invisible to the caller); returns: the
        return expressions."""
        params_read, params_written, rebound = set(), set(), set()
        param_names = {p.get("name") for p in stmts[0].get("parameters", []) if p.get("name")}
        for s in stmts:
            for v in s.get("left_side", []):
                if v.get("var_id") in param_ids:
                    rebound.add(v.get("name"))
            for v in s.get("right_side", []):
                if v.get("var_id") in param_ids:
                    params_read.add(v.get("name"))
                    param_names.add(v.get("name"))
        alias = cls._param_aliases(stmts, param_names)
        for s in stmts[1:]:
            if s.get("type") in _CONTROL_FLOW_TYPES:
                continue
            for base in cls._written_bases(s.get("expression", "")):
                target = base if base in param_names else alias.get(base)
                if target:
                    params_written.add(target + "*")
        returns = [s.get("expression") for s in stmts if s.get("type") == "return_statement"
                   and (s.get("expression") or "").strip() != "return;"]
        return {
            "params_read": sorted(x for x in params_read if x),
            "params_written": sorted(x for x in params_written if x),
            "params_rebound": sorted(x for x in rebound if x),
            "returns": returns[:6],
        }

    def _summarize(self, stmts: List[dict], param_ids: set) -> dict:
        """The summary plus the writes that called macros make (see add_macro_writes)."""
        summary = self._modref_summary(stmts, param_ids)
        lookup = getattr(self, "_macro_lookup", None)
        if lookup is not None:
            add_macro_writes(stmts, summary, lookup, self._macro_cache)
        return summary

    # ------------------------------------------------------------------
    # 3. orchestration
    # ------------------------------------------------------------------

    def enrich(self, internals) -> Tuple[str, dict]:
        old_sites, new_sites, changed_fns = self._collect_targets(internals)
        if self.debug:
            print(f"[cross] callee targets old={list(old_sites)} new={list(new_sites)} "
                  f"changed_fns={changed_fns}")

        results = {"old": {"callees": {}, "callers": {}, "ring2": {}},
                   "new": {"callees": {}, "callers": {}, "ring2": {}},
                   "stats": {}}

        for version, commit, sites in (("old", self.old_commit, old_sites),
                                       ("new", self.new_commit, new_sites)):
            want_callers = version == "new" and bool(changed_fns)
            if not sites and not want_callers:
                continue
            with Worktree(self.repo_path, commit) as wt:
                gtags = GtagsHandler(wt.path, cache_dir=os.path.join(
                    self.cache_dir, "gtags", commit) if self.cache_dir else None)
                if not gtags.ensure_index():
                    continue
                self._macro_lookup = lambda n, g=gtags, r=wt.path: macro_definitions(g, r, n)
                self._macro_cache = {}
                resolver = TargetResolver(wt.path, audit_lsp=self.audit_lsp,
                                          debug=self.debug)
                try:
                    resolved = resolver.resolve(sites, gtags)
                    for name, tgt in resolved.items():
                        analyzed = self._analyze_callee(wt.path, tgt, sites.get(name))
                        if analyzed:
                            results[version]["callees"][name] = analyzed
                    if self.cross_depth >= 2:
                        self._expand_ring2(wt.path, resolver, gtags,
                                           results[version], changed_fns)
                    if want_callers:
                        callers = resolver.find_callers(
                            changed_fns, gtags, self.max_callers_per_fn)
                        for fn, cs in callers.items():
                            analyzed = [a for a in
                                        (self._analyze_caller(wt.path, c) for c in cs) if a]
                            if analyzed:
                                results[version]["callers"][fn] = analyzed
                finally:
                    results["stats"][version] = dict(resolver.stats)
                    self.resolution_failures.update(resolver.failures)
                    self.lsp_audit.extend(resolver.audit)
                    resolver.close()

        self.last_results = results
        return self._format(results), self._to_json(results)

    def _expand_ring2(self, wt_root, resolver, gtags, version_results, changed_fns):
        """Second expansion ring: signature + mod/ref summary only."""
        ring1 = set(version_results["callees"])
        calls: Dict[str, List[CallSite]] = {}
        for analyzed in version_results["callees"].values():
            for name, sites in (analyzed.get("ring2_calls") or {}).items():
                if name in ring1 or name in changed_fns:
                    continue
                calls.setdefault(name, []).extend(sites)
        if not calls:
            return
        resolved = resolver.resolve(calls, gtags)
        for name, tgt in resolved.items():
            summary = None
            if not tgt.is_macro:
                try:
                    data = create_ast_json(os.path.join(wt_root, tgt.rel_file), tgt.line)
                    if data and data.get("statements"):
                        stmts = data["statements"]
                        param_ids = {p.get("var_id")
                                     for p in stmts[0].get("parameters", [])
                                     if p.get("var_id")}
                        summary = self._summarize(stmts, param_ids)
                except Exception:
                    pass
            version_results["ring2"][name] = {"target": tgt, "summary": summary}

    def format_text(self, include_ring2: bool = True) -> str:
        """Re-render the last enrich() results, optionally without ring 2."""
        if self.last_results is None:
            return ""
        return self._format(self.last_results, include_ring2=include_ring2)

    # ------------------------------------------------------------------
    # output
    # ------------------------------------------------------------------

    def _format(self, results, include_ring2: bool = True) -> str:
        out = []

        # dedup: identical callee definitions present in both versions
        both, only = {}, {"old": {}, "new": {}}
        old_c, new_c = results["old"]["callees"], results["new"]["callees"]
        for name in dict.fromkeys([*old_c, *new_c]):  # discovery order (a set would vary per run)
            o, n = old_c.get(name), new_c.get(name)
            if o and n and o["target"].rel_file == n["target"].rel_file \
                    and o["target"].line == n["target"].line \
                    and o["rendered"] == n["rendered"]:
                both[name] = n
            else:
                if o:
                    only["old"][name] = o
                if n:
                    only["new"][name] = n

        def emit_callee(name, analyzed, version_label):
            t = analyzed["target"]
            kind = "macro" if analyzed["kind"] == "macro" else "function"
            out.append(f"-- called {kind}: {name} — {t.rel_file}:{t.line + 1} "
                       f"[{t.resolution_method}{', ' + version_label if version_label else ''}] --")
            out.append(analyzed["rendered"])
            summary = analyzed.get("summary")
            if summary and (summary["params_written"] or summary["params_read"]):
                out.append(f"   [reads: {', '.join(summary['params_read']) or '-'}; "
                           f"writes: {', '.join(summary['params_written']) or '-'}]")
            out.append("")

        if both or only["old"] or only["new"] or results["new"]["callers"]:
            out.append("==== Cross-function context ====")
            out.append("")
        for name, analyzed in both.items():
            emit_callee(name, analyzed, "")
        for version in ("old", "new"):
            for name, analyzed in only[version].items():
                emit_callee(name, analyzed, f"{version} version")

        for fn, sites in results["new"]["callers"].items():
            for a in sites:
                s = a["site"]
                out.append(f"-- caller of {fn}: {s.caller_name} — {s.rel_file}:{s.line + 1} --")
                out.append(a["rendered"])
                out.append("")

        if include_ring2:
            ring2 = {}
            for version in ("old", "new"):
                for name, entry in results[version]["ring2"].items():
                    ring2.setdefault(name, entry)  # identical defs: emit once
            if ring2:
                out.append("-- 2nd-level context (summaries) --")
                for name, entry in ring2.items():
                    t = entry["target"]
                    out.append(f"  {name} — {t.rel_file}:{t.line + 1} "
                               f"[{t.resolution_method}]: {t.signature}")
                    s = entry.get("summary")
                    if s:
                        out.append(f"    reads: {', '.join(s['params_read']) or '-'}; "
                                   f"writes: {', '.join(s['params_written']) or '-'}")
                out.append("")

        return "\n".join(out).rstrip() + ("\n" if out else "")

    @staticmethod
    def _to_json(results) -> dict:
        def tgt_json(analyzed):
            t = analyzed["target"]
            return {"name": t.name, "file": t.rel_file, "line": t.line + 1,
                    "is_macro": t.is_macro, "resolution_method": t.resolution_method,
                    "candidates_total": t.candidates_total,
                    "candidates_after_ts": t.candidates_after_ts,
                    "summary": analyzed.get("summary")}

        return {
            "stats": results["stats"],
            "old": {"callees": {k: tgt_json(v) for k, v in results["old"]["callees"].items()}},
            "new": {"callees": {k: tgt_json(v) for k, v in results["new"]["callees"].items()},
                    "callers": {fn: [{"caller": a["site"].caller_name,
                                      "file": a["site"].rel_file,
                                      "line": a["site"].line + 1}
                                     for a in sites]
                                for fn, sites in results["new"]["callers"].items()}},
        }
