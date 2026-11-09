"""
CLI for the on-demand repository graph.

  crossslice expand <function> [--levels N] [--direction both|up|down]
                    [-C REPO] [--rev REV] [--dot FILE] [--json]
  crossslice graph update [-C REPO] [--rev REV]
  crossslice graph stats  [-C REPO] [--rev REV]

The repository defaults to the one containing the current directory. The
older form `crossslice expand <repo> <function>` still works.
"""

import argparse
import contextlib
import json
import sys
import time

from crossslice.paths import add_repo_args, workspace_from_args


def _print_neighborhood(hood, dt):
    node = hood["node"]
    print(f"{node['name']} — {node['file']}:{node['line'] + 1} "
          f"[{node['resolution_method']}] ({dt:.2f}s)")
    if node.get("summary"):
        s = node["summary"]
        print(f"  reads: {', '.join(s.get('params_read', [])) or '-'}; "
              f"writes: {', '.join(s.get('params_written', [])) or '-'}")
    print(f"  callees ({len(hood['callees'])}):")
    for c in hood["callees"]:
        print(f"    -> {c['name']} ({c['file']}:{c['line'] + 1}, {c['state']})")
    callers = hood["callers"]
    print(f"  callers ({len(callers)}):")
    seen = set()
    for c in callers:
        key = (c["name"], c["file"], c.get("call_line"))
        if key in seen:
            continue
        seen.add(key)
        site = f", call at line {c['call_line'] + 1}" if c.get("call_line") is not None else ""
        print(f"    <- {c['name']} ({c['file']}:{c['line'] + 1}{site})")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="crossslice", description="On-demand repository code graph")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_expand = sub.add_parser(
        "expand", prog="crossslice expand",
        usage="crossslice expand FUNCTION [-C DIR] [--rev REV] [--levels N] "
              "[--direction both|up|down] [--dot FILE] [--json]",
        help="expand a function's neighborhood",
        description="Resolve FUNCTION, analyze it, and list its callees and callers "
                    "(one ring per level). Results are cached, so repeated calls are fast.")
    p_expand.add_argument("names", nargs="+", metavar="FUNCTION",
                          help="function or macro name (an optional repository "
                               "directory may come first)")
    add_repo_args(p_expand, positional=False)
    p_expand.add_argument("--db", default=None, help=argparse.SUPPRESS)
    p_expand.add_argument("--levels", type=int, default=1, metavar="N",
                          help="rings to expand (default 1)")
    p_expand.add_argument("--direction", choices=["both", "up", "down"], default="both",
                          help="callers (up), callees (down) or both (default)")
    p_expand.add_argument("--dot", default=None, metavar="FILE",
                          help="also write the graph in Graphviz DOT format")
    p_expand.add_argument("--json", action="store_true", help="print the neighborhood as JSON")

    p_update = sub.add_parser("update", prog="crossslice graph update",
                              help="re-analyze functions in files that changed on disk")
    add_repo_args(p_update)
    p_update.add_argument("--db", default=None, help=argparse.SUPPRESS)

    p_stats = sub.add_parser("stats", prog="crossslice graph stats",
                             help="show the cached graph's size and location")
    add_repo_args(p_stats)
    p_stats.add_argument("--db", default=None, help=argparse.SUPPRESS)

    args = ap.parse_args(argv)
    repo = None
    if args.cmd == "expand":
        if len(args.names) > 2:
            p_expand.error("expected FUNCTION (optionally preceded by a repository directory)")
        if len(args.names) == 2:
            repo, args.function = args.names
        else:
            args.function = args.names[0]
    ws, sha = workspace_from_args(args, f"crossslice {args.cmd}", repo=repo)

    from crossslice.cross.graph import RepoGraph
    with contextlib.redirect_stdout(sys.stderr):
        g = RepoGraph(ws.root, commit=sha, db_path=args.db, cache_dir=args.cache_dir)
    try:
        if args.cmd == "expand":
            t0 = time.time()
            with contextlib.redirect_stdout(sys.stderr):
                g.expand(args.function, direction=args.direction, levels=args.levels)
            dt = time.time() - t0
            hood = g.neighborhood(args.function)
            if not hood.get("node"):
                with contextlib.redirect_stdout(sys.stderr):
                    sugg = g.gtags.suggest(args.function)
                msg = f"'{args.function}' has no definition in {ws.root}"
                if sugg:
                    msg += f". Did you mean: {', '.join(sugg[:5])}?"
                print(msg, file=sys.stderr)
                return 1
            if args.json:
                print(json.dumps(hood, indent=2, default=str))
            else:
                _print_neighborhood(hood, dt)
            if args.dot:
                with open(args.dot, "w") as f:
                    f.write(g.to_dot())
                print(f"DOT graph written to {args.dot}", file=sys.stderr)
        elif args.cmd == "update":
            with contextlib.redirect_stdout(sys.stderr):
                res = g.update()
            print(res)
        else:
            print(json.dumps(g.stats(), indent=2))
    finally:
        with contextlib.redirect_stdout(sys.stderr):
            g.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
