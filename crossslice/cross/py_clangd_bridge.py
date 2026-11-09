#!/usr/bin/env python3
"""
py-clangd-bridge
================

A lightweight Python library to:
  1) Synthesize or locate a `compile_commands.json` for C projects using multiple strategies
     (works even for partial / non-buildable trees via a heuristic scoped DB), and
  2) Talk to `clangd` via LSP over stdio with a tiny client you can call from Python
     to resolve definitions, references, and call hierarchies for OLD/NEW code trees.

No third-party deps. Python 3.9+.

Design goals
------------
- Never require a full build.
- Scope indexing to just the files you care about (e.g., diff neighborhood).
- Work on giant trees (Linux kernel) with timeouts and fallbacks.
- Be easy to embed in an analysis pipeline.
- Wait for background indexing to complete for accurate cross-TU queries.

Usage (quickstart)
------------------
from crossslice.cross.py_clangd_bridge import CompileDBBuilder, ClangdSession

root = "/path/to/project"  # per-version root (old/new in separate dirs)
# 1) Make or find a compile DB (scoped to the files you care about):
files_of_interest = [
    f"{root}/drivers/net/ethernet/eth.c",
    f"{root}/include/linux/net.h",
]
db_path = CompileDBBuilder(root).ensure_compile_commands(target_files=files_of_interest)

# 2) Start clangd bound to that DB and query:
with ClangdSession(project_root=root, compile_commands_dir=db_path.parent) as ls:
    loc = ls.definition(file=f"{root}/drivers/net/ethernet/eth.c", line=123, col=17)
    refs = ls.references(file=f"{root}/drivers/net/ethernet/eth.c", line=123, col=17, include_declaration=True)
    ch_items = ls.prepare_call_hierarchy(file=f"{root}/drivers/net/ethernet/eth.c", line=123, col=17)
    out_calls = ls.outgoing_calls(ch_items[0]) if ch_items else []
    in_calls  = ls.incoming_calls(ch_items[0]) if ch_items else []

See the bottom of the file for a __main__ smoke test.
"""
from __future__ import annotations

import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import argparse
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# ------------------------------- Utilities ---------------------------------

@dataclass
class CmdResult:
    code: int
    out: str
    err: str


def run(cmd: List[str], cwd: Optional[Union[str, Path]] = None, timeout: int = 30) -> CmdResult:
    """Run a command, return code/stdout/stderr. Never raises. Trims output."""
    try:
        p = subprocess.run(
            cmd,
            cwd=str(cwd) if cwd is not None else None,
            stdin=subprocess.DEVNULL,   # `gcc -E -v -` reads stdin: never ours
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
            text=True,
        )
        return CmdResult(p.returncode, p.stdout.strip(), p.stderr.strip())
    except Exception as e:
        return CmdResult(127, "", f"{e}")


def which(exe: str) -> Optional[str]:
    return shutil.which(exe)


# ----------------------- compile_commands.json builder ----------------------

class CompileDBBuilder:
    """
    Attempts multiple strategies to obtain a compile_commands.json for C code.

    Strategy order (short-circuit on success):
      1) Existing compile_commands.json in root or immediate subdirs
      2) Linux kernel helper (scripts/clang-tools/gen_compile_commands.py)
      3) CMake configure-only export (if CMakeLists.txt exists)
      4) Optional external tools if available: 'compiledb' (parses Makefiles)
      5) Heuristic SCOPED DB for target files (no build system required)

    The heuristic builder creates command entries for only the provided target files,
    discovering local include directories and adding system include paths.
    """

    def __init__(self, project_root: Union[str, Path],
                 work_dir: Optional[Union[str, Path]] = None):
        self.root = Path(project_root).resolve()
        # generated databases go here; CrossSlice passes a folder in its cache
        # so a user's checkout is never written to
        self._work_dir = Path(work_dir).resolve() if work_dir else self.root / ".py_clangd_bridge"
        self._work_dir.mkdir(parents=True, exist_ok=True)

    # -- Public API --
    def ensure_compile_commands(self, target_files: Optional[List[Union[str, Path]]] = None,
                                prefer_existing: bool = True,
                                allow_cmake: bool = True,
                                allow_kernel_helper: bool = True,
                                allow_compiledb: bool = True,
                                system_include_probe: bool = True) -> Path:
        """
        Returns path to compile_commands.json. May be a copy/symlink or generated file.
        If target_files is provided, the heuristic builder will limit to that set.
        """
        # 1) Existing
        if prefer_existing:
            existing = self._find_existing_db()
            if existing:
                return existing

        # 2) Linux kernel helper
        if allow_kernel_helper and (self.root / "scripts/clang-tools/gen_compile_commands.py").exists():
            db = self._try_kernel_helper()
            if db:
                return db

        # 3) CMake export
        if allow_cmake and (self.root / "CMakeLists.txt").exists():
            db = self._try_cmake_export()
            if db:
                return db

        # 4) compiledb (optional; pip install compiledb)
        if allow_compiledb and which("compiledb"):
            db = self._try_compiledb()
            if db:
                return db

        # 5) Heuristic scoped DB
        db = self._build_heuristic_db(target_files=target_files, system_include_probe=system_include_probe)
        return db

    # -- Strategies --
    def _find_existing_db(self) -> Optional[Path]:
        candidates = [self.root / "compile_commands.json"]
        # common build dirs
        for d in ["build", "out", ".cmake", ".build", ".cache", "cmake-build", "build-debug", "build-release"]:
            candidates.append(self.root / d / "compile_commands.json")
        for c in candidates:
            if c.exists():
                return c.resolve()
        # one level deep search but bounded; hidden directories are skipped (a
        # leftover `.py_clangd_bridge/compile_commands.json` of an older run would
        # make clangd keep its index next to it, inside the checkout)
        for sub in list(self.root.glob("*/compile_commands.json"))[:20]:
            if not sub.parent.name.startswith("."):
                return sub.resolve()
        return None

    def _try_kernel_helper(self) -> Optional[Path]:
        script = self.root / "scripts/clang-tools/gen_compile_commands.py"
        if not script.exists():
            return None
        # The kernel script writes compile_commands.json at the root; it expects a configured tree.
        # It doesn't compile, just inspects make metadata. Try it with a timeout.
        res = run([sys.executable, str(script)], cwd=self.root, timeout=120)
        out_path = self.root / "compile_commands.json"
        if out_path.exists():
            return out_path.resolve()
        return None

    def _try_cmake_export(self) -> Optional[Path]:
        if not which("cmake"):
            return None
        bdir = self._work_dir / "cmake-export"
        bdir.mkdir(parents=True, exist_ok=True)
        args = [
            "cmake", "-S", str(self.root), "-B", str(bdir),
            "-DCMAKE_EXPORT_COMPILE_COMMANDS=ON",
        ]
        res = run(args, cwd=self.root, timeout=120)
        db = bdir / "compile_commands.json"
        return db.resolve() if db.exists() else None

    def _try_compiledb(self) -> Optional[Path]:
        # compiledb can parse Makefile rules without executing recipes (fast for many projects)
        # usage: compiledb -n make
        db = self._work_dir / "compiledb" / "compile_commands.json"
        db.parent.mkdir(parents=True, exist_ok=True)
        res = run(["compiledb", "-n", "-o", str(db), "make"], cwd=self.root, timeout=120)
        return db.resolve() if db.exists() else None

    # Heuristic builder ------------------------------------------------------
    def _build_heuristic_db(self, target_files: Optional[List[Union[str, Path]]], system_include_probe: bool) -> Path:
        # Scope to passed files; if none, choose a conservative subset: all .c under root up to a cap
        if target_files:
            files = [Path(f).resolve() for f in target_files]
        else:
            files = [p.resolve() for p in self.root.rglob("*.c")][:500]
        sys_includes = self._probe_system_includes() if system_include_probe else []
        proj_includes = self._discover_project_includes()
        header_index = self._build_header_index()
        entries = []
        for f in files:
            if not f.exists():
                continue
            local_inc = self._local_includes_for_file(f, header_index)
            incs = list(dict.fromkeys(proj_includes + local_inc))  # stable unique
            args = ["clang", "-x", "c"]
            for d in sys_includes + incs:
                args.extend(["-I", d])
            # conservative mode: define common guards we often see; you can tweak this list per project
            common_defs = ["-DDEBUG=1", "-D_GNU_SOURCE"]
            args.extend(common_defs)
            args.append(str(f))
            entries.append({
                "directory": str(self.root),
                "file": str(f),
                "arguments": args,
            })
        out = self._work_dir / "compile_commands.json"
        out.write_text(json.dumps(entries, indent=2))
        return out.resolve()

    def _probe_system_includes(self) -> List[str]:
        incs: List[str] = []
        # Try GCC probe first
        gcc = which("gcc") or which("clang")
        if not gcc:
            return incs
        # We ask the preprocessor for system include search paths
        # The output contains lines like:  #include <...> search starts here:  /usr/include  ...
        res = run([gcc, "-E", "-v", "-"], cwd=self.root, timeout=10)
        text = (res.err or res.out)
        grab = False
        for line in text.splitlines():
            if "#include <...> search starts here:" in line:
                grab = True
                continue
            if grab:
                if line.strip().startswith("End of search list."):
                    break
                path = line.strip()
                if path:
                    incs.append(path)
        return incs

    def _discover_project_includes(self) -> List[str]:
        # Common include roots
        dirs = []
        candidates = ["include", "includes", "inc", "headers", "src", "source"]
        for name in candidates:
            p = self.root / name
            if p.exists() and p.is_dir():
                dirs.append(str(p))
        # also any directory immediately under root named include*
        for sub in self.root.iterdir():
            if sub.is_dir() and sub.name.lower().startswith("include"):
                dirs.append(str(sub))
        # nested include dirs anywhere in the tree (e.g. source/include), capped
        nested = []
        for p in self.root.rglob("*"):
            if p.is_dir() and p.name.lower() in ("include", "includes", "inc"):
                if ".git" in p.parts:
                    continue
                nested.append(str(p))
                if len(nested) >= 20:
                    break
        dirs.extend(nested)
        # unique preserve order
        return list(dict.fromkeys(dirs))

    def _build_header_index(self, cap: int = 50000) -> Dict[str, List[Path]]:
        """Map header basename -> directories containing it, repo-wide."""
        index: Dict[str, List[Path]] = {}
        count = 0
        for p in self.root.rglob("*.h"):
            if ".git" in p.parts:
                continue
            index.setdefault(p.name, []).append(p.parent)
            count += 1
            if count >= cap:
                break
        return index

    def _local_includes_for_file(self, f: Path, header_index: Optional[Dict[str, List[Path]]] = None,
                                 max_dirs: int = 30) -> List[str]:
        incs: List[str] = []
        try:
            src = f.read_text(errors="ignore")
        except Exception:
            return incs
        # Find quoted includes only (local)
        for m in re.finditer(r"^\s*#\s*include\s*\"([^\"]+)\"", src, flags=re.M):
            inc = m.group(1)
            # 1) relative to the including file
            if (f.parent / inc).exists():
                incs.append(str((f.parent / inc).parent))
                continue
            # 2) resolve via repo-wide header index: find a root R with R/inc existing
            if header_index:
                basename = Path(inc).name
                for d in header_index.get(basename, []):
                    # strip the include's own directory part to get the -I root
                    rel_parts = Path(inc).parent.parts
                    root_candidate = d
                    ok = True
                    for part in reversed(rel_parts):
                        if root_candidate.name == part:
                            root_candidate = root_candidate.parent
                        else:
                            ok = False
                            break
                    if ok and (root_candidate / inc).exists():
                        incs.append(str(root_candidate))
                        break
        # also consider sibling include dirs
        for name in ["include", "inc", "headers"]:
            p = f.parent / name
            if p.exists():
                incs.append(str(p))
        # unique preserve order, capped to keep command lines sane
        return list(dict.fromkeys(incs))[:max_dirs]


# ------------------------------ LSP / clangd -------------------------------

class _ResponseWaiter:
    def __init__(self):
        self.cv = threading.Condition()
        self.result: Any = None
        self.error: Any = None
        self.done = False

    def set_result(self, result: Any):
        with self.cv:
            self.result = result
            self.done = True
            self.cv.notify_all()

    def set_error(self, error: Any):
        with self.cv:
            self.error = error
            self.done = True
            self.cv.notify_all()

    def wait(self, timeout: Optional[float] = 30.0) -> Any:
        with self.cv:
            if not self.done:
                self.cv.wait(timeout=timeout)
            if not self.done:
                raise TimeoutError("LSP request timed out")
            if self.error is not None:
                raise RuntimeError(f"LSP error: {self.error}")
            return self.result


class LSPClient:
    """Minimal JSON-RPC 2.0 client over stdio with Content-Length framing."""

    def __init__(self, cmd: List[str], cwd: Optional[Union[str, Path]] = None):
        self.cmd = cmd
        self.cwd = Path(cwd).resolve() if cwd else None
        self.proc: Optional[subprocess.Popen] = None
        self.reader = None
        self._id = 0
        self._lock = threading.Lock()
        self._waiters: Dict[int, _ResponseWaiter] = {}
        self._read_thread: Optional[threading.Thread] = None
        self._progress_notifications: List[Dict[str, Any]] = []
        self._progress_lock = threading.Lock()

    def start(self):
        self.proc = subprocess.Popen(
            self.cmd,
            cwd=str(self.cwd) if self.cwd else None,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            # nobody reads clangd's stderr; a full pipe would stall clangd
            stderr=subprocess.DEVNULL,
        )
        self._read_thread = threading.Thread(target=self._read_loop, daemon=True)
        self._read_thread.start()

    def stop(self):
        try:
            self.request("shutdown", {})
        except Exception:
            pass
        try:
            self.notify("exit", None)
        except Exception:
            pass
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def _read_exact(self, n: int) -> bytes:
        assert self.proc and self.proc.stdout
        buf = b""
        while len(buf) < n:
            chunk = self.proc.stdout.read(n - len(buf))
            if not chunk:
                break
            buf += chunk
        return buf

    def _read_loop(self):
        assert self.proc and self.proc.stdout
        f = self.proc.stdout
        while True:
            # Read headers
            headers: Dict[str, str] = {}
            header_bytes = b""
            while True:
                line = f.readline()
                if not line:
                    return
                if line in (b"\r\n", b"\n"):
                    break
                header_bytes += line
                try:
                    s = line.decode("utf-8")
                except Exception:
                    s = ""
                if ":" in s:
                    k, v = s.split(":", 1)
                    headers[k.strip().lower()] = v.strip()
            length = int(headers.get("content-length", "0"))
            if length <= 0:
                continue
            body = self._read_exact(length)
            try:
                msg = json.loads(body.decode("utf-8"))
            except Exception:
                continue
            # Dispatch
            if "id" in msg:
                wid = msg["id"]
                waiter = self._waiters.pop(wid, None)
                if waiter is not None:
                    if "result" in msg:
                        waiter.set_result(msg["result"])
                    else:
                        waiter.set_error(msg.get("error"))
            else:
                # Handle progress notifications for indexing status
                if msg.get("method") == "$/progress":
                    with self._progress_lock:
                        self._progress_notifications.append(msg)
                # Other notifications ignored (you may log them if needed)

    def wait_for_indexing(self, timeout: float = 60.0):
        """Wait until clangd's background indexing reports completion.

        Relies on $/progress notifications (token 'backgroundIndexProgress').
        If no 'begin' arrives within a grace period (nothing to index, or the
        server does not report progress), returns early instead of blocking.
        """
        deadline = time.time() + timeout
        begin_grace = time.time() + 3.0
        saw_begin = False
        while time.time() < deadline:
            with self._progress_lock:
                msgs = list(self._progress_notifications)
            for msg in msgs:
                params = msg.get("params", {})
                if params.get("token") != "backgroundIndexProgress":
                    continue
                kind = (params.get("value") or {}).get("kind")
                if kind == "begin":
                    saw_begin = True
                elif kind == "end" and saw_begin:
                    return True
            if not saw_begin and time.time() > begin_grace:
                return False
            time.sleep(0.1)
        return False

    def notify(self, method: str, params: Any):
        self._send({"jsonrpc": "2.0", "method": method, "params": params})

    def request(self, method: str, params: Any, timeout: float = 30.0):
        with self._lock:
            self._id += 1
            req_id = self._id
        waiter = _ResponseWaiter()
        self._waiters[req_id] = waiter
        self._send({"jsonrpc": "2.0", "id": req_id, "method": method, "params": params})
        return waiter.wait(timeout=timeout)

    def _send(self, payload: Dict[str, Any]):
        raw = json.dumps(payload).encode("utf-8")
        header = f"Content-Length: {len(raw)}\r\n\r\n".encode("ascii")
        assert self.proc and self.proc.stdin
        self.proc.stdin.write(header)
        self.proc.stdin.write(raw)
        self.proc.stdin.flush()


# ------------------------------ ClangdSession ------------------------------

class ClangdSession:
    """Small wrapper around clangd with handy helpers for C codebases."""

    def __init__(self, project_root: Union[str, Path], compile_commands_dir: Optional[Union[str, Path]] = None,
                 extra_args: Optional[List[str]] = None, debug=False, wait_for_indexing: bool = True):
        self.root = Path(project_root).resolve()
        self.ccdir = Path(compile_commands_dir).resolve() if compile_commands_dir else self.root
        clangd = which("clangd")
        if not clangd:
            raise RuntimeError("clangd not found in PATH")
        args = [clangd,
                f"--compile-commands-dir={self.ccdir}",
                "--background-index",  # helpful for xref across TUs
                "--log=error",
                ]
        if extra_args:
            args.extend(extra_args)
        self._client = LSPClient(args, cwd=self.root)
        self._initialized = False

        self.debug = debug
        self.wait_for_indexing_on_start = wait_for_indexing
        self._server_caps = {}

    # Context manager
    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.stop()

    def start(self):
        self._client.start()
        init_params = {
            "processId": os.getpid(),
            "rootUri": self._path_to_uri(self.root),
            "capabilities": {
                "textDocument": {
                    "callHierarchy": {"dynamicRegistration": False},
                },
                "window": {"workDoneProgress": True},
            },
            "workspaceFolders": [{
                "uri": self._path_to_uri(self.root),
                "name": self.root.name,
            }],
        }
        init_res = self._client.request("initialize", init_params, timeout=30)
        self._server_caps = init_res.get("capabilities", {}) or {}
        if self.debug:
            print("[clangd] server capabilities:")
            import json as _json
            print(_json.dumps(self._server_caps, indent=2))
        self._client.notify("initialized", {})
        self._initialized = True
        
        # Wait for initial indexing to complete for better query results
        if self.wait_for_indexing_on_start:
            if self.debug:
                print("[clangd] Waiting for background indexing to complete...")
            self.wait_for_indexing()
            if self.debug:
                print("[clangd] Indexing wait completed")

    def wait_for_indexing(self, timeout: float = 60.0):
        """Wait for clangd background indexing to complete."""
        self._client.wait_for_indexing(timeout)

    def stop(self):
        self._client.stop()
        self._initialized = False

    # ----------------- LSP helpers -----------------
    @staticmethod
    def _path_to_uri(p: Union[str, Path]) -> str:
        return Path(p).resolve().as_uri()

    def _pos(self, line: int, col: int) -> Dict[str, int]:
        # LSP uses 0-based lines/columns; we accept 0-based in API to avoid ambiguity
        return {"line": int(line), "character": int(col)}

    def _text_doc(self, file: Union[str, Path]) -> Dict[str, Any]:
        return {"uri": self._path_to_uri(file)}

    def open(self, file: Union[str, Path], language_id: str = "c"):
        path = Path(file)
        txt = path.read_text(errors="ignore")
        params = {
            "textDocument": {
                "uri": self._path_to_uri(path),
                "languageId": language_id,
                "version": 1,
                "text": txt,
            }
        }
        self._client.notify("textDocument/didOpen", params)

    def definition(self, file: Union[str, Path], line: int, col: int):
        params = {"textDocument": self._text_doc(file), "position": self._pos(line, col)}
        return self._client.request("textDocument/definition", params)

    def references(self, file: Union[str, Path], line: int, col: int, include_declaration: bool = False):
        params = {
            "textDocument": self._text_doc(file),
            "position": self._pos(line, col),
            "context": {"includeDeclaration": bool(include_declaration)}
        }
        return self._client.request("textDocument/references", params)
    
    def get_server_capabilities(self):
        return self._server_caps

    def supports_call_hierarchy(self) -> bool:
        ch = self._server_caps.get("callHierarchyProvider")
        return bool(ch)  # true or an object both mean supported

    # --- Call Hierarchy (LSP standard) ---
    def prepare_call_hierarchy(self, file: Union[str, Path], line: int, col: int):
        params = {"textDocument": self._text_doc(file), "position": self._pos(line, col)}
        return self._client.request("textDocument/prepareCallHierarchy", params)

    def incoming_calls(self, call_hierarchy_item: Dict[str, Any]):
        return self._client.request("callHierarchy/incomingCalls", {"item": call_hierarchy_item})

    def outgoing_calls(self, call_hierarchy_item: Dict[str, Any]):
        return self._client.request("callHierarchy/outgoingCalls", {"item": call_hierarchy_item})

    # --- Document symbols (handy for function ranges) ---
    def document_symbols(self, file: Union[str, Path]):
        params = {"textDocument": self._text_doc(file)}
        return self._client.request("textDocument/documentSymbol", params)


# ------------------------------- Smoke test --------------------------------

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="py-clangd-bridge quick demo")
    ap.add_argument("root", help="project root (per-version)")
    ap.add_argument("file", help="C file to query")
    ap.add_argument("line", type=int, help="0-based line")
    ap.add_argument("col", type=int, help="0-based column")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    file = Path(args.file).resolve()

    db = CompileDBBuilder(root).ensure_compile_commands(target_files=[file])
    print(f"Using compile_commands.json at: {db}")

    with ClangdSession(project_root=root, compile_commands_dir=db.parent) as ls:
        # optional: open the file (can help clangd with unsaved edits or perf)
        ls.open(file)
        defs = ls.definition(file, args.line, args.col)
        print("\nDEFINITION:")
        print(json.dumps(defs, indent=2))
        refs = ls.references(file, args.line, args.col, include_declaration=True)
        print("\nREFERENCES (truncated to 10):")
        print(json.dumps(refs[:10] if isinstance(refs, list) else refs, indent=2))
        chi = ls.prepare_call_hierarchy(file, args.line, args.col)
        print("\nCALL HIERARCHY PREPARE:")
        print(json.dumps(chi, indent=2))
        if chi:
            inc = ls.incoming_calls(chi[0])
            out = ls.outgoing_calls(chi[0])
            print("\nINCOMING CALLS:")
            print(json.dumps(inc, indent=2))
            print("\nOUTGOING CALLS:")
            print(json.dumps(out, indent=2))
