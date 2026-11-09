"""
On-demand repository graph.

A persistently cached code graph over one repository snapshot, built lazily:
nodes (functions/macros with their statement-level analysis and mod/ref
summary) and edges (calls) are materialized only when a query touches them.
The graph at any point in time is the union of past queries' neighborhoods.

  g = RepoGraph("data/repos/ffmpeg", commit="10e9d1f7...")
  g.expand("mp_decode_layer3", levels=1)   # focus fn analyzed, neighbors summarized
  g.expand("mp_decode_layer3", levels=2)   # one more ring, cached work reused
  g.update()                               # after the repo advanced: invalidate by
                                           # content hash, refresh gtags incrementally

Node states: 'summarized' (name/file/line/signature + light summary, the
default for neighbors) and 'analyzed' (full statement IR + mod/ref summary).
Invalidation is per file content hash — update() marks nodes of changed files
'stale'; they are re-analyzed on the next expand that touches them.
"""

import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from typing import Dict, List, Optional, Set, Tuple


from crossslice.cross.gtags_handler import GtagsHandler
from crossslice.cross.resolve import CallSite, TargetResolver, Worktree
from crossslice.cross.enrich import (CrossFunctionEnricher, _IDENT_RE, add_macro_writes,
                                     is_type_macro, macro_definitions)
from crossslice.intra.general_code_analyzer import create_ast_json
from crossslice.paths import repo_cache

# Bump this whenever the statement IR, the read/write summary or the slicing
# changes: cached stores built by an older analysis are rebuilt on open
# (the file content hash alone cannot tell that the analysis itself changed).
ANALYSIS_VERSION = "2026-11-03.10" + (  # .8: update() drops the edges of changed files; .9: stale nodes relocated, index manifest; .10: one node per definition, twins and caller-only nodes resolved by the cascade
    "-scalar" if os.environ.get("CROSSSLICE_DEFUSE") == "scalar" else "")

_SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes (
  id     INTEGER PRIMARY KEY AUTOINCREMENT,
  kind   TEXT NOT NULL,                    -- function | macro
  name   TEXT NOT NULL,
  file   TEXT NOT NULL,                    -- repo-relative path
  line   INTEGER NOT NULL,                 -- 0-based definition line
  blob_hash TEXT,
  signature TEXT,
  state  TEXT NOT NULL DEFAULT 'summarized',  -- summarized | analyzed | stale
  resolution_method TEXT,
  analysis TEXT,                           -- JSON statement IR (state=analyzed)
  summary  TEXT,                           -- JSON mod/ref summary
  UNIQUE(name, file, line)
);
CREATE TABLE IF NOT EXISTS edges (
  src INTEGER NOT NULL REFERENCES nodes(id),
  dst INTEGER NOT NULL REFERENCES nodes(id),
  kind TEXT NOT NULL DEFAULT 'calls',
  call_file TEXT,
  call_line INTEGER,
  UNIQUE(src, dst, kind, call_file, call_line)
);
CREATE INDEX IF NOT EXISTS idx_nodes_name ON nodes(name);
CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(src);
CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(dst);
CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
CREATE TABLE IF NOT EXISTS files (file TEXT PRIMARY KEY, blob_hash TEXT);  -- content the store was built from
"""


def _content_hash(path: str) -> Optional[str]:
    try:
        with open(path, "rb") as f:
            return hashlib.sha1(f.read()).hexdigest()
    except OSError:
        return None


class RepoGraph:

    def __init__(self, repo_path: str, commit: Optional[str] = None,
                 db_path: Optional[str] = None, slice_level: int = 2,
                 max_callers_per_fn: int = 50, debug: bool = False,
                 cache_dir: Optional[str] = None):
        self.repo_path = os.path.abspath(repo_path)
        # all caches live outside the checkout (crossslice.paths); cache_dir
        # overrides the cache root, db_path just the graph store
        self.cache_dir = repo_cache(self.repo_path, cache_dir)
        if commit:  # caches are keyed by SHA: never by a moving name like HEAD
            import subprocess
            out = subprocess.run(["git", "rev-parse", "--verify", "-q", f"{commit}^{{commit}}"],
                                 cwd=self.repo_path, capture_output=True, text=True)
            if out.returncode != 0:
                raise ValueError(f"{commit!r} is not a commit in {self.repo_path}")
            commit = out.stdout.strip()
        self.commit = commit
        self.debug = debug
        self.slice_level = slice_level
        self.max_callers_per_fn = max_callers_per_fn

        self._wt: Optional[Worktree] = None
        if commit:
            self._wt = Worktree(self.repo_path, commit).__enter__()
            # repo_path may be a subdirectory of the repository: analyze the
            # same subdirectory of the snapshot
            import subprocess
            prefix = subprocess.run(["git", "rev-parse", "--show-prefix"], cwd=self.repo_path,
                                    capture_output=True, text=True).stdout.strip()
            self.root = os.path.join(self._wt.path, prefix) if prefix else self._wt.path
        else:
            self.root = self.repo_path

        if db_path is None:
            tag = (commit[:12] if commit else "worktree")
            db_path = os.path.join(self.cache_dir, f"graph-{tag}.db")
        # check_same_thread=False so the HTTP server (graph_server.py) can share
        # one connection across handler threads; callers serialize access.
        # timeout: several processes (e.g. parallel agent runs) may share this
        # store; WAL lets readers proceed while one writer commits
        self.db = sqlite3.connect(db_path, check_same_thread=False, timeout=60)
        try:
            self.db.execute("PRAGMA journal_mode=WAL")
        except sqlite3.DatabaseError:
            pass
        self.db.executescript(_SCHEMA)
        self._migrate()
        self._check_analysis_version()
        self.db_path = db_path
        self._sig_cache: Dict[str, Tuple[Optional[str], Dict[int, str]]] = {}
        self._macro_cache: Dict[str, object] = {}   # name -> write effects of its macro definitions
        self._twin_choice: Dict[str, int] = {}      # name with several nodes -> the node the cascade picks

        # commit snapshot: the index is built inside the temporary worktree and
        # saved per commit, so a second RepoGraph on the same commit (another
        # process, another run) restores it instead of rebuilding — minutes on
        # Linux-sized trees. Working tree: the index itself lives in the cache
        # and is refreshed incrementally (gtags -i).
        if commit:
            self.gtags = GtagsHandler(self.root, cache_dir=os.path.join(
                self.cache_dir, "gtags", commit))
            clangd_dir = None  # inside the throwaway worktree
        else:
            self.gtags = GtagsHandler(self.root, dbpath=os.path.join(
                self.cache_dir, "gtags", "worktree"))
            clangd_dir = os.path.join(self.cache_dir, "clangd")
        self.resolver = TargetResolver(self.root, debug=debug, work_dir=clangd_dir)
        self._gtags_ready = False

    # ------------------------------------------------------------------
    # infrastructure
    # ------------------------------------------------------------------

    def _migrate(self):
        """Add columns introduced after a store was created (stores are caches)."""
        cols = {r[1] for r in self.db.execute("PRAGMA table_info(nodes)")}
        for col, decl in (("callers_total", "INTEGER"), ("alternatives", "TEXT")):
            if col not in cols:
                self.db.execute(f"ALTER TABLE nodes ADD COLUMN {col} {decl}")
        self.db.commit()

    def _check_analysis_version(self):
        """Drop a store that an older version of the analysis built."""
        row = self.db.execute("SELECT value FROM meta WHERE key='analysis_version'").fetchone()
        if row is not None and row[0] == ANALYSIS_VERSION:
            return
        if self.db.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]:
            print(f"[graph] analysis changed ({row[0] if row else 'unversioned'} -> "
                  f"{ANALYSIS_VERSION}): rebuilding the cached graph")
        self.db.executescript("DELETE FROM edges; DELETE FROM nodes; DELETE FROM files;")
        self.db.execute("INSERT OR REPLACE INTO meta (key, value) VALUES ('analysis_version', ?)",
                        (ANALYSIS_VERSION,))
        self.db.commit()

    def _signature_at(self, rel_file: str, line0: int) -> Optional[str]:
        """The head of the function definition starting at `line0` (everything
        before its body, on one line), parsed with tree-sitter and cached per file."""
        abs_file = os.path.join(self.root, rel_file)
        blob = _content_hash(abs_file)
        cached = self._sig_cache.get(abs_file)
        if cached is None or cached[0] != blob:
            sigs: Dict[int, str] = {}
            try:
                from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
                for node, _name, s0, _e0 in SourceCodeParserC(abs_file).collect_function_definitions():
                    head = node.text.decode("utf-8", errors="replace").split("{")[0]
                    sigs[s0] = " ".join(part.strip() for part in head.split("\n") if part.strip())[:200]
            except Exception:
                pass
            cached = (blob, sigs)
            self._sig_cache[abs_file] = cached
        return cached[1].get(line0)

    def _ensure_gtags(self):
        if not self._gtags_ready:
            self.gtags.ensure_index()
            self._gtags_ready = True

    def close(self):
        self.resolver.close()
        self.db.commit()
        self.db.close()
        if self._wt:
            self._wt.__exit__(None, None, None)
            self._wt = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # ------------------------------------------------------------------
    # node/edge store
    # ------------------------------------------------------------------

    @staticmethod
    def _clean_signature(sig):
        return re.sub(r"\s+", " ", (sig or "")).rstrip(" {").strip()[:200]

    def _upsert_node(self, kind, name, file, line, signature="",
                     resolution_method="", state="summarized",
                     analysis=None, summary=None) -> int:
        signature = self._clean_signature(signature)
        blob = _content_hash(os.path.join(self.root, file))
        self.db.execute("INSERT OR REPLACE INTO files (file, blob_hash) VALUES (?,?)", (file, blob))
        cur = self.db.execute(
            "SELECT id, state FROM nodes WHERE name=? AND file=? AND line=?",
            (name, file, line))
        row = cur.fetchone()
        if not row:
            # the same definition reached by another line convention (the
            # resolver reports the identifier's line, a caller lookup the
            # tree-sitter start line: one or two lines apart), or the stale
            # node of a definition that moved within its file — one node per
            # definition, so its edges from unchanged files survive
            twins = self.db.execute(
                "SELECT id, state, line FROM nodes WHERE name=? AND file=? AND kind=?",
                (name, file, kind)).fetchall()
            near = [t for t in twins if abs(t[2] - line) <= 2]
            if near:
                row = near[0][:2]
            elif len(twins) == 1 and twins[0][1] == "stale":
                # the only definition of this name in the file moved; with
                # several (START_TEST(x) { … } test bodies) nothing says which
                node_id = self._move_node(twins[0][0], name, file, line, kind)
                row = (node_id, "stale")
        if row:
            node_id, old_state = row
            # never downgrade an analyzed node to summarized
            if state == "analyzed" or old_state in ("summarized", "stale"):
                self.db.execute(
                    "UPDATE nodes SET kind=?, signature=?, resolution_method=?,"
                    " state=CASE WHEN ?='analyzed' THEN 'analyzed' ELSE state END,"
                    " blob_hash=?,"
                    " analysis=COALESCE(?, analysis), summary=COALESCE(?, summary)"
                    " WHERE id=?",
                    (kind, signature, resolution_method, state, blob,
                     json.dumps(analysis) if analysis else None,
                     json.dumps(summary) if summary else None, node_id))
            return node_id
        cur = self.db.execute(
            "INSERT INTO nodes (kind, name, file, line, blob_hash, signature,"
            " state, resolution_method, analysis, summary)"
            " VALUES (?,?,?,?,?,?,?,?,?,?)",
            (kind, name, file, line, blob, signature, state, resolution_method,
             json.dumps(analysis) if analysis else None,
             json.dumps(summary) if summary else None))
        return cur.lastrowid

    def _add_edge(self, src: int, dst: int, call_file=None, call_line=None):
        self.db.execute(
            "INSERT OR IGNORE INTO edges (src, dst, kind, call_file, call_line)"
            " VALUES (?,?,'calls',?,?)", (src, dst, call_file, call_line))

    def _node(self, node_id: int) -> Optional[dict]:
        cur = self.db.execute(
            "SELECT id, kind, name, file, line, signature, state,"
            " resolution_method, summary, callers_total, alternatives"
            " FROM nodes WHERE id=?", (node_id,))
        r = cur.fetchone()
        if r is None:
            return None
        keys = ["id", "kind", "name", "file", "line", "signature", "state",
                "resolution_method", "summary", "callers_total", "alternatives"]
        d = dict(zip(keys, r))
        if d["summary"]:
            d["summary"] = json.loads(d["summary"])
        d["alternatives"] = json.loads(d["alternatives"]) if d["alternatives"] else []
        return d

    def _find_node_by_name(self, name: str) -> Optional[dict]:
        """The node stored under a name. Several definitions can share a name
        (zlib: `gzdopen` in gzlib.c and a wrapper in test/minigzip.c,
        `check_match` as a function and as a macro in deflate.c), and a node
        reached only through a caller lookup may be the wrong one of them;
        then the cascade decides which definition the name means, as it would
        on a fresh graph, and the choice is cached until the next update()."""
        rows = self.db.execute(
            "SELECT id, file, kind, line, resolution_method FROM nodes WHERE name=?"
            " ORDER BY state='analyzed' DESC, id",
            (name,)).fetchall()
        if not rows:
            return None
        # a node without a resolution method was created as the enclosing
        # function of a reference site (a caller lookup), not by resolving the
        # name: it says nothing about which definition the name means
        if "(" not in name and (len(rows) > 1 or not rows[0][4]):
            choice = self._twin_choice.get(name)
            if choice is None:
                r = self._resolve_name_uncached(name)
                if r is not None:
                    kind = "macro" if r["is_macro"] else "function"
                    near = [row for row in rows if row[1] == r["rel_file"] and row[2] == kind
                            and abs(row[3] - r["line"]) <= 2]
                    # the cascade's pick may have no node yet (only its twins
                    # were reached, through callers): store it, so the name
                    # means the same definition as on a fresh graph
                    choice = near[0][0] if near else self._upsert_node(
                        kind, name, r["rel_file"], r["line"], signature=r["signature"],
                        resolution_method=r["resolution_method"])
                else:
                    choice = rows[0][0]
                self._twin_choice[name] = choice
            node = self._node(choice)
            if node is not None:
                return node
        return self._node(rows[0][0])

    # ------------------------------------------------------------------
    # analysis
    # ------------------------------------------------------------------

    def _analyze_node(self, name: str, rel_file: str, line: int,
                      kind: str, signature: str, method: str) -> Tuple[int, Optional[dict]]:
        """Fully analyze one definition; store as 'analyzed'. Returns (id, analysis)."""
        abs_file = os.path.join(self.root, rel_file)
        analysis, summary = None, None
        if kind == "function":
            # the definition head from tree-sitter beats whatever the resolver
            # stored (a caller's bare name, the return-type line of a GNU-style
            # definition)
            signature = self._signature_at(rel_file, line) or signature
            try:
                analysis = create_ast_json(abs_file, line)
            except Exception as e:
                if self.debug:
                    print(f"[graph] analysis failed for {name}: {e}")
            if analysis and analysis.get("statements"):
                stmts = analysis["statements"]
                param_ids = {p.get("var_id")
                             for p in stmts[0].get("parameters", []) if p.get("var_id")}
                summary = CrossFunctionEnricher._modref_summary(stmts, param_ids)
                self._ensure_gtags()
                add_macro_writes(stmts, summary,
                                 lambda n: macro_definitions(self.gtags, self.root, n),
                                 self._macro_cache)
        # a function whose body could not be analysed stays summarized, so the
        # next expand retries and a lookup by name prefers an analysed twin
        state = "analyzed" if (analysis and analysis.get("statements")) or kind != "function" else "summarized"
        node_id = self._upsert_node(
            kind, name, rel_file, line, signature=signature,
            resolution_method=method, state=state,
            analysis=analysis, summary=summary)
        return node_id, analysis

    def _relocate(self, node: dict):
        """Where is the definition of a stale node now? By name in the same
        file first (it usually just moved a few lines), then through the
        cascade; None when it is gone. Analysing at the old line would read
        whatever function covers that line now. Returns (file, line,
        signature, method, kind) — the kind can change too (zlib's
        `check_match` is a macro in one revision and a function in the next)."""
        name, kind = node["name"], node["kind"]
        if "(" in name:   # a macro-form caller name (`PHP_METHOD(C, m)`): no C symbol to look up
            return node["file"], node["line"], node["signature"] or "", node["resolution_method"] or "", kind
        # the cascade first: it answers what a fresh graph would store for the
        # name at this revision (the preferred of several definitions can change)
        r = self._resolve_name_uncached(name)
        if r is not None:
            return (r["rel_file"], r["line"], r["signature"], r["resolution_method"],
                    "macro" if r["is_macro"] else "function")
        try:
            from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
            parser = SourceCodeParserC(os.path.join(self.root, node["file"]))
            for n, fname, s0, _e0 in parser.collect_function_definitions():
                if fname == name and (n.type != "function_definition") == (kind == "macro"):
                    return node["file"], s0, node["signature"] or "", node["resolution_method"] or "stored", kind
        except Exception:
            pass
        return None

    def _move_node(self, node_id: int, name: str, rel_file: str, line: int, kind: str) -> int:
        """The definition of `node_id` is now at (rel_file, line): update the
        row in place, or merge into the node already stored there (edges
        re-pointed, the old row dropped), so a name keeps one node."""
        # the node's own callees came from the analysis at the old location
        # and are recomputed there; its callers are references to the name
        # and stay (their call sites were checked by update())
        self.db.execute("DELETE FROM edges WHERE src=?", (node_id,))
        row = self.db.execute("SELECT id FROM nodes WHERE name=? AND file=? AND line=?",
                              (name, rel_file, line)).fetchone()
        if row and row[0] != node_id:
            other = row[0]
            self.db.execute("INSERT OR IGNORE INTO edges (src, dst, kind, call_file, call_line)"
                            " SELECT src, ?, kind, call_file, call_line FROM edges WHERE dst=?", (other, node_id))
            self.db.execute("DELETE FROM edges WHERE dst=?", (node_id,))
            self.db.execute("DELETE FROM nodes WHERE id=?", (node_id,))
            return other
        self.db.execute("UPDATE nodes SET file=?, line=?, kind=?, blob_hash=NULL, analysis=NULL, summary=NULL"
                        " WHERE id=?", (rel_file, line, kind, node_id))
        return node_id

    def _resolve_name(self, name: str,
                      call_sites: Optional[List[CallSite]] = None) -> Optional[dict]:
        """Resolve a bare name to a definition: the definition already stored
        under this name wins (identity must not depend on how a name was first
        reached); otherwise the cascade decides."""
        existing = self._find_node_by_name(name)
        if existing is not None:
            return {"is_macro": existing["kind"] == "macro", "rel_file": existing["file"],
                    "line": existing["line"], "signature": existing["signature"] or "",
                    "resolution_method": existing["resolution_method"] or "stored",
                    "alternatives": existing.get("alternatives") or []}
        return self._resolve_name_uncached(name, call_sites)

    def _resolve_name_uncached(self, name: str,
                               call_sites: Optional[List[CallSite]] = None) -> Optional[dict]:
        self._ensure_gtags()
        sites = {name: call_sites or
                 [CallSite(callee=name, arg_count=-1, rel_file="", line=0, col=0)]}
        resolved = self.resolver.resolve(sites, self.gtags)
        return None if name not in resolved else resolved[name].__dict__

    # ------------------------------------------------------------------
    # public API
    # ------------------------------------------------------------------

    def expand(self, function_name: str, direction: str = "both",
               levels: int = 1, node_id: Optional[int] = None) -> Optional[int]:
        """Materialize the neighborhood of `function_name` up to `levels` rings.

        The focus function (and, at levels>1, inner-ring neighbors) are fully
        analyzed; the outermost ring is stored as summarized stubs. Cached
        analyzed nodes with unchanged file hashes are reused, not re-analyzed.
        """
        self._ensure_gtags()
        frontier = [function_name]
        focus_id = None
        for level in range(levels):
            next_frontier: List[str] = []
            for name in frontier:
                nid = self._expand_one(name, direction, next_frontier,
                                       node_id=node_id if level == 0 else None)
                if nid is None:
                    continue
                if focus_id is None and name == function_name:
                    focus_id = nid
            frontier = list(dict.fromkeys(next_frontier))
            if not frontier:
                break
        self.db.commit()
        return focus_id

    def expand_definition(self, name: str, rel_file: str, line: int, kind: str = "function",
                          direction: str = "both", levels: int = 1) -> Optional[int]:
        """Expand one specific definition (file, 0-based line) of a name — e.g. a
        search hit or an alternative of an ambiguous name — as its own node."""
        self._ensure_gtags()
        node_id = self._upsert_node(kind, name, rel_file, line,
                                    resolution_method="user_pick")
        self.db.commit()
        return self.expand(name, direction=direction, levels=levels, node_id=node_id)

    def _expand_one(self, name: str, direction: str,
                    next_frontier: List[str],
                    node_id: Optional[int] = None) -> Optional[int]:
        # Which definition: An explicit node (a click in the UI), else the node
        # already stored under this name, else the cascade. A name must map to
        # the same node however it was reached, so an existing node is analyzed
        # at ITS location and never re-resolved (that used to create a second
        # node when a bare-name lookup picked another candidate).
        existing = self._node(node_id) if node_id is not None else self._find_node_by_name(name)
        analysis = None
        if existing is not None:
            node_id = existing["id"]
            moved = existing["state"] == "stale"
            if existing["state"] == "analyzed":
                blob = _content_hash(os.path.join(self.root, existing["file"]))
                stored_blob, stored_analysis = self.db.execute(
                    "SELECT blob_hash, analysis FROM nodes WHERE id=?", (node_id,)).fetchone()
                if blob == stored_blob and stored_analysis:
                    analysis = json.loads(stored_analysis)
                elif blob != stored_blob:
                    moved = True   # the file changed without update(): same as stale
            if analysis is None and (existing["state"] != "analyzed"
                                     or existing["kind"] == "function"):
                rel_file, line, kind = existing["file"], existing["line"], existing["kind"]
                signature, method = existing["signature"] or "", existing["resolution_method"] or ""
                if moved:
                    # find the definition again before analysing: the stored
                    # line may now lie inside another function, or in no function
                    loc = self._relocate(existing)
                    if loc is None:   # the definition is gone
                        self.db.execute("DELETE FROM edges WHERE src=? OR dst=?", (node_id, node_id))
                        self.db.execute("DELETE FROM nodes WHERE id=?", (node_id,))
                        self.db.commit()
                        return None
                    rel_file, line, signature, method, kind = loc
                    node_id = self._move_node(node_id, name, rel_file, line, kind)
                node_id, analysis = self._analyze_node(
                    name, rel_file, line, kind, signature, method)
        else:
            r = self._resolve_name(name)
            if r is None:
                return None
            kind = "macro" if r["is_macro"] else "function"
            node_id, analysis = self._analyze_node(
                name, r["rel_file"], r["line"], kind, r["signature"],
                r["resolution_method"])
            if r.get("alternatives"):
                self.db.execute("UPDATE nodes SET alternatives=? WHERE id=?",
                                (json.dumps(r["alternatives"]), node_id))

        node = self._node(node_id)

        # downward: callees from the analysis
        if direction in ("both", "down") and analysis:
            calls: Dict[str, List[CallSite]] = {}
            for s in analysis.get("statements", []):
                for c in s.get("calls_info", []):
                    cname = c.get("function_name", "")
                    if not _IDENT_RE.match(cname) or cname == name:
                        continue
                    r0, c0 = c.get("position_start", [0, 0])
                    calls.setdefault(cname, []).append(CallSite(
                        callee=cname, arg_count=len(c.get("arguments", [])),
                        rel_file=node["file"], line=r0, col=c0))
            resolved = self.resolver.resolve(calls, self.gtags)
            for cname, tgt in resolved.items():
                if tgt.is_macro and calls[cname][0].arg_count > 0 and is_type_macro(tgt.signature):
                    continue  # `(INTFLOAT)(x)`: a type macro in a cast, not a call
                known = self._find_node_by_name(cname)
                if known is not None:
                    dst = known["id"]  # keep one node per name unless the user picks another
                else:
                    dst = self._upsert_node(
                        "macro" if tgt.is_macro else "function",
                        cname, tgt.rel_file, tgt.line, signature=tgt.signature,
                        resolution_method=tgt.resolution_method)
                    if tgt.alternatives:
                        self.db.execute("UPDATE nodes SET alternatives=? WHERE id=?",
                                        (json.dumps(tgt.alternatives), dst))
                for site in calls[cname]:          # one edge per call site
                    self._add_edge(node_id, dst, call_file=site.rel_file,
                                   call_line=site.line)
                next_frontier.append(cname)

        # upward: callers via gtags references (capped; the total is recorded)
        if direction in ("both", "up"):
            callers = self.resolver.find_callers(
                [name], self.gtags, self.max_callers_per_fn)
            total = getattr(self.resolver, "last_caller_totals", {}).get(name)
            if total is not None:
                self.db.execute("UPDATE nodes SET callers_total=? WHERE id=?",
                                (total, node_id))
            for site in callers.get(name, []):
                if not site.caller_name:
                    continue
                src = self._upsert_node(
                    "function", site.caller_name, site.rel_file, site.caller_start_line,
                    signature=self._signature_at(site.rel_file, site.caller_start_line)
                    or site.caller_header or site.caller_name)
                self._add_edge(src, node_id, call_file=site.rel_file,
                               call_line=site.line)
                if "(" not in site.caller_name:   # `PHP_METHOD(C, m)` is no C symbol to expand further
                    next_frontier.append(site.caller_name)

        return node_id

    def update(self) -> dict:
        """After the repository content changed: bring the store back to what a
        rebuild would answer. Files whose content hash differs from the one
        the store was built from have their nodes marked stale (re-analysed,
        or located again, on the next expand) and lose every edge whose call
        site lies in them — the call may be gone or moved, and a stale edge
        would otherwise survive forever (edges are only ever added). The
        resolver forgets its parsed trees and the macro cache is dropped. The
        symbol index is refreshed incrementally (`gtags -i`, by mtime) and the
        changed files are re-indexed explicitly (`--single-update`): gtags
        compares mtimes with one-second granularity and misses an edit made
        in the same second as the previous index write."""
        t0 = time.time()
        rows = self.db.execute("SELECT file, blob_hash FROM files").fetchall()
        if not rows:  # a store from before the files table
            rows = self.db.execute("SELECT file, MIN(blob_hash) FROM nodes GROUP BY file").fetchall()
        changed = []
        for rel_file, old_blob in rows:
            if _content_hash(os.path.join(self.root, rel_file)) != old_blob:
                changed.append(rel_file)
        stale = 0
        for rel_file in changed:
            stale += self.db.execute(
                "UPDATE nodes SET state='stale', analysis=NULL WHERE file=? AND state!='stale'",
                (rel_file,)).rowcount
            self.db.execute("DELETE FROM edges WHERE call_file=?", (rel_file,))
            blob = _content_hash(os.path.join(self.root, rel_file))
            if blob is None:  # the file is gone
                self.db.execute("DELETE FROM files WHERE file=?", (rel_file,))
            else:
                self.db.execute("INSERT OR REPLACE INTO files (file, blob_hash) VALUES (?,?)", (rel_file, blob))
        self.db.commit()
        if changed:
            self.resolver.invalidate()
            self._macro_cache.clear()
            self._twin_choice.clear()
        self.gtags.update([f for f in changed if os.path.exists(os.path.join(self.root, f))])
        self._gtags_ready = True
        return {"stale_nodes": stale, "changed_files": len(changed),
                "seconds": round(time.time() - t0, 3)}

    # ------------------------------------------------------------------
    # queries / export
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        n = self.db.execute("SELECT state, COUNT(*) FROM nodes GROUP BY state").fetchall()
        e = self.db.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return {"nodes": dict(n), "edges": e, "db": self.db_path}

    def neighborhood(self, function_name: str) -> dict:
        node = self._find_node_by_name(function_name)
        if not node:
            return {}
        callees = [dict(self._node(dst), call_file=cf, call_line=cl) for dst, cf, cl in self.db.execute(
            "SELECT dst, call_file, call_line FROM edges WHERE src=?", (node["id"],))]
        callers = [dict(self._node(src), call_file=cf, call_line=cl) for src, cf, cl in self.db.execute(
            "SELECT src, call_file, call_line FROM edges WHERE dst=?", (node["id"],))]
        return {"node": node, "callees": callees, "callers": callers}

    def to_dot(self) -> str:
        lines = ["digraph repo {", '  rankdir=LR; node [shape=box, fontsize=10];']
        for nid, name, state, kind in self.db.execute(
                "SELECT id, name, state, kind FROM nodes"):
            style = "filled" if state == "analyzed" else "dashed"
            fill = "lightblue" if kind == "function" else "lightyellow"
            lines.append(f'  n{nid} [label="{name}", style="{style}", fillcolor="{fill}"];')
        for src, dst in self.db.execute("SELECT src, dst FROM edges"):
            lines.append(f"  n{src} -> n{dst};")
        lines.append("}")
        return "\n".join(lines)
