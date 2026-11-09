"""Context for a point in the code (file + line) or for a named function, on
one repository snapshot. This is the shared implementation behind
`crossslice context`, the MCP tools `get_neighborhood` / `get_context_at` /
`get_type_definition`, and the editor integration. Everything here operates on
a RepoGraph and never expands rings: callees are summarized one by one, which
keeps a single request cheap on large trees."""
from __future__ import annotations

import contextlib
import copy
import json
import os
import re
import sys
from typing import Optional

from crossslice.cross.graph import RepoGraph, _content_hash
from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC

STD_TYPES = {"size_t", "ssize_t", "off_t", "time_t", "pid_t", "uid_t", "gid_t",
             "int8_t", "int16_t", "int32_t", "int64_t", "uint8_t", "uint16_t",
             "uint32_t", "uint64_t", "intptr_t", "uintptr_t", "ptrdiff_t",
             "wchar_t", "va_list", "FILE", "bool", "socklen_t", "mode_t", "dev_t",
             "ino_t", "loff_t", "clock_t", "sigset_t", "pthread_t", "pthread_mutex_t"}
TYPE_NODES = ("type_definition", "struct_specifier", "union_specifier",
              "enum_specifier", "preproc_def", "preproc_function_def", "declaration")
_IDENT_RE = re.compile(r"^[A-Za-z_]\w*$")


def _quiet():
    """Analysis chatter goes to stderr: stdout belongs to the result (CLI) or
    to the protocol (MCP)."""
    return contextlib.redirect_stdout(sys.stderr)


# ---------------------------------------------------------------- locating

def locate(graph: RepoGraph, rel_file: str, line: int) -> Optional[dict]:
    """The function definition containing 1-based `line` of `rel_file`
    (relative to the snapshot root): {name, kind, file, line (0-based start of
    the definition node, the graph's node key), end_line, signature}.
    None when the line is outside any function definition."""
    abs_file = os.path.join(graph.root, rel_file)
    if not os.path.isfile(abs_file):
        raise FileNotFoundError(f"{rel_file} does not exist in this snapshot")
    parser = SourceCodeParserC(abs_file)
    node = parser.find_function_containing_line(line - 1)
    if node is None:
        return None
    try:
        name = parser.get_function_name(node)
    except Exception:
        return None
    if not _IDENT_RE.match(name or ""):
        return None
    head = node.text.decode("utf-8", errors="replace").split("{")[0]
    signature = " ".join(part.strip() for part in head.split("\n") if part.strip())
    return {"name": name, "kind": "function", "file": rel_file,
            "line": node.start_point[0], "end_line": node.end_point[0],
            "signature": signature[:200]}


def ensure_node(graph: RepoGraph, name: Optional[str] = None,
                location: Optional[dict] = None):
    """(node, analysis, summary) for one function, analyzing it if needed and
    never expanding its ring. `location` (from locate()) pins a specific
    definition; otherwise the node already stored under `name` wins, otherwise
    the resolution cascade decides. Returns (None, None, None) if unresolved."""
    with _quiet():
        graph._ensure_gtags()
        node = None
        if location is not None:
            name = location["name"]
            row = graph.db.execute(
                "SELECT id FROM nodes WHERE name=? AND file=? AND line=?",
                (name, location["file"], location["line"])).fetchone()
            node = graph._node(row[0]) if row else None
        elif name:
            node = graph._find_node_by_name(name)
        node_id, analysis, summary = None, None, None
        if node is not None and node["state"] == "analyzed":
            row = graph.db.execute(
                "SELECT blob_hash, analysis, summary FROM nodes WHERE id=?",
                (node["id"],)).fetchone()
            current = row and row[0] == _content_hash(os.path.join(graph.root, node["file"]))
            if current and (row[1] or node["kind"] == "macro"):
                node_id = node["id"]
                analysis = json.loads(row[1]) if row[1] else None
                summary = json.loads(row[2]) if row[2] else None
        if node_id is None:
            if location is not None:
                node_id, analysis = graph._analyze_node(
                    name, location["file"], location["line"], "function",
                    location["signature"], "location")
            else:
                r = graph._resolve_name(name)
                if r is None:
                    return None, None, None
                node_id, analysis = graph._analyze_node(
                    name, r["rel_file"], r["line"],
                    "macro" if r["is_macro"] else "function",
                    r["signature"], r["resolution_method"])
                if r.get("alternatives"):
                    graph.db.execute("UPDATE nodes SET alternatives=? WHERE id=?",
                                     (json.dumps(r["alternatives"]), node_id))
            graph.db.commit()
            row = graph.db.execute("SELECT summary FROM nodes WHERE id=?", (node_id,)).fetchone()
            summary = json.loads(row[0]) if row and row[0] else None
    return graph._node(node_id), analysis, summary


# ---------------------------------------------------------------- facts about one function

def summary_of(graph: RepoGraph, name: str) -> dict:
    """Read/write/return summary of a function, or the #define of a macro."""
    node, _analysis, summary = ensure_node(graph, name=name)
    if node is None:
        return {"error": f"{name}: no in-repo definition"}
    base = {"name": name, "file": node["file"], "line": node["line"] + 1}
    if node["kind"] == "macro":
        return {**base, "kind": "macro", "signature": node["signature"] or ""}
    if summary is None:
        return {"error": f"{name}: no summary (not analyzable)"}
    return {**base, "kind": "function", **summary}


def callers_of(graph: RepoGraph, name: str, limit: int = 50) -> dict:
    """Callers of `name` from gtags references, each with its call-site line;
    `total_sites` says how many reference sites exist, `cap` how many were
    followed."""
    with _quiet():
        graph._ensure_gtags()
        found = graph.resolver.find_callers([name], graph.gtags, max_callers_per_fn=limit)
    total = getattr(graph.resolver, "last_caller_totals", {}).get(name, 0)
    return {"callers": [{"caller": c.caller_name, "file": c.rel_file, "line": c.line + 1}
                        for c in found.get(name, []) if c.caller_name],
            "total_sites": total, "cap": limit}


def function_source(graph: RepoGraph, node: dict) -> Optional[str]:
    """Verbatim text of a node's definition (function: tree-sitter span;
    macro: the #define and its continuation lines)."""
    abs_file = os.path.join(graph.root, node["file"])
    start, end = node["line"], None
    try:
        parser = SourceCodeParserC(abs_file)
        for _n, _name, s0, e0 in parser.collect_function_definitions():
            if s0 == start:
                end = e0
                break
        lines = open(abs_file, errors="replace").read().split("\n")
        if end is None and node["kind"] == "macro":
            end = start
            while end < len(lines) - 1 and lines[end].rstrip().endswith("\\"):
                end += 1
    except Exception:
        return None
    if end is None:
        return None
    return "\n".join(lines[start:end + 1])


def type_definition(graph: RepoGraph, name: str, max_lines: int = 80) -> dict:
    """Definition text of a struct/union/enum/typedef/macro/global by name:
    gtags tags them all; tree-sitter gives the exact span (a typedef'd struct
    is one node even when the tag sits on its closing line)."""
    with _quiet():
        graph._ensure_gtags()
        cands = graph.gtags.find_function_definition_detailed(name)
    best = None
    for c in cands[:8]:
        abs_file = c["file_path"]
        if not os.path.isabs(abs_file):
            abs_file = os.path.join(graph.root, abs_file)
        try:
            parser = SourceCodeParserC(abs_file)
            root = parser._tree.root_node
        except Exception:
            continue
        line0 = c["line_number"] - 1
        node = None
        stack = [root]
        while stack:                     # outermost type-ish node on the tag line
            n = stack.pop()
            # a node ending at column 0 of a line does not occupy that line
            end_row = n.end_point[0] - (1 if n.end_point[1] == 0
                                        and n.end_point[0] > n.start_point[0] else 0)
            if n.start_point[0] <= line0 <= end_row:
                if n.type in TYPE_NODES and re.search(
                        rf"\b{re.escape(name)}\b",
                        n.text.decode("utf-8", errors="replace")):
                    node = n
                    break
                stack.extend(reversed(n.children))
        if node is None:
            continue
        text = node.text.decode("utf-8", errors="replace")
        has_body = "{" in text
        cand = {"name": name, "file": os.path.relpath(abs_file, graph.root),
                "start_line": node.start_point[0] + 1,
                "end_line": node.end_point[0] + 1, "kind": node.type,
                "source": text, "has_body": has_body}
        if best is None or (has_body and not best["has_body"]):
            best = cand
        if has_body:
            break
    if best is None:
        return {"error": f"{name}: no type/macro/global definition"}
    lines = best["source"].split("\n")
    if len(lines) > max_lines:
        best["source"] = "\n".join(lines[:max_lines]) + f"\n... ({len(lines) - max_lines} more lines)"
    best.pop("has_body")
    return best


# ---------------------------------------------------------------- slicing from a point

def point_slice_text(analysis: dict, line: int, level: int = 2,
                     signature: Optional[str] = None) -> Optional[str]:
    """The def-use slice of a function around the statement at 1-based `line`
    (the innermost statement covering the line is the slicing criterion),
    rendered like the commit pipeline renders a callee; the seed is marked '>'."""
    from crossslice.intra.relevant_dataflow import find_relevant_dataflow
    from crossslice.cross.enrich import CrossFunctionEnricher
    stmts = copy.deepcopy(analysis.get("statements") or [])
    if len(stmts) < 2:
        return None
    line0 = line - 1
    body = [s for s in stmts[1:] if s.get("start")]
    covering = [s for s in body if s.get("end") and s["start"][0] <= line0 <= s["end"][0]]
    if covering:
        seed = min(covering, key=lambda s: (s["end"][0] - s["start"][0], -s["start"][0]))
    elif body:
        seed = min(body, key=lambda s: abs(s["start"][0] - line0))
    else:
        return None
    from crossslice.cross.enrich import _CONTROL_FLOW_TYPES
    for s in stmts:
        s["change_status"] = "matched"
    seed["change_status"] = "changed"
    if seed.get("type") in _CONTROL_FLOW_TYPES and seed.get("end"):
        # pointing at an `if`/loop header means its branches too: seed the
        # statements directly inside it (both branches of an if/else)
        depth = seed.get("scope_depth", seed.get("scope_level", 1))
        for s in body:
            if s is seed or not s.get("start"):
                continue
            if (seed["start"][0] <= s["start"][0] <= seed["end"][0]
                    and s.get("scope_depth", s.get("scope_level", 1)) <= depth + 1):
                s["change_status"] = "changed"
    find_relevant_dataflow(stmts, level=level)
    _close_defs(stmts)
    return CrossFunctionEnricher._render_sliced(stmts, mark_line=seed["start"][0], header=signature)


def _close_defs(stmts: list, hops: int = 2) -> None:
    """Pull in the definitions that the kept statements use (defs only, up to
    `hops` rounds) and the control-flow statements enclosing every kept
    statement, so a kept use never dangles (`for (i = 0; i < n; i++)` without
    `n = ...`) and no body statement appears without its header."""
    from crossslice.cross.enrich import _CONTROL_FLOW_TYPES
    body = stmts[1:]

    def defs(s):
        return {v.get("var_id") for v in s.get("left_side", []) if v.get("var_id")}

    def uses(s):
        return {v.get("var_id") for v in s.get("right_side", []) if v.get("var_id")}

    # a def inside an if/switch that does not contain the use is conditional:
    # keep looking for the unconditional one before it (declaration or assignment)
    conds = [(tuple(c["start"]), tuple(c["end"])) for c in body
             if c.get("type") in ("if_statement", "switch_statement", "case_statement")
             and c.get("start") and c.get("end")]

    def conditional(def_s, use_s):
        if not def_s.get("start") or not use_s.get("start"):
            return False
        d, u = tuple(def_s["start"]), tuple(use_s["start"])
        return any(a <= d <= b and not (a <= u <= b) for a, b in conds)

    for _ in range(hops):
        added = False
        for i, s in enumerate(body):
            if not s.get("relevant_to_dataflow"):
                continue
            for v in uses(s) - defs(s):          # `for (i = 0; i < n; i++)`: not i's own history
                taken = 0
                for t in reversed(body[:i]):
                    if v not in defs(t):
                        continue
                    if not t.get("relevant_to_dataflow"):
                        t["relevant_to_dataflow"] = True
                        added = True
                    taken += 1
                    if taken >= 4 or not conditional(t, s):
                        break               # the nearest unconditional def reaches the use
        if not added:
            break
    spans = [(tuple(c["start"]), tuple(c["end"]), c) for c in body
             if c.get("type") in _CONTROL_FLOW_TYPES and c.get("start") and c.get("end")]
    for s in body:
        if not s.get("relevant_to_dataflow") or not s.get("start"):
            continue
        p = tuple(s["start"])
        for a, b, c in spans:
            if c is not s and not c.get("relevant_to_dataflow") and a <= p <= b:
                c["relevant_to_dataflow"] = True


def sliced_body_text(analysis: dict, level: int = 2, signature: Optional[str] = None) -> Optional[str]:
    """The function reduced to the statements connected to its parameters and
    return values: the seeding the commit pipeline uses for a callee when no
    call site narrows it. Control-flow statements appear as headers."""
    from crossslice.intra.relevant_dataflow import find_relevant_dataflow
    from crossslice.cross.enrich import CrossFunctionEnricher
    stmts = copy.deepcopy(analysis.get("statements") or [])
    if len(stmts) < 2:
        return None
    param_ids = {p.get("var_id") for p in stmts[0].get("parameters", []) if p.get("var_id")}
    for s in stmts:
        s["change_status"] = "matched"
    for s in stmts[1:]:
        touched = {v.get("var_id") for v in s.get("left_side", []) + s.get("right_side", [])}
        if (touched & param_ids) or s.get("type") == "return_statement":
            s["change_status"] = "changed"
    find_relevant_dataflow(stmts, level=level)
    _close_defs(stmts)
    return CrossFunctionEnricher._render_sliced(stmts, header=signature)


def full_body_text(analysis: dict, signature: Optional[str] = None) -> Optional[str]:
    """Every statement of the function, one line each, control flow as headers."""
    from crossslice.cross.enrich import CrossFunctionEnricher
    stmts = copy.deepcopy(analysis.get("statements") or [])
    if len(stmts) < 2:
        return None
    for s in stmts[1:]:
        s["relevant_to_dataflow"] = True
    return CrossFunctionEnricher._render_sliced(stmts, header=signature)


# ---------------------------------------------------------------- the one-call context

def neighborhood_text(graph: RepoGraph, name: Optional[str] = None,
                      location: Optional[dict] = None, *, point_line: Optional[int] = None,
                      show_slice: bool = False, slice_level: int = 2,
                      max_callees: int = 30, max_callers: int = 8, max_types: int = 6):
    """Ring-1 context of a function as plain text: location and summary; the
    def-use slice around `point_line` (if `show_slice`); every callee as a
    one-line summary (macros as their #define); callers with the call-site
    source line (and a note when the cap truncated them); the project types
    the function uses. Returns {"error": ...} when the function is unknown."""
    from crossslice.cross.lsp_function_resolver import STANDARD_LIB_FUNCTIONS
    node, analysis, summary = ensure_node(graph, name=name, location=location)
    if node is None:
        return {"error": f"{name}: no in-repo definition"}
    name = node["name"]
    out = [f"{name} — {node['file']}:{node['line'] + 1} [{node['kind']}] "
           f"{node['signature'] or ''}".rstrip()]
    alts = node.get("alternatives") or []
    if alts:
        others = ", ".join(f"{a['file']}:{a['line'] + 1}" + (" [macro]" if a.get("is_macro") else "")
                           for a in alts[:8])
        out.append(f"  AMBIGUOUS: {len(alts) + 1} definitions of this name; this one was chosen by "
                   f"{node.get('resolution_method') or '?'}; others: {others}"
                   f"{f' (+{len(alts) - 8} more)' if len(alts) > 8 else ''}"
                   " — get_context_at(file, line) looks at another one")
    if summary:
        out.append(f"  reads: {', '.join(summary.get('params_read', [])) or '-'}; "
                   f"writes: {', '.join(summary.get('params_written', [])) or '-'}; "
                   f"returns: {' | '.join(summary.get('returns', [])) or '-'}")
    if node["kind"] == "macro":
        src = function_source(graph, node)
        if src:
            out.append(src)
        return "\n".join(out)

    if show_slice and point_line is not None and analysis:
        sl = point_slice_text(analysis, point_line, level=slice_level, signature=node.get("signature"))
        if sl:
            out.append(f"\nSLICE around line {point_line} (def-use, level {slice_level}; '>' marks the seed):")
            out.append(sl)

    names, seen, with_args = [], set(), set()
    for st in (analysis or {}).get("statements", []):
        for c in st.get("calls_info", []):
            cname = c.get("function_name", "")
            if c.get("arguments"):
                with_args.add(cname)
            if (not _IDENT_RE.match(cname) or cname == name
                    or cname in STANDARD_LIB_FUNCTIONS or cname in seen):
                continue
            seen.add(cname)
            names.append(cname)
    # classify every callee first, then cap: project functions get the budget
    # before macros, and names without a definition in the repository go on one
    # line and never displace a real one
    functions, macros, external = [], [], []
    for cname in names[:80]:
        sm = summary_of(graph, cname)
        if "error" in sm:
            external.append(cname)
            continue
        n_defs = len((graph._find_node_by_name(cname) or {}).get("alternatives") or []) + 1
        amb = f" (1 of {n_defs} definitions)" if n_defs > 1 else ""
        if sm.get("kind") == "macro":
            sig = sm.get("signature", "")
            from crossslice.cross.enrich import is_type_macro
            if cname in with_args and is_type_macro(sig):
                continue                        # a type macro in a cast, not a call
            macros.append(f"  {cname} [macro{amb}]: {sig[:200]}")
        else:
            functions.append(f"  {cname} ({sm['file']}:{sm['line']}{amb}): "
                             f"reads {', '.join(sm.get('params_read', [])) or '-'}; "
                             f"writes {', '.join(sm.get('params_written', [])) or '-'}; "
                             f"returns {' | '.join(sm.get('returns', [])) or '-'}")
    shown_fn = functions[:max_callees]
    shown_mc = macros[:max(0, max_callees - len(shown_fn))]
    hidden = [l.strip().split(" ")[0] for l in functions[len(shown_fn):] + macros[len(shown_mc):]]
    hidden += names[80:]
    out.append(f"\nCALLEES ({len(names)}):")
    out.extend(shown_fn)
    out.extend(shown_mc)
    if external:
        out.append(f"  not defined in this repository: {', '.join(external)}")
    if hidden:
        out.append(f"  not shown ({len(hidden)}): {', '.join(hidden)}")

    cl = callers_of(graph, name, max_callers)
    out.append(f"\nCALLERS ({len(cl['callers'])}):")
    for c in cl["callers"]:
        try:
            src_line = open(os.path.join(graph.root, c["file"]), errors="replace") \
                .read().split("\n")[c["line"] - 1].strip()
        except Exception:
            src_line = ""
        out.append(f"  {c['caller']} ({c['file']}:{c['line']}): {src_line[:200]}")
    if cl["total_sites"] > cl["cap"]:
        out.append(f"  ... only the first {cl['cap']} of {cl['total_sites']} reference sites "
                   f"were followed")

    src = function_source(graph, node) or ""
    tnames, tseen = [], set()
    for m in re.finditer(r"\b(?:struct|union|enum)\s+([A-Za-z_]\w*)|\b([A-Za-z_]\w*_t)\b", src):
        t = m.group(1) or m.group(2)
        if t in tseen or t in STD_TYPES or t == name:
            continue
        tseen.add(t)
        tnames.append(t)
    types_out = []
    for t in tnames:
        if len(types_out) >= max_types:
            break
        d = type_definition(graph, t, max_lines=200)
        if "source" in d and "{" in d["source"]:
            # comments stripped: a kernel/FFmpeg struct is mostly doc text
            src_t = re.sub(r"/\*.*?\*/", "", d["source"], flags=re.S)
            src_t = re.sub(r"//[^\n]*", "", src_t)
            body_lines = [l for l in src_t.split("\n") if l.strip()][:40]
            body = "\n".join("    " + l for l in body_lines)
            types_out.append(f"  {t} — {d['file']}:{d['start_line']}\n{body}")
    if types_out:
        out.append(f"\nTYPES ({len(types_out)}):")
        out.extend(types_out)
    return "\n".join(out)


def context_at(graph: RepoGraph, rel_file: str, line: int, *, show_slice: bool = True,
               **kw):
    """neighborhood_text() for the function containing FILE:LINE."""
    loc = locate(graph, rel_file, line)
    if loc is None:
        return {"error": f"{rel_file}:{line} is not inside a function definition"}
    return neighborhood_text(graph, location=loc, point_line=line, show_slice=show_slice, **kw)
