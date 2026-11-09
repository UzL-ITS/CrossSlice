"""`crossslice` cli"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys

from crossslice import __version__

USAGE = """\
usage: crossslice <command> [options]

Run it inside a git checkout of a C project; every command analyzes the
repository containing the current directory (or -C DIR).

Commit context
  enrich   [REV]               the commit's change, its def-use slice, and the callees,
                               callers and macros it touches (REV defaults to HEAD)
  dataset  <jsonl>             batch enrichment of a JSONL list of commits

Code context (also works outside git)
  context  <file>:<line>       the function at that line: summary, callees, callers,
                               types; --slice adds the def-use slice around the line
  expand   <function>          a function's callees and callers (--levels, --dot)
  explore                      interactive call-graph explorer in the browser (--open)

Integrations
  mcp                          MCP server for coding agents over stdio

Maintenance
  graph    update|stats        refresh or inspect the cached graph
  check                        check git, GNU Global, clangd, Java and GumTree

Common options
  -C DIR                       repository directory (default: the current directory)
  --rev REV                    analyze a past revision instead of the files on disk
  --cache-dir DIR              cache root (default: ~/.cache/crossslice)

`crossslice <command> --help` lists every option of a command. Revisions are any
git expression: HEAD, HEAD~1, a tag, a short SHA.
"""

PASSTHROUGH = {  # command -> (module, argv prefix)
    "expand": ("crossslice.cross.graph_cli", ["expand"]),
    "graph": ("crossslice.cross.graph_cli", []),
    "explore": ("crossslice.cross.graph_server", []),
    "mcp": ("crossslice.cross.mcp_server", []),
}


def _is_rev(root: str, word: str) -> bool:
    return subprocess.run(["git", "-C", root, "rev-parse", "--verify", "-q",
                           f"{word}^{{commit}}"], capture_output=True).returncode == 0


def cmd_enrich(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="crossslice enrich",
        usage="crossslice enrich [REV] [-C DIR] [options]",
        description="Commit context: the change of REV (default HEAD) against its first "
                    "parent, merged with its intra-procedural def-use slice, plus the "
                    "callees, callers and macros it touches. Needs a git repository. "
                    "The older form `crossslice enrich <repo> <rev>` still works.")
    ap.add_argument("positional", nargs="*", metavar="REV", help=argparse.SUPPRESS)
    ap.add_argument("-C", "--repo", dest="repo_opt", metavar="DIR",
                    help="repository directory (default: the current directory)")
    ap.add_argument("--parent", metavar="REV",
                    help="compare against this revision instead of the first parent")
    ap.add_argument("--no-cross", action="store_true", help="intra-procedural slice only")
    ap.add_argument("--slice-level", type=int, default=2, metavar="N",
                    help="def-use slice depth (default 2)")
    ap.add_argument("--cross-slice-level", type=int, default=2, metavar="N",
                    help="slice depth inside expanded callees and callers (default 2)")
    ap.add_argument("-o", "--out", metavar="FILE", help="write the result here instead of stdout")
    ap.add_argument("-v", "--verbose", action="store_true", help="show the analysis log on stderr")
    ap.add_argument("--cache-dir", metavar="DIR", default=None,
                    help="cache root (default: ~/.cache/crossslice)")
    a = ap.parse_args(argv)

    from crossslice.paths import find_workspace, NO_GIT
    pos = list(a.positional)
    if len(pos) > 2:
        ap.error("expected at most a revision (optionally preceded by a repository directory)")
    repo, rev = a.repo_opt, None
    if len(pos) == 2:
        repo, rev = pos
    elif len(pos) == 1:
        here = find_workspace()
        if os.path.isdir(pos[0]) and not (here.is_git and _is_rev(here.git_root, pos[0])):
            repo = pos[0]
        else:
            rev = pos[0]
    try:
        ws = find_workspace(repo)
    except FileNotFoundError as e:
        print(f"crossslice enrich: {e}", file=sys.stderr)
        return 2
    if not ws.is_git:
        print(f"crossslice enrich: {ws.root}: {NO_GIT}", file=sys.stderr)
        return 2

    from crossslice.commit import enrich_commit
    try:
        res = enrich_commit(ws.git_root, rev or "HEAD", parent=a.parent, cross=not a.no_cross,
                            slice_level=a.slice_level, cross_slice_level=a.cross_slice_level,
                            log=sys.stderr if a.verbose else None, cache_dir=a.cache_dir)
    except ValueError as e:
        print(f"crossslice enrich: {e}", file=sys.stderr)
        return 2
    except FileNotFoundError as e:  # GumTree / Java / gtags missing
        print(f"crossslice enrich: {e}\nRun `crossslice check` to see what is missing.",
              file=sys.stderr)
        return 1
    head = f"{res.commit[:12]} vs {res.parent[:12]}"
    if res.note:
        print(f"{head}: {res.note}", file=sys.stderr)
    if res.cross_error:
        print(f"{head}: cross-function step failed ({res.cross_error}); "
              f"showing the intra-procedural result", file=sys.stderr)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(res.text)
        print(f"{head}: {len(res.text)} chars in {res.seconds:.1f}s -> {a.out}", file=sys.stderr)
    else:
        sys.stdout.write(res.text)
        if res.text and not res.text.endswith("\n"):
            sys.stdout.write("\n")
    if res.cross_stats:
        print(f"cross-function resolution: {res.cross_stats}", file=sys.stderr)
    return 0


def cmd_dataset(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="crossslice dataset",
                                 description="Batch enrichment over a JSONL dataset "
                                             "(fields: project_url, commit_id).")
    ap.add_argument("dataset")
    ap.add_argument("--repos-dir", default="./repos", help="clone cache (default ./repos)")
    ap.add_argument("--out-dir", default="./outputs", help="one .txt per commit (default ./outputs)")
    ap.add_argument("--no-cross", action="store_true")
    ap.add_argument("--slice-level", type=int, default=2)
    ap.add_argument("--cross-slice-level", type=int, default=2)
    a = ap.parse_args(argv)
    from crossslice.commit import enrich_dataset
    ok = fail = 0
    for entry, res, path in enrich_dataset(a.dataset, a.repos_dir, a.out_dir, cross=not a.no_cross,
                                           slice_level=a.slice_level,
                                           cross_slice_level=a.cross_slice_level):
        sha = entry.get("commit_id", "?")[:12]
        if isinstance(res, Exception):
            fail += 1
            print(f"FAIL {sha}: {res}", file=sys.stderr)
        else:
            ok += 1
            extra = f" (cross-function failed: {res.cross_error})" if res.cross_error else ""
            print(f"ok   {sha}: {len(res.text)} chars, {res.seconds:.1f}s -> {path}{extra}",
                  file=sys.stderr)
    print(f"{ok} enriched, {fail} failed", file=sys.stderr)
    return 1 if fail and not ok else 0


def cmd_context(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="crossslice context",
        description="Code context for a point in the code: the function containing "
                    "FILE:LINE, its read/write summary, its callees as one-line summaries "
                    "(macros as their #define), its callers with call-site lines, and the "
                    "project types it uses. Works in any directory of C sources; --rev "
                    "needs git.")
    ap.add_argument("location", help="FILE:LINE — a .c/.h file and a 1-based line number")
    ap.add_argument("-C", "--repo", dest="repo_opt", metavar="DIR",
                    help="repository root (default: the git top level containing FILE, "
                         "else the current directory)")
    ap.add_argument("--rev", metavar="REV",
                    help="analyze this revision (in a temporary worktree) instead of the files on disk")
    ap.add_argument("--slice", action="store_true", help="also show the def-use slice around LINE")
    ap.add_argument("--slice-level", type=int, default=2, metavar="N", help="slice depth (default 2)")
    ap.add_argument("--callees", type=int, default=30, metavar="N", help="max callees shown (default 30)")
    ap.add_argument("--callers", type=int, default=8, metavar="N",
                    help="max reference sites followed (default 8)")
    ap.add_argument("--types", type=int, default=6, metavar="N", help="max type definitions shown (default 6)")
    ap.add_argument("--cache-dir", metavar="DIR", default=None,
                    help="cache root (default: ~/.cache/crossslice)")
    a = ap.parse_args(argv)
    path, sep, line = a.location.rpartition(":")
    if not sep or not line.isdigit() or not path:
        print("crossslice context: location must be FILE:LINE, e.g. src/inflate.c:770",
              file=sys.stderr)
        return 2
    abs_path = os.path.abspath(path)
    if not os.path.isfile(abs_path):
        print(f"crossslice context: {path}: no such file", file=sys.stderr)
        return 2

    from crossslice.paths import find_workspace, git_toplevel, NO_GIT
    if a.repo_opt:
        ws = find_workspace(a.repo_opt)
    else:
        top = git_toplevel(os.path.dirname(abs_path))
        if top:
            ws = find_workspace(top)
        else:  # not in git: the current directory if FILE is below it, else FILE's directory
            cwd = os.getcwd()
            inside = not os.path.relpath(abs_path, cwd).startswith("..")
            ws = find_workspace(cwd if inside else os.path.dirname(abs_path))
    root = ws.root
    rel = os.path.relpath(abs_path, root)
    if rel.startswith(".."):
        print(f"crossslice context: {path} is outside the repository root {root}", file=sys.stderr)
        return 2
    if a.rev and not ws.is_git:
        print(f"crossslice context: {root}: {NO_GIT}; --rev needs git", file=sys.stderr)
        return 2
    if not ws.is_git:
        print(f"note: {root}: {NO_GIT}", file=sys.stderr)

    import contextlib
    from crossslice.cross.graph import RepoGraph
    from crossslice.cross.context import context_at
    commit = None
    if a.rev:
        from crossslice.commit import resolve_commit
        try:
            commit = resolve_commit(root, a.rev)
        except ValueError as e:
            print(f"crossslice context: {e}", file=sys.stderr)
            return 2
    with contextlib.redirect_stdout(sys.stderr):
        g = RepoGraph(root, commit=commit, cache_dir=a.cache_dir)
    try:
        with contextlib.redirect_stdout(sys.stderr):
            try:
                res = context_at(g, rel, int(line), show_slice=a.slice, slice_level=a.slice_level,
                                 max_callees=a.callees, max_callers=a.callers, max_types=a.types)
            except FileNotFoundError as e:
                res = {"error": str(e)}
    finally:
        with contextlib.redirect_stdout(sys.stderr):
            g.close()
    if isinstance(res, dict):
        print(f"crossslice context: {res.get('error', 'unknown error')}", file=sys.stderr)
        return 1
    print(res)
    return 0


def _dir_size(path: str) -> int:
    total = 0
    for dirpath, _dirs, files in os.walk(path):
        for f in files:
            try:
                total += os.path.getsize(os.path.join(dirpath, f))
            except OSError:
                pass
    return total


def cmd_check(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="crossslice check",
                                 description="Check the external tools CrossSlice uses and "
                                             "show where it keeps its caches.")
    ap.add_argument("--cache-dir", metavar="DIR", default=None)
    a = ap.parse_args(argv)
    rows = []

    def tool(name, required, hint):
        path = shutil.which(name)
        rows.append((name, bool(path), required, path or hint))

    tool("git", True, "install git")
    tool("gtags", True, "GNU Global: apt install global | brew install global | scripts/setup_tools.sh")
    tool("global", True, "GNU Global (same package as gtags)")
    tool("clangd", False, "apt install clangd | brew install llvm (only used for ambiguous call targets)")
    tool("gcc", False, "apt install gcc (used to synthesize the compile database for clangd)")
    tool("java", True, "Java 17+ (GumTree runtime): apt install openjdk-21-jre-headless")
    from crossslice.paths import cache_root, find_gumtree, find_workspace
    gt = find_gumtree()
    rows.append(("gumtree", bool(gt), True,
                 gt or "unzip GumTree 4.0.0-beta3 into /opt/gumtree or ~/gumtree, or set GUMTREE_PATH "
                       "(scripts/setup_tools.sh)"))
    width = max(len(r[0]) for r in rows)
    missing = False
    for name, ok, required, info in rows:
        mark = "ok     " if ok else ("MISSING" if required else "absent ")
        print(f"{mark}  {name:<{width}}  {info}")
        missing |= (required and not ok)

    root = cache_root(a.cache_dir)
    size = _dir_size(root) if os.path.isdir(root) else 0
    print(f"cache    {root} ({size / 1e6:.1f} MB)")
    ws = find_workspace()
    print(f"here     {ws.root} " + ("(git repository: commit and code context)" if ws.is_git
                                    else "(not a git repository: code context only)"))
    print(f"python {sys.version.split()[0]}, crossslice {__version__}")
    if missing:
        print("required tools are missing: enrich/dataset/mcp need GumTree + Java; "
              "everything needs git + gtags/global", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    if argv[0] in ("-V", "--version"):
        print(f"crossslice {__version__}")
        return 0
    # options given before the command (`crossslice --cache-dir X expand f`) move after it
    lead = []
    while argv and argv[0] in ("-C", "--repo", "--cache-dir", "--rev", "--commit") and len(argv) > 1:
        lead += argv[:2]
        argv = argv[2:]
    if not argv:
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:] + lead
    from crossslice.paths import MissingTool
    try:
        if cmd == "enrich":
            return cmd_enrich(rest)
        if cmd == "dataset":
            return cmd_dataset(rest)
        if cmd == "context":
            return cmd_context(rest)
        if cmd == "check":
            return cmd_check(rest)
        if cmd in PASSTHROUGH:
            module, prefix = PASSTHROUGH[cmd]
            import importlib
            mod = importlib.import_module(module)
            return mod.main(prefix + rest) or 0
    except KeyboardInterrupt:
        print("interrupted", file=sys.stderr)
        return 130
    except MissingTool as e:
        print(f"crossslice: {e}", file=sys.stderr)
        return 1
    print(f"crossslice: unknown command {cmd!r}\n\n{USAGE}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
