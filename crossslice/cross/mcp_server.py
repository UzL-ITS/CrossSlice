"""
MCP server exposing on-demand code and commit context as typed tools.

Built with the official MCP Python SDK (FastMCP). An LLM agent connects over
stdio and pulls exactly the context it needs.

Two modes:
  * working tree (default, `crossslice mcp` inside a checkout): the symbol
    tools answer for the files on disk (version="work"); the commit tools take
    a `rev` (default HEAD) and compare it with its parent ("old" / "new").
  * commit scope (`--commit <rev>`): the server is about one commit; `version`
    defaults to "new" and `rev` defaults to that commit. This is the setting of
    the paper's agent experiments.
Outside a git repository only version="work" is available.

Tools (see each tool's docstring for the contract):
  get_commit_overview(rev)                  changed files + changed functions
  get_raw_diff(rev)                         the plain unified diff (-U3)
  get_intra_diff(rev)                       def/use (GumTree) enriched diff:
                                            the change + its intra-procedural
                                            data-flow slice
  list_changed_functions(rev)               names of the functions the commit
                                            touches (where to start)
  resolve_symbol(name, version)             where a function/macro is defined
  get_sliced_body(name, version)            def-use-sliced body of a function
  get_summary(name, version)                reads/writes/returns summary
  get_callers(name, version, limit)         who calls it (with call sites)
  expand_function(name, version, levels)    its callees + callers (graph ring)
  get_function_source(name, version)        verbatim source of a definition,
                                            with line numbers (for patching)
  get_neighborhood(name, version)           ONE call: callee summaries, macro
                                            defs, callers + call sites, types
  get_type_definition(name, version)        struct/union/enum/typedef/macro/
                                            global definition text

`version` is "work" (the files on disk), "old" (the parent of `rev`) or "new"
(`rev` itself); the default is "new" under --commit and "work" otherwise.

`--lock-version old|new` restricts the server to ONE version: the diff/overview
tools are disabled and every `version` argument must equal the lock. This is
what the fix-task experiment (eval/agent_probe.py fix) uses so an agent asked
to repair the pre-commit code cannot read the actual fix.

Run:
  crossslice mcp                               # working tree of the current repo
  crossslice mcp -C data/repos/ffmpeg --commit <SHA>

Register with an MCP client, e.g. Claude Code (from inside the repository):
  claude mcp add crossslice -- crossslice mcp
"""

import argparse
import contextlib
import io
import json
import os
import subprocess
import sys
from typing import Literal


from mcp.server.fastmcp import FastMCP

from crossslice.cross.graph import RepoGraph
from crossslice.paths import NO_GIT, MissingTool, find_workspace

MAX_CHARS = 20000  # budget guard: never return more than this in one result
RING_CAP = 60      # nodes listed per expansion ring (the rest is counted)

# The def-use slicer is C-only; these extensions mark files where deep analysis
# (slicing / summaries / expansion) is unsupported and should fast-fail.
_CPP_EXT = (".cxx", ".cpp", ".cc", ".c++", ".hpp", ".hh", ".hxx")

Version = Literal["work", "old", "new"]


class ToolError(Exception):
    """A user-facing failure: its message is returned to the agent verbatim."""


def _clip(text: str) -> str:
    if text and len(text) > MAX_CHARS:
        return text[:MAX_CHARS] + "\n... [truncated to budget] ..."
    return text


def _dump(obj) -> str:
    return _clip(obj if isinstance(obj, str)
                 else json.dumps(obj, indent=2, default=str))


def _logged(fn):
    """Log every tool call (args, duration, outcome) to stderr and turn an
    exception into an error result — so a slow or failing call is visible in
    the server log instead of being a silent gap on the client side."""
    import functools
    import time
    import traceback

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        t0 = time.time()
        argstr = ", ".join(f"{k}={str(v)[:40]}" for k, v in kwargs.items())
        try:
            out = fn(*args, **kwargs)
            print(f"[mcp] {fn.__name__}({argstr}) ok {time.time() - t0:.1f}s "
                  f"{len(out) if isinstance(out, str) else 0} chars",
                  file=sys.stderr, flush=True)
            return out
        except (ToolError, MissingTool) as e:
            print(f"[mcp] {fn.__name__}({argstr}) declined {time.time() - t0:.1f}s: {e}",
                  file=sys.stderr, flush=True)
            return _dump({"error": str(e)})
        except Exception as e:
            print(f"[mcp] {fn.__name__}({argstr}) ERROR {time.time() - t0:.1f}s "
                  f"{type(e).__name__}: {e}\n{traceback.format_exc()}",
                  file=sys.stderr, flush=True)
            return _dump({"error": f"{fn.__name__} failed: {type(e).__name__}: {e}"})
    return wrapper


class CommitContext:
    """Lazily-built context for one commit, over both its versions — or, with
    sha=None, for the working tree only. The working-tree graph ("work") is
    owned by the Session and shared by all commit contexts."""

    def __init__(self, repo_path: str, sha: str | None, session: "Session | None" = None,
                 cache_dir: str | None = None, git_root: str | None = None):
        self.repo = os.path.abspath(repo_path)            # analysis root (graphs)
        self.git_root = os.path.abspath(git_root or repo_path)  # diffs
        self.sha = sha
        self.session = session
        self.cache_dir = cache_dir
        self.prev = self._parent(sha) if sha else None
        self._graphs: dict[str, RepoGraph] = {}
        self._raw = None
        self._intra = None
        self._changed = None  # {"files": [...], "functions": [...]}

    def _parent(self, sha):
        """The first parent; for a root commit git's empty tree, so the diff
        tools show everything as added (there is no old version to analyze)."""
        from crossslice.commit import EMPTY_TREE
        out = subprocess.run(["git", "rev-parse", "--verify", "-q", f"{sha}^"], cwd=self.repo,
                             capture_output=True, text=True)
        return out.stdout.strip() if out.returncode == 0 and out.stdout.strip() else EMPTY_TREE

    @property
    def is_root(self):
        from crossslice.commit import EMPTY_TREE
        return self.prev == EMPTY_TREE

    # ---- version graphs -----------------------------------------------------

    def graph(self, version: str) -> RepoGraph:
        if version == "work":
            if self.session is None:
                raise ToolError("version='work' is not available in this server")
            return self.session.work_graph()
        if self.sha is None:
            raise ToolError(f"version={version!r} needs a commit; this context is the working tree")
        if version == "old" and self.is_root:
            raise ToolError(f"{self.sha[:12]} is the root commit: it has no old version "
                            "(every function is new; use version=\"new\")")
        key = "new" if version == "new" else "old"
        if key not in self._graphs:
            commit = self.sha if key == "new" else self.prev
            # Keep pipeline chatter off stdout — the MCP protocol owns it.
            with contextlib.redirect_stdout(sys.stderr):
                self._graphs[key] = RepoGraph(self.repo, commit=commit,
                                              cache_dir=self.cache_dir)
        return self._graphs[key]

    # ---- diff / intra (built once) -----------------------------------------

    def _build_diff(self):
        if self._raw is not None:
            return
        if self.sha is None:
            raise ToolError("no commit selected")
        from crossslice.intra.github_loader import get_changed_files
        from crossslice.intra.data_diff import create_diff
        from crossslice.intra.parse_diff import parse_diff
        from crossslice.intra.gen_dataflow import gen_dataflow
        from crossslice.intra.github_loader import extract_file_from_commit

        import shutil
        import tempfile
        # per-process scratch: a shared directory would be wiped by any other
        # server / case loader running at the same time
        work = tempfile.mkdtemp(prefix="cce_mcp_")
        old_dir = os.path.join(work, "old_version")
        new_dir = os.path.join(work, "new_version")
        os.makedirs(old_dir)
        os.makedirs(new_dir)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                files = [f for f in get_changed_files(self.git_root, self.prev, self.sha)
                         if f.endswith((".c", ".h"))]
                for f in files:
                    extract_file_from_commit(self.git_root, self.prev, f,
                                             os.path.join(old_dir, f))
                    extract_file_from_commit(self.git_root, self.sha, f,
                                             os.path.join(new_dir, f))
                diff = create_diff(old_dir, new_dir, files)
                changes = parse_diff(diff, work, old_dir, new_dir,
                                     use_hungarian=True, debug_matching=False)
                intra, _ = gen_dataflow(changes, old_dir, new_dir, level=2,
                                        collect_internals=True)
            self._raw = subprocess.run(
                ["git", "diff", "-U3", self.prev, self.sha, "--", *files],
                cwd=self.git_root, capture_output=True, text=True,
                errors="replace").stdout
            self._intra = intra or ""
            fns = sorted({name for d in changes.values()
                          for name in d.get("functions", {})
                          if not name.startswith("__")})  # drop synthetic scopes
            self._changed = {"files": files, "functions": fns}
            if self.is_root:
                self._changed["note"] = ("root commit: compared with the empty tree, so every "
                                         "file and function is new")
            if any(f.endswith(_CPP_EXT) for f in files):
                self._changed["note"] = (
                    "This commit touches C++ files. Deep analysis tools "
                    "(get_sliced_body / get_summary / expand_function) support C "
                    "only and will decline on C++ symbols; rely on get_raw_diff, "
                    "get_intra_diff, resolve_symbol, and get_callers here.")
        finally:
            shutil.rmtree(work, ignore_errors=True)

    def raw_diff(self):
        self._build_diff()
        return self._raw

    def intra_diff(self):
        self._build_diff()
        return self._intra

    def changed(self):
        self._build_diff()
        return self._changed

    # ---- symbol tools (operate on a chosen version graph) ------------------

    def resolve(self, name, version):
        with contextlib.redirect_stdout(sys.stderr):
            r = self.graph(version)._resolve_name(name)
        if not r:
            with contextlib.redirect_stdout(sys.stderr):
                g = self.graph(version)
                g._ensure_gtags()
                sugg = g.gtags.suggest(name)
            return {"resolved": False, "name": name, "version": version,
                    "reason": "no in-repo definition or unverifiable",
                    **({"did_you_mean": sugg} if sugg else {})}
        out = {"resolved": True, "name": name, "version": version,
               "file": r["rel_file"], "line": r["line"] + 1,
               "kind": "macro" if r["is_macro"] else "function",
               "signature": r["signature"],
               "resolution_method": r["resolution_method"]}
        alts = r.get("alternatives") or []
        if alts:
            out.update({
                "ambiguous": True, "definitions": len(alts) + 1,
                "alternatives": [{"file": a["file"], "line": a["line"] + 1,
                                  "kind": "macro" if a.get("is_macro") else "function"}
                                 for a in alts[:10]],
                "hint": "several definitions share this name; the chosen one is ranked by "
                        "resolution_method (functions over macros, real code over stubs). "
                        "get_context_at(file, line) looks at another definition."})
        else:
            out["ambiguous"] = False
        return out

    def _cpp_guard(self, name, version):
        """The def-use slicer uses a tree-sitter-C + GumTree pipeline that does
        not handle C++; short-circuit (instead of hanging) when a symbol lives
        in a C++ file, with an actionable message."""
        with contextlib.redirect_stdout(sys.stderr):
            r = self.graph(version)._resolve_name(name)
        if r and str(r["rel_file"]).endswith(_CPP_EXT):
            return {"error": f"{name} is defined in a C++ file ({r['rel_file']}). "
                    "Deep analysis (sliced body / summary / expand) supports C "
                    "only. Use get_raw_diff, get_intra_diff, resolve_symbol, or "
                    "get_callers for this commit instead.",
                    "language": "c++"}
        return None

    def _analyzed(self, name, version):
        """Statement IR + mod/ref summary of one function: reuse the cached
        analyzed node when current, else resolve and analyze just this node.
        Deliberately does NOT materialize its callees (expand does that):
        resolving a ring costs gtags + tree-sitter + possibly clangd per callee,
        which made a single summary request take minutes on large trees."""
        g = self.graph(version)
        with contextlib.redirect_stdout(sys.stderr):
            g._ensure_gtags()
            node = g._find_node_by_name(name)
            node_id = None
            if node and node["state"] == "analyzed":
                from crossslice.cross.graph import _content_hash
                row = g.db.execute("SELECT blob_hash, analysis FROM nodes WHERE id=?",
                                   (node["id"],)).fetchone()
                if row and row[1] and row[0] == _content_hash(
                        os.path.join(g.root, node["file"])):
                    node_id = node["id"]
            if node_id is None:
                r = g._resolve_name(name)
                if r is None:
                    return None, None
                node_id, _ = g._analyze_node(
                    name, r["rel_file"], r["line"],
                    "macro" if r["is_macro"] else "function",
                    r["signature"], r["resolution_method"])
                g.db.commit()
        row = g.db.execute("SELECT analysis, summary FROM nodes WHERE id=?",
                           (node_id,)).fetchone()
        analysis = json.loads(row[0]) if row and row[0] else None
        summary = json.loads(row[1]) if row and row[1] else None
        return analysis, summary

    def sliced_body(self, name, version):
        guard = self._cpp_guard(name, version)
        if guard:
            return guard
        analysis, summary = self._analyzed(name, version)
        if not analysis:
            return {"error": f"{name}: no analyzable definition in {version} version"}
        from crossslice.cross.context import sliced_body_text
        node = self.graph(version)._find_node_by_name(name) or {}
        return {"name": name, "version": version, "summary": summary,
                "body": sliced_body_text(analysis, signature=node.get("signature")) or ""}

    def summary(self, name, version):
        guard = self._cpp_guard(name, version)
        if guard:
            return guard
        _, summary = self._analyzed(name, version)
        if summary is None:
            r = self.graph(version)._resolve_name(name)
            if r and r["is_macro"]:
                return {"name": name, "version": version, "kind": "macro",
                        "signature": r["signature"]}
            return {"error": f"{name}: no summary in {version} version"}
        return {"name": name, "version": version, **summary}

    def callers(self, name, version, limit):
        g = self.graph(version)
        with contextlib.redirect_stdout(sys.stderr):
            g._ensure_gtags()
            found = g.resolver.find_callers([name], g.gtags, max_callers_per_fn=limit)
        return {"name": name, "version": version, "callers": [
            {"caller": c.caller_name, "file": c.rel_file, "line": c.line + 1}
            for c in found.get(name, []) if c.caller_name]}

    def expand(self, name, version, levels):
        guard = self._cpp_guard(name, version)
        if guard:
            return guard
        g = self.graph(version)
        levels = max(1, min(int(levels), 3))
        with contextlib.redirect_stdout(sys.stderr):
            g.expand(name, direction="both", levels=levels)
            hood = g.neighborhood(name)
        if not hood:
            return {"error": f"{name}: could not resolve in {version} version"}

        def row(n, **extra):  # 1-based lines, like every other tool
            d = {"name": n["name"], "file": n["file"], "line": n["line"] + 1,
                 "kind": n["kind"], "state": n["state"]}
            d.update(extra)
            return d

        def site(n):
            cl = n.get("call_line")
            return {"call_line": cl + 1} if cl is not None else {}

        def grouped(entries):  # one entry per definition, with every call site
            by_key = {}
            for c in entries:
                key = (c["name"], c["file"], c["line"])
                d = by_key.setdefault(key, row(c, call_lines=[]))
                if c.get("call_line") is not None and c["call_line"] + 1 not in d["call_lines"]:
                    d["call_lines"].append(c["call_line"] + 1)
            for d in by_key.values():
                d["call_lines"].sort()
            return list(by_key.values())

        node = hood["node"]
        out = {"name": name, "version": version, "levels": levels, "node": row(node),
               "callees": grouped(hood["callees"]),
               "callers": grouped(hood["callers"])}
        alts = node.get("alternatives") or []
        if alts:
            out["node"]["ambiguous"] = True
            out["node"]["definitions"] = len(alts) + 1
            out["node"]["alternatives"] = [f"{a['file']}:{a['line'] + 1}" for a in alts[:10]]
        if levels > 1:
            # rings 2..n are listed compactly ("name file:line via direction"),
            # capped per ring: a level-3 ring on a large project has hundreds of nodes
            out["rings"] = self._rings(g, node["id"], levels)
            out["rings_format"] = ("name file:line <- via (callee of via) | name file:line -> via "
                                   "(caller of via); ordered: callers of callers, callees of callees, "
                                   "then the rest; at most 10 per via")
        return out

    @staticmethod
    def _rings(g, start_id, levels):
        """Ring k: nodes first reached at distance k (callees and callers), as
        one short string each, capped at RING_CAP per ring."""
        # The chains that matter come first: who calls my callers (upward) and
        # what my callees call (downward). Callers of a callee are mostly hub
        # noise (every caller of a bit reader) and come last, 10 per via.
        PER_VIA = 10
        order = {("caller", "caller"): 0, ("callee", "callee"): 1,
                 ("caller", "callee"): 2, ("callee", "caller"): 3}
        seen, rings = {start_id}, []
        frontier = [(start_id, None)]          # (node id, direction it was reached by)
        for level in range(1, levels + 1):
            found, nxt = [], []
            for nid, d1 in frontier:
                via = g._node(nid)["name"]
                per_via = 0
                neighbors = ([(dst, "callee") for dst, in g.db.execute(
                                 "SELECT DISTINCT dst FROM edges WHERE src=?", (nid,))]
                             + [(src, "caller") for src, in g.db.execute(
                                 "SELECT DISTINCT src FROM edges WHERE dst=?", (nid,))])
                for other, d2 in neighbors:
                    if other in seen:
                        continue
                    seen.add(other)
                    nxt.append((other, d2 if d1 is None else d1))
                    n = g._node(other)
                    cat = 0 if d1 is None else order[(d1, d2)]
                    arrow = "<-" if d2 == "callee" else "->"
                    found.append((cat, via, per_via >= PER_VIA, n["name"],
                                  f"{n['name']} {n['file']}:{n['line'] + 1} {arrow} {via}"))
                    per_via += 1
            found.sort(key=lambda t: (t[2], t[0], t[1], t[3]))
            listed = [t[4] for t in found[:RING_CAP]]
            entry = {"level": level, "count": len(found), "nodes": listed}
            if len(found) > RING_CAP:
                entry["note"] = (f"{len(found) - RING_CAP} more not listed; get_callers or "
                                 "expand_function on a node of interest instead")
            rings.append(entry)
            frontier = nxt
            if not nxt:
                break
        return rings

    def function_source(self, name, version):
        """Verbatim definition text (function or macro) with 1-based line
        numbers, so an agent can quote exact lines when it writes a patch."""
        with contextlib.redirect_stdout(sys.stderr):
            r = self.graph(version)._resolve_name(name)
        if not r:
            return {"error": f"{name}: no in-repo definition in {version} version"}
        from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
        abs_file = os.path.join(self.graph(version).root, r["rel_file"])
        start, end = r["line"], None
        try:
            parser = SourceCodeParserC(abs_file)
            for node, _fname, s0, e0 in parser.collect_function_definitions():
                if s0 == start:
                    end = e0
                    break
            if end is None and r["is_macro"]:
                # object-like or unparsed macro: #define line + continuations
                lines = open(abs_file, errors="replace").read().split("\n")
                end = start
                while end < len(lines) - 1 and lines[end].rstrip().endswith("\\"):
                    end += 1
        except Exception as e:  # pragma: no cover - defensive
            return {"error": f"{name}: could not parse {r['rel_file']}: {e}"}
        if end is None:
            return {"error": f"{name}: definition span not found in {r['rel_file']}"}
        lines = open(abs_file, errors="replace").read().split("\n")[start:end + 1]
        numbered = "\n".join(f"{start + 1 + i:5d}| {l}" for i, l in enumerate(lines))
        return {"name": name, "version": version, "file": r["rel_file"],
                "start_line": start + 1, "end_line": end + 1,
                "kind": "macro" if r["is_macro"] else "function",
                "source": numbered}

    # ---- types and one-call neighborhood ------------------------------------

    def type_definition(self, name, version, max_lines=80):
        from crossslice.cross.context import type_definition
        r = type_definition(self.graph(version), name, max_lines=max_lines)
        if "error" in r:
            return {"error": f"{name}: no type/macro/global definition in {version} version"}
        return {"version": version, **r}

    def neighborhood(self, name, version, max_callees=30, max_callers=8, max_types=6):
        """One-call ring-1 context for a function (shared implementation in
        crossslice.cross.context; the tool wrapper clips it to the budget)."""
        from crossslice.cross.context import neighborhood_text
        r = neighborhood_text(self.graph(version), name=name, max_callees=max_callees,
                              max_callers=max_callers, max_types=max_types)
        if isinstance(r, dict):
            return {"error": f"{name}: no in-repo definition in {version} version"}
        return r

    def context_at(self, file, line, version, show_slice=True):
        """Context for FILE:LINE (file relative to the repository root)."""
        from crossslice.cross.context import context_at
        try:
            r = context_at(self.graph(version), file, int(line), show_slice=show_slice)
        except FileNotFoundError as e:
            return {"error": f"{e} ({version} version)"}
        if isinstance(r, dict):
            return {"error": f"{file}:{line} is not inside a function definition in the {version} version"}
        return r

    def close(self):
        for g in self._graphs.values():
            g.close()


# ------------------------------- session -----------------------------------

class Session:
    """Everything one server process serves: the working tree of `repo`, and
    one CommitContext per commit asked about (built on first use)."""

    def __init__(self, repo: str, git_root: str | None, commit: str | None = None,
                 cache_dir: str | None = None):
        self.repo = os.path.abspath(repo)
        self.git_root = git_root
        self.is_git = git_root is not None
        self.commit = commit          # --commit: the commit this server is scoped to
        self.cache_dir = cache_dir
        self._work: RepoGraph | None = None
        self._work_ctx = CommitContext(self.repo, None, self, cache_dir)
        self._commits: dict[str, CommitContext] = {}

    @property
    def default_version(self) -> str:
        return "new" if self.commit else "work"

    def work_graph(self) -> RepoGraph:
        if self._work is None:
            with contextlib.redirect_stdout(sys.stderr):
                self._work = RepoGraph(self.repo, cache_dir=self.cache_dir)
        return self._work

    def commit_ctx(self, rev: str | None = None) -> CommitContext:
        """The CommitContext for `rev` (default: --commit, else HEAD)."""
        if not self.is_git:
            raise ToolError(f"{NO_GIT}. Use version=\"work\" with the symbol tools.")
        rev = (rev or "").strip() or self.commit or "HEAD"
        out = subprocess.run(["git", "rev-parse", "--verify", "-q", f"{rev}^{{commit}}"],
                             cwd=self.repo, capture_output=True, text=True)
        sha = out.stdout.strip()
        if out.returncode != 0 or not sha:
            raise ToolError(f"{rev!r} is not a commit in this repository")
        if sha not in self._commits:
            self._commits[sha] = CommitContext(self.repo, sha, self, self.cache_dir,
                                               git_root=self.git_root)
        return self._commits[sha]

    def ctx(self, version: str, rev: str | None = None) -> CommitContext:
        return self._work_ctx if version == "work" else self.commit_ctx(rev)

    def close(self):
        for c in self._commits.values():
            c.close()
        self._commits.clear()
        if self._work is not None:
            self._work.close()
            self._work = None


# --------------------------- FastMCP tool surface --------------------------

mcp = FastMCP("crossslice")
SESSION: Session | None = None  # set in main() before mcp.run()
LOCK: str | None = None         # "old" / "new": restrict the server to one version


def _locked_diff_tool(tool):
    if LOCK:
        return _dump({"error": f"{tool} is not available: this server is locked "
                      f"to the '{LOCK}' version of the code (no diff / other "
                      "version). Use resolve_symbol, get_function_source, "
                      "get_sliced_body, get_summary, get_callers, expand_function "
                      f"with version=\"{LOCK}\"."})
    return None


def _target(version, rev=None):
    """(CommitContext, version) for a symbol tool. Under a lock every symbol
    tool answers for the locked version of the server's commit, whatever the
    caller passed (a small model omitting the argument should not be punished
    with an error)."""
    if LOCK:
        return SESSION.commit_ctx(None), LOCK
    version = version or SESSION.default_version
    return SESSION.ctx(version, rev), version


def _commit(rev):
    return SESSION.commit_ctx(None if LOCK else rev)




@mcp.tool()
@_logged
def get_commit_overview(rev: str | None = None) -> str:
    """List the C/H files a commit changes and the functions it touches.
    The starting point: call this first to see what changed, then drill in.
    `rev` is any git revision (default: the server's commit, else HEAD)."""
    err = _locked_diff_tool("get_commit_overview")
    if err:
        return err
    ctx = _commit(rev)
    c = ctx.changed()
    return _dump({"commit": ctx.sha, "parent": None if ctx.is_root else ctx.prev,
                  "changed_files": c["files"], "changed_functions": c["functions"],
                  **({"note": c["note"]} if c.get("note") else {})})


@mcp.tool()
@_logged
def get_raw_diff(rev: str | None = None) -> str:
    """Return the plain unified diff of a commit (git diff -U3). The minimal
    view: the changed lines with three lines of surrounding context.
    `rev` is any git revision (default: the server's commit, else HEAD)."""
    err = _locked_diff_tool("get_raw_diff")
    if err:
        return err
    return _dump(_commit(rev).raw_diff())


@mcp.tool()
@_logged
def get_intra_diff(rev: str | None = None) -> str:
    """Return the def/use (GumTree) enriched diff: the change merged with its
    intra-procedural data-flow slice — every statement inside the changed
    functions that defines or uses a variable the change touches. Shows *why*
    the changed lines matter within their function, without cross-function noise.
    `rev` is any git revision (default: the server's commit, else HEAD)."""
    err = _locked_diff_tool("get_intra_diff")
    if err:
        return err
    return _dump(_commit(rev).intra_diff())


@mcp.tool()
@_logged
def list_changed_functions(rev: str | None = None) -> str:
    """Return just the names of the functions a commit modifies — the natural
    seeds for resolve_symbol / get_sliced_body / expand_function.
    `rev` is any git revision (default: the server's commit, else HEAD)."""
    err = _locked_diff_tool("list_changed_functions")
    if err:
        return err
    return _dump(_commit(rev).changed()["functions"])


# Every symbol tool takes `version` ("work": the files on disk; "old": the
# parent of `rev`; "new": `rev` itself; default "new" when the server is scoped
# to a commit, else "work") and `rev` (only used for old/new).

@mcp.tool()
@_logged
def resolve_symbol(name: str, version: Version | None = None, rev: str | None = None) -> str:
    """Resolve a C function or macro to its definition (file, line, kind,
    signature, resolution method) via the gtags->tree-sitter->clangd cascade.
    Use before asking for a body. `version`: "work" (files on disk), "old"
    (parent of `rev`) or "new" (`rev`); `rev` defaults to the server's commit,
    else HEAD."""
    ctx, version = _target(version, rev)
    return _dump(ctx.resolve(name, version))


@mcp.tool()
@_logged
def get_sliced_body(name: str, version: Version | None = None, rev: str | None = None) -> str:
    """Return a function's body reduced by def-use slicing to the statements
    connected to its parameters and return values ("..." marks what was left
    out; control flow appears as headers), plus its reads/writes summary.
    Compare a callee's "old" and "new" bodies to see what a fix changed inside
    it. `version`: "work" (files on disk), "old" (parent of `rev`) or "new"
    (`rev`)."""
    ctx, version = _target(version, rev)
    r = ctx.sliced_body(name, version)
    if "body" not in r:
        return _dump(r)
    sm = r.get("summary") or {}
    head = (f"{name} ({version} version) — def-use-sliced body; "
            f"reads: {', '.join(sm.get('params_read', [])) or '-'}; "
            f"writes: {', '.join(sm.get('params_written', [])) or '-'}; "
            f"returns: {' | '.join(sm.get('returns', [])) or '-'}")
    return _clip(head + "\n" + r["body"])


@mcp.tool()
@_logged
def get_summary(name: str, version: Version | None = None, rev: str | None = None) -> str:
    """Return only the side-effect summary of a function: which parameters it
    reads, which it writes through pointers (marked *), and its return
    expressions. The cheapest way to learn what a callee does. `version`:
    "work" (files on disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    return _dump(ctx.summary(name, version))


@mcp.tool()
@_logged
def get_callers(name: str, version: Version | None = None, limit: int = 50,
                rev: str | None = None) -> str:
    """List functions that call the given function, with call-site file and
    line. Use to see how a change propagates — e.g. whether callers pass
    attacker-controlled data into a newly bounds-checked argument. `version`:
    "work" (files on disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    return _dump(ctx.callers(name, version, limit))


def _dump_compact(obj) -> str:
    """JSON without pretty-printing, for results that would otherwise be clipped."""
    return _clip(json.dumps(obj, separators=(",", ":"), default=str))


@mcp.tool()
@_logged
def expand_function(name: str, version: Version | None = None, levels: int = 1,
                    rev: str | None = None) -> str:
    """Materialize a function's neighborhood in the on-demand graph and return
    its direct callees and callers (1-based lines, call sites); levels>1 (max 3)
    adds `rings`: the nodes first reached at distance 2, 3 with the node they
    were reached through. The primary navigation tool. `version`: "work" (files
    on disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    r = ctx.expand(name, version, levels)
    return _dump(r) if levels <= 1 else _dump_compact(r)


@mcp.tool()
@_logged
def get_function_source(name: str, version: Version | None = None,
                        rev: str | None = None) -> str:
    """Return the verbatim source of a function or macro definition, with file
    path and 1-based line numbers. Use this when you need exact lines (e.g. to
    write a patch); prefer get_sliced_body / get_summary when you only need to
    understand what a function does. `version`: "work" (files on disk), "old"
    (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    r = ctx.function_source(name, version)
    if "source" not in r:
        return _dump(r)
    return _clip(f"{name} ({r['kind']}, {version} version) — "
                 f"{r['file']}:{r['start_line']}-{r['end_line']}\n{r['source']}")


@mcp.tool()
@_logged
def get_neighborhood(name: str, version: Version | None = None, rev: str | None = None) -> str:
    """ONE call for a function's ring-1 context: its location and
    read/write/return summary; every callee as a one-line summary (macros as
    their #define); every caller with the call-site source line; and the
    definitions of the project struct/typedef types it uses. Start here — it
    replaces a dozen resolve/summary/callers calls. `version`: "work" (files on
    disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    return _dump(ctx.neighborhood(name, version))


@mcp.tool()
@_logged
def get_context_at(file: str, line: int, version: Version | None = None,
                   rev: str | None = None) -> str:
    """Context for a POINT in the code: the function containing `line` (1-based)
    of `file` (path relative to the repository root) — its read/write summary,
    the def-use slice around that line ('>' marks the seed), its callees as
    one-line summaries, its callers with call-site lines, and the project types
    it uses. Use it when you know where you are (a diff hunk, a stack frame, an
    editor position) but not what the function is called. `version`: "work"
    (files on disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    return _dump(ctx.context_at(file, int(line), version))


@mcp.tool()
@_logged
def get_type_definition(name: str, version: Version | None = None,
                        rev: str | None = None) -> str:
    """Return the definition of a struct, union, enum, typedef, macro or global
    variable by name (file, line span, source) — e.g. to see a field's width or
    signedness before reasoning about an overflow. `version`: "work" (files on
    disk), "old" (parent of `rev`) or "new" (`rev`)."""
    ctx, version = _target(version, rev)
    r = ctx.type_definition(name, version)
    if "source" not in r:
        return _dump(r)
    return _clip(f"{name} ({r['kind']}, {version} version) — "
                 f"{r['file']}:{r['start_line']}-{r['end_line']}\n{r['source']}")


def main(argv=None):
    global SESSION, LOCK
    ap = argparse.ArgumentParser(
        prog="crossslice mcp",
        description="MCP server (stdio) for coding agents. Default: the working tree of "
                    "the repository in the current directory, with commit tools for any "
                    "revision; --commit scopes the server to one commit.")
    ap.add_argument("repo", nargs="?", default=None,
                    help="repository (default: -C, else the current directory)")
    ap.add_argument("-C", "--repo", dest="repo_opt", metavar="DIR", default=None,
                    help="repository directory (default: the current directory)")
    ap.add_argument("--commit", default=None,
                    help="scope the server to this commit (old = its parent, new = it)")
    ap.add_argument("--lock-version", choices=["old", "new"], default=None,
                    help="with --commit: expose only this version (disables the diff tools)")
    ap.add_argument("--cache-dir", default=None,
                    help="cache root (default: $CROSSSLICE_CACHE_DIR or ~/.cache/crossslice)")
    args = ap.parse_args(argv)

    try:
        ws = find_workspace(args.repo_opt or args.repo)
    except FileNotFoundError as e:
        print(f"[mcp] {e}", file=sys.stderr)
        sys.exit(2)
    if args.lock_version and not args.commit:
        print("[mcp] --lock-version needs --commit", file=sys.stderr)
        sys.exit(2)
    LOCK = args.lock_version
    SESSION = Session(ws.root, ws.git_root, commit=None, cache_dir=args.cache_dir)
    if args.commit:
        try:
            ctx = SESSION.commit_ctx(args.commit)
        except ToolError as e:
            print(f"[mcp] {e}", file=sys.stderr)
            sys.exit(1)
        SESSION.commit = ctx.sha
        print(f"[mcp] crossslice ready on {ws.root} @ {ctx.sha[:12]} "
              f"(parent {ctx.prev[:12]})", file=sys.stderr, flush=True)
    else:
        mode = ("commit tools default to HEAD" if ws.is_git else NO_GIT)
        print(f"[mcp] crossslice ready on {ws.root} (working tree; {mode})",
              file=sys.stderr, flush=True)
    _install_signal_handlers()
    try:
        import anyio
        anyio.run(_serve_isolated)
    except KeyboardInterrupt:
        pass
    finally:
        SESSION.close()


def _install_signal_handlers():
    """Exit promptly on SIGTERM/SIGINT (docker stop, editor shutdown, Ctrl-C):
    remove the temporary worktrees and stop clangd, then leave without waiting
    for the thread blocked on stdin (asyncio would join it for minutes).
    Docker runs the server as PID 1, which ignores SIGTERM without a handler."""
    import signal

    def stop(signum, _frame):
        print(f"[mcp] signal {signum}: shutting down", file=sys.stderr, flush=True)
        try:
            if SESSION is not None:
                SESSION.close()
        finally:
            os._exit(0)

    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGHUP):
        signal.signal(sig, stop)


async def _serve_isolated():
    """Serve MCP over private copies of the original stdin/stdout, then point
    the process's fd 0 at /dev/null and fd 1 at stderr. Every child process
    the analysis spawns (gtags, global, git, GumTree's JVM, clangd, gcc) and
    every stray print — from any thread — then lands on stderr instead of the
    protocol channel. Without this a child that reads stdin (`gcc -E -v -`)
    swallowed the next request and the session hung."""
    import io
    import anyio
    from mcp.server.stdio import stdio_server
    chan_in = os.fdopen(os.dup(0), "rb", buffering=0)
    chan_out = os.fdopen(os.dup(1), "wb", buffering=0)
    devnull = os.open(os.devnull, os.O_RDONLY)
    os.dup2(devnull, 0)
    os.dup2(2, 1)
    sys.stdout = sys.stderr
    stdin = anyio.wrap_file(io.TextIOWrapper(chan_in, encoding="utf-8", errors="replace"))
    stdout = anyio.wrap_file(io.TextIOWrapper(chan_out, encoding="utf-8"))
    async with stdio_server(stdin=stdin, stdout=stdout) as (read, write):
        await mcp._mcp_server.run(read, write,
                                  mcp._mcp_server.create_initialization_options())


if __name__ == "__main__":
    main()
