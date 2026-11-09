"""
Interactive graph explorer server.

A tiny stdlib HTTP server over a RepoGraph: serves the built Vue single-page
UI (crossslice/cross/webui/, built from frontend/ via `npm run build`) and a
small JSON API. Clicking a node in the UI calls /api/expand, which runs the
demand-driven cascade server-side and streams the newly materialized ring
back into the view — the graph construction made visible.

  crossslice explore --open                     # repository in the current directory
  crossslice explore -C data/repos/ffmpeg --focus mp_decode_layer3

Then open http://127.0.0.1:8000/ (the next free port if 8000 is taken).

Endpoints (all JSON):
  GET  /                              -> the UI
  GET  /api/state                     -> current graph (nodes + edges + focus)
  POST /api/expand   {id|name, levels}-> expand a node, return updated graph
  GET  /api/search?q=NAME             -> gtags symbol candidates for NAME
  GET  /api/node?id=ID|name=NAME      -> full node detail (sliced body / summary)
  POST /api/update                    -> incremental refresh after repo change
  GET  /api/commits?limit=N           -> recent commits that touch C files
  GET  /api/commit?rev=REV            -> commit context of REV (enrich pipeline)
  GET  /api/context?file=F&line=N     -> code context at a position (editor integration)
  GET  /api/functions?file=F          -> function definitions in a file (editor CodeLens)
  GET  /api/health                    -> {ok, version, repo, is_git}
"""

import argparse
import contextlib
import json
import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs


from crossslice.cross.graph import RepoGraph
from crossslice.paths import NO_GIT, MissingTool, add_repo_args, workspace_from_args

_PKG_DIR = os.path.dirname(os.path.abspath(__file__))
_WEBUI_DIR = os.path.join(_PKG_DIR, "webui")

_CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".svg": "image/svg+xml",
    ".ico": "image/x-icon",
    ".map": "application/json",
    ".woff2": "font/woff2",
}


class GraphService:
    """Thread-safe wrapper around a RepoGraph for the HTTP handlers."""

    def __init__(self, graph: RepoGraph, git_root: str | None = None):
        self.graph = graph
        self.git_root = git_root
        self.is_git = git_root is not None
        self.lock = threading.Lock()
        self.commit_lock = threading.Lock()   # one enrichment at a time
        self._commit_cache: dict = {}

    def snapshot(self, focus=None):
        """Full node/edge list for the UI (only materialized nodes)."""
        with self.lock:
            g = self.graph.db
            nodes = []
            for nid, name, file, line, state, kind, method in g.execute(
                    "SELECT id, name, file, line, state, kind, resolution_method"
                    " FROM nodes"):
                nodes.append({"id": nid, "name": name, "file": file,
                              "line": line + 1, "state": state, "kind": kind,
                              "resolution_method": method})
            edges = [{"src": s, "dst": d, "line": (cl + 1) if cl is not None else None}
                     for s, d, cl in g.execute(
                         "SELECT src, dst, call_line FROM edges")]
            return {"nodes": nodes, "edges": edges, "focus": focus,
                    "stats": self._stats(),
                    "meta": {"repo": os.path.basename(self.graph.repo_path),
                             "repo_path": self.graph.repo_path,
                             "commit": self.graph.commit,
                             "is_git": self.is_git}}

    def _stats(self):
        n = dict(self.graph.db.execute(
            "SELECT state, COUNT(*) FROM nodes GROUP BY state").fetchall())
        e = self.graph.db.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        return {"nodes": n, "edges": e}

    def expand(self, name=None, levels=1, node_id=None, file=None, line=None, kind=None):
        """Expand by node id (a click), by a specific definition (a search hit or
        an alternative: file + 1-based line), or by bare name."""
        with self.lock:
            if node_id is not None:
                node = self.graph._node(int(node_id))
                if node is None:
                    raise ValueError(f"no node with id {node_id}")
                name = node["name"]
                fid = self.graph.expand(name, direction="both", levels=levels,
                                        node_id=int(node_id))
            elif name and file and line:
                fid = self.graph.expand_definition(name, file, int(line) - 1,
                                                   kind or "function", levels=levels)
            elif name:
                fid = self.graph.expand(name, direction="both", levels=levels)
            else:
                raise ValueError("expand needs an id or a name")
        if fid is None:
            with self.lock:
                sugg = self.graph.gtags.suggest(name)
            raise ValueError(f"'{name}' has no definition in this repository"
                             + (f". Did you mean: {', '.join(sugg[:5])}?" if sugg else ""))
        snap = self.snapshot(focus=name)
        snap["focus_id"] = fid
        return snap

    def search(self, q):
        """Definitions of the exact name; when there are none, similar names."""
        with self.lock:
            self.graph._ensure_gtags()
            defs = self.graph.gtags.find_function_definition_detailed(q)
            suggestions = [] if defs else self.graph.gtags.suggest(q)
        hits = [{"name": q, "file": os.path.relpath(d["file_path"], self.graph.root)
                 if os.path.isabs(d["file_path"]) else d["file_path"],
                 "line": d["line_number"], "code": d["code_line"],
                 "kind": "macro" if d["code_line"].lstrip().startswith("#") else "function"}
                for d in defs[:20]]
        return {"hits": hits, "suggestions": suggestions}

    def node_detail(self, name=None, node_id=None):
        with self.lock:
            node = (self.graph._node(int(node_id)) if node_id is not None
                    else self.graph._find_node_by_name(name))
            if not node:
                return {"error": f"{name or node_id} not resolved"}
            name = node["name"]
            cur = self.graph.db.execute(
                "SELECT analysis, summary, signature FROM nodes WHERE id=?",
                (node["id"],))
            analysis, summary, signature = cur.fetchone()
        detail = {"id": node["id"], "name": name, "file": node["file"], "line": node["line"],
                  "kind": node["kind"], "state": node["state"],
                  "signature": signature,
                  "resolution_method": node["resolution_method"],
                  "callers_total": node.get("callers_total"),
                  "callers_cap": self.graph.max_callers_per_fn,
                  "callers_truncated": bool(node.get("callers_total")
                                            and node["callers_total"] > self.graph.max_callers_per_fn),
                  "alternatives": node.get("alternatives") or [],
                  "summary": json.loads(summary) if summary else None}
        if analysis:
            from crossslice.cross.context import full_body_text, sliced_body_text
            data = json.loads(analysis)
            detail["body"] = sliced_body_text(data, signature=signature)     # parameters/returns slice
            detail["body_full"] = full_body_text(data, signature=signature)  # every statement, headers only
        return detail

    def update(self):
        with self.lock:
            info = self.graph.update()
        return {"updated": info, **self.snapshot()}

    # ---- editor integration --------------------------------------------------

    def health(self):
        from crossslice import __version__
        return {"ok": True, "version": __version__, "repo": self.graph.repo_path,
                "commit": self.graph.commit, "is_git": self.is_git, "pid": os.getpid()}

    def _rel(self, file):
        """A path from the editor (absolute or relative) as a path below the analysis root."""
        if not file:
            raise ValueError("file is required")
        if os.path.isabs(file):
            rel = os.path.relpath(os.path.realpath(file), os.path.realpath(self.graph.repo_path))
            if rel.startswith(".."):
                raise ValueError(f"{file} is outside the analyzed directory {self.graph.repo_path}")
            return rel
        return os.path.normpath(file)

    def context(self, file, line, show_slice=True, slice_level=2):
        """Code context for FILE:LINE, the same text as `crossslice context`."""
        from crossslice.cross.context import context_at
        rel = self._rel(file)
        with self.lock:
            try:
                res = context_at(self.graph, rel, int(line), show_slice=show_slice,
                                 slice_level=slice_level)
            except FileNotFoundError as e:
                raise ValueError(str(e))
        if isinstance(res, dict):
            raise ValueError(res.get("error", "unknown error"))
        return {"file": rel, "line": int(line), "text": res}

    def functions(self, file):
        """Function definitions in FILE with 1-based line spans (for CodeLens)."""
        from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
        rel = self._rel(file)
        abs_path = os.path.join(self.graph.root, rel)
        if not os.path.isfile(abs_path):
            raise ValueError(f"{rel}: no such file in the analyzed tree")
        out = []
        for _node, name, s0, e0 in SourceCodeParserC(abs_path).collect_function_definitions():
            if name:
                out.append({"name": name, "line": s0 + 1, "end_line": e0 + 1, "kind": "function"})
        return {"file": rel, "functions": out}

    # ---- commit mode ---------------------------------------------------------

    def _require_git(self):
        if not self.is_git:
            raise ValueError(f"{NO_GIT}")

    def commits(self, limit=30):
        """Recent commits that change C sources below the analysis root
        (newest first; pathspecs are relative to the working directory)."""
        self._require_git()
        out = subprocess.run(
            ["git", "log", f"-n{int(limit)}", "--format=%H%x1f%h%x1f%s%x1f%an%x1f%ar%x1f%P",
             "--", "*.c", "*.h"],
            cwd=self.graph.repo_path, capture_output=True, text=True, errors="replace")
        rows = []
        for line in out.stdout.splitlines():
            parts = line.split("\x1f")
            if len(parts) == 6:
                sha, short, subject, author, when, parents = parts
                rows.append({"sha": sha, "short": short, "subject": subject,
                             "author": author, "when": when,
                             "merge": len(parents.split()) > 1})
        return {"commits": rows}

    def commit(self, rev="HEAD"):
        """Commit context of `rev`: changed files and functions, the raw diff,
        and the enriched text (intra slice + cross-function context). Cached
        per SHA; the graph lock is not held, so the graph stays usable."""
        self._require_git()
        from crossslice.commit import enrich_commit, resolve_commit, split_sections
        sha = resolve_commit(self.git_root, rev or "HEAD")
        if sha in self._commit_cache:
            return self._commit_cache[sha]
        with self.commit_lock:
            if sha in self._commit_cache:
                return self._commit_cache[sha]
            with contextlib.redirect_stdout(sys.stderr):
                res = enrich_commit(self.git_root, sha)
            git = ["git", "-C", self.git_root]
            subject, author, when = subprocess.run(
                git + ["show", "-s", "--format=%s%x1f%an%x1f%ar", sha],
                capture_output=True, text=True, errors="replace").stdout.strip().split("\x1f")
            diff = subprocess.run(
                git + ["diff", "-U3", res.parent, sha, "--", *res.changed_files],
                capture_output=True, text=True, errors="replace").stdout if res.changed_files else ""
            out = {"sha": sha, "parent": res.parent, "subject": subject, "author": author,
                   "when": when, "files": res.changed_files, "functions": res.functions,
                   "text": res.text, "sections": split_sections(res.text),
                   "diff": diff, "seconds": round(res.seconds, 1),
                   "note": res.note, "cross_error": res.cross_error,
                   "cross_stats": res.cross_stats}
            self._commit_cache[sha] = out
            return out


def make_handler(service: GraphService):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            pass  # quiet

        def _send(self, obj, status=200, content_type="application/json"):
            body = obj if isinstance(obj, bytes) else json.dumps(obj, default=str).encode()
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body_json(self):
            length = int(self.headers.get("Content-Length", 0))
            if not length:
                return {}
            try:
                return json.loads(self.rfile.read(length))
            except Exception:
                return {}

        def _send_static(self, rel):
            """Serve a file from the built web UI (crossslice/cross/webui, built from frontend/)."""
            path = os.path.normpath(os.path.join(_WEBUI_DIR, rel or "index.html"))
            if not path.startswith(_WEBUI_DIR) or not os.path.isfile(path):
                # SPA fallback: unknown non-API paths get the app shell
                path = os.path.join(_WEBUI_DIR, "index.html")
            ext = os.path.splitext(path)[1]
            with open(path, "rb") as f:
                self._send(f.read(),
                           content_type=_CONTENT_TYPES.get(ext,
                                                           "application/octet-stream"))

        def do_GET(self):
            u = urlparse(self.path)
            q = parse_qs(u.query)
            try:
                if not u.path.startswith("/api/"):
                    self._send_static(u.path.lstrip("/"))
                elif u.path == "/api/state":
                    self._send(service.snapshot())
                elif u.path == "/api/search":
                    self._send(service.search(q.get("q", [""])[0]))
                elif u.path == "/api/node":
                    nid = q.get("id", [None])[0]
                    self._send(service.node_detail(name=q.get("name", [""])[0],
                                                   node_id=nid))
                elif u.path == "/api/health":
                    self._send(service.health())
                elif u.path == "/api/context":
                    self._send(service.context(q.get("file", [""])[0], q.get("line", ["0"])[0],
                                               show_slice=q.get("slice", ["1"])[0] != "0"))
                elif u.path == "/api/functions":
                    self._send(service.functions(q.get("file", [""])[0]))
                elif u.path == "/api/commits":
                    self._send(service.commits(int(q.get("limit", ["30"])[0])))
                elif u.path == "/api/commit":
                    self._send(service.commit(q.get("rev", ["HEAD"])[0]))
                else:
                    self._send({"error": "not found"}, status=404)
            except (ValueError, MissingTool) as e:
                self._send({"error": str(e)}, status=400)
            except Exception as e:
                self._send({"error": f"{type(e).__name__}: {e}"}, status=500)

        def do_POST(self):
            u = urlparse(self.path)
            data = self._body_json()
            try:
                if u.path == "/api/expand":
                    self._send(service.expand(name=data.get("name"),
                                              levels=int(data.get("levels", 1)),
                                              node_id=data.get("id"),
                                              file=data.get("file"),
                                              line=data.get("line"),
                                              kind=data.get("kind")))
                elif u.path == "/api/update":
                    self._send(service.update())
                else:
                    self._send({"error": "not found"}, status=404)
            except (ValueError, MissingTool) as e:
                self._send({"error": str(e)}, status=400)
            except Exception as e:
                self._send({"error": f"{type(e).__name__}: {e}"}, status=500)

    return Handler


def _bind(host, port, handler, explicit):
    """Bind to `port`; when the user did not choose it, try the next few."""
    import errno
    for p in ([port] if explicit else range(port, port + 20)):
        try:
            return ThreadingHTTPServer((host, p), handler)
        except OSError as e:
            if e.errno != errno.EADDRINUSE or explicit:
                raise
    raise OSError(f"no free port in {port}-{port + 19}; pass --port")


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="crossslice explore",
        description="Interactive call-graph explorer in the browser. Click a function to "
                    "expand it; the Commit tab shows the commit context of recent commits.")
    add_repo_args(ap)
    ap.add_argument("--db", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--focus", default=None, metavar="FUNCTION",
                    help="expand this function at startup")
    ap.add_argument("--levels", type=int, default=1, metavar="N",
                    help="rings to expand for --focus (default 1)")
    ap.add_argument("--port", type=int, default=None,
                    help="port (default 8000, or the next free one)")
    ap.add_argument("--host", default=os.environ.get("CROSSSLICE_HOST", "127.0.0.1"),
                    help="interface to listen on (default 127.0.0.1; the Docker image "
                         "sets CROSSSLICE_HOST=0.0.0.0)")
    ap.add_argument("--open", action="store_true", help="open the explorer in the default browser")
    args = ap.parse_args(argv)
    ws, sha = workspace_from_args(args, "crossslice explore")

    import signal

    def _stop(signum, _frame):  # docker stop / kill: leave serve_forever, clean up
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, _stop)

    with contextlib.redirect_stdout(sys.stderr):
        graph = RepoGraph(ws.root, commit=sha, db_path=args.db, cache_dir=args.cache_dir)
    try:
        service = GraphService(graph, git_root=ws.git_root)
        if args.focus:
            print(f"expanding {args.focus} ...", file=sys.stderr)
            try:
                with contextlib.redirect_stdout(sys.stderr):
                    service.expand(args.focus, args.levels)
            except (ValueError, MissingTool) as e:
                print(f"--focus: {e}", file=sys.stderr)
        server = _bind(args.host, args.port or 8000, make_handler(service),
                       explicit=args.port is not None)
        host, port = server.server_address[:2]
        shown = "127.0.0.1" if host in ("0.0.0.0", "") else host
        url = f"http://{shown}:{port}/"
        what = f"{ws.root}" + (f" @ {sha[:12]}" if sha else "")
        print(f"CrossSlice explorer for {what}\n  {url}  (Ctrl-C to stop)", flush=True)
        if args.open:
            import webbrowser
            threading.Timer(0.5, lambda: webbrowser.open(url)).start()
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            print("stopping", file=sys.stderr)
        finally:
            server.server_close()
    finally:
        with contextlib.redirect_stdout(sys.stderr):
            graph.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
