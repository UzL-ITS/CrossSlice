"""
RQ4 replay: incremental graph maintenance vs. full rebuild.

Replays N consecutive first-parent commits of a repository in a scratch
worktree. After each commit the graph is brought up to date and a fixed query
workload runs: expand every function whose file changed in that commit
(1 level, both directions).

Two modes over the same commit sequence and workload:
  incremental — one persistent RepoGraph: update() (content-hash invalidation
                + `global -u`) then expand; cached analyses survive.
  rebuild     — fresh DB + full gtags index each commit (what eager tools do).

  uv run python -m eval.replay --repo acpica --n 40 --out eval/results/replay_acpica_v2.jsonl

Runs on the released package (crossslice.cross.graph.RepoGraph).

Output: one JSON line per (mode, commit) with timings and, per workload
function, the answer (callee and caller names with call lines) so that the
aggregate can check the incremental graph against the rebuilt one: the two
modes must give the same answers (E3b, equivalence), otherwise the speed-up
is bought with stale results.
"""

import argparse
import json
import os
import re
import statistics
import subprocess
import sys
import shutil
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crossslice.cross.graph import RepoGraph

REPOS_DIR = "./data/repos"


def sh(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def commit_chain(repo_dir, n):
    """The last n+1 first-parent commits on the default branch, oldest first."""
    r = sh(["git", "log", "--first-parent", "--format=%H", f"-n{n + 1}"], repo_dir)
    return list(reversed(r.stdout.split()))


def changed_functions(repo_dir, prev, commit, cap=5):
    """Function names from -U0 hunk headers of changed C files (workload proxy)."""
    r = sh(["git", "diff", "-U0", prev, commit, "--", "*.c", "*.h"], repo_dir)
    names = []
    for m in re.finditer(r"^@@ .* @@.*?(\w+)\s*\(", r.stdout, flags=re.M):
        if m.group(1) not in names:
            names.append(m.group(1))
    return names[:cap]


def run_mode(mode, repo_dir, chain, out):
    with tempfile.TemporaryDirectory(prefix=f"replay_{mode}_") as tmp:
        wt = os.path.join(tmp, "wt")
        subprocess.run(["git", "worktree", "add", "--detach", wt, chain[0]],
                       cwd=repo_dir, check=True, capture_output=True)
        db = os.path.join(tmp, "graph.db")
        cache = os.path.join(tmp, "cache")   # CrossSlice cache root, isolated per run
        g = RepoGraph(wt, db_path=db, cache_dir=cache) if mode == "incremental" else None
        try:
            for i in range(1, len(chain)):
                prev, commit = chain[i - 1], chain[i]
                workload = changed_functions(repo_dir, prev, commit)
                subprocess.run(["git", "checkout", "-q", commit], cwd=wt,
                               check=True, capture_output=True)
                rec = {"mode": mode, "i": i, "commit": commit[:12],
                       "workload": workload}
                t0 = time.time()
                if mode == "incremental":
                    upd = g.update()
                    rec["stale_nodes"] = upd["stale_nodes"]
                else:
                    # eager baseline: throw everything away (store, index, cache),
                    # rebuild from scratch
                    shutil.rmtree(cache, ignore_errors=True)
                    for f in (db, db + "-wal", db + "-shm"):
                        if os.path.exists(f):
                            os.remove(f)
                    g2 = RepoGraph(wt, db_path=db, cache_dir=cache)
                    g2.gtags.generate_gtags()
                    g2._gtags_ready = True
                    g = g2
                rec["t_maintain"] = time.time() - t0

                t0 = time.time()
                expanded = 0
                for fn in workload:
                    if g.expand(fn, levels=1) is not None:
                        expanded += 1
                rec["t_query"] = time.time() - t0
                rec["expanded"] = expanded
                rec["answers"] = {fn: answer(g, fn) for fn in workload}
                if mode == "rebuild":
                    rec["refs"] = {fn: references(g, fn) for fn in workload}
                rec["t_total"] = rec["t_maintain"] + rec["t_query"]
                out.write(json.dumps(rec) + "\n")
                out.flush()
                if mode == "rebuild":
                    g.close()
                    g = None
        finally:
            if g:
                g.close()
            subprocess.run(["git", "worktree", "remove", "--force", wt],
                           cwd=repo_dir, capture_output=True)


def answer(g, fn):
    """What a client would see for `fn` after the expansion: the callee and
    caller names with their call sites (sorted, deduplicated), or None when
    the name did not resolve."""
    hood = g.neighborhood(fn)
    if not hood:
        return None
    return {"callees": sorted({(c["name"], c.get("call_file"), c.get("call_line")) for c in hood["callees"]}),
            "callers": sorted({(c["name"], c.get("call_file"), c.get("call_line")) for c in hood["callers"]})}


def references(g, fn):
    """Every reference site of `fn` the index knows at this revision, as
    (rel file, 0-based line): the ground truth for caller edges."""
    out = set()
    for r in g.gtags.find_function_callers_detailed(fn) or []:
        out.add((os.path.relpath(r["file_path"], g.root), r["line_number"] - 1))
    return sorted(out)


def equivalence(recs, show=8):
    """E3b: per (commit, function) compare the incremental answer with the
    rebuilt one. `identical`: the same answer. `consistent`: callees
    identical and callers consistent — every caller site the rebuild found is
    there, and every caller site the incremental graph reports is a reference
    the index knows at this revision (the incremental graph may know *more*
    callers than a fresh graph, whose caller lookup is capped per function;
    what it must not do is keep a call that is gone). Returns (identical,
    consistent, total, mismatches)."""
    inc = {r["commit"]: r for r in recs if r["mode"] == "incremental"}
    reb = {r["commit"]: r for r in recs if r["mode"] == "rebuild"}
    identical = consistent = total = 0
    mismatches = []
    for commit, ri in inc.items():
        rr = reb.get(commit)
        if rr is None or "answers" not in ri or "answers" not in rr:
            continue
        for fn, a in ri["answers"].items():
            b = rr["answers"].get(fn)
            total += 1
            if a == b:
                identical += 1
                consistent += 1
                continue
            if a is None or b is None:
                mismatches.append((commit, fn, "resolved", a is not None, b is not None))
                continue
            ok = True
            ca, cb = {tuple(x) for x in a["callees"]}, {tuple(x) for x in b["callees"]}
            if ca != cb:
                ok = False
                mismatches.append((commit, fn, "callees", sorted(ca - cb), sorted(cb - ca)))
            sa = {(f, l) for _, f, l in a["callers"]}
            sb = {(f, l) for _, f, l in b["callers"]}
            refs = {tuple(x) for x in (rr.get("refs") or {}).get(fn, [])}
            if not sb <= sa or not sa <= refs:
                ok = False
                mismatches.append((commit, fn, "callers", sorted(sa - refs), sorted(sb - sa)))
            if ok:
                consistent += 1
    return identical, consistent, total, mismatches


def aggregate(path):
    recs = [json.loads(l) for l in open(path)]
    identical, consistent, total, mismatches = equivalence(recs)
    if total:
        print(f"equivalence  incremental == rebuild in {identical}/{total} queries "
              f"({100.0 * identical / total:.1f} %); consistent (callees equal, callers superset within the "
              f"index) {consistent}/{total} ({100.0 * consistent / total:.1f} %); {len(mismatches)} differing sides")
        for commit, fn, side, only_inc, only_reb in mismatches[:8]:
            what = "stale/unknown in incremental" if side == "callers" else "only incremental"
            print(f"  {commit} {fn} {side}: {what} {only_inc}  only rebuild {only_reb}")
    for mode in ("incremental", "rebuild"):
        rs = [r for r in recs if r["mode"] == mode]
        if not rs:
            continue
        tm = [r["t_maintain"] for r in rs]
        tq = [r["t_query"] for r in rs]
        tt = [r["t_total"] for r in rs]
        print(f"{mode:12s} n={len(rs)} maintain median={statistics.median(tm):.3f}s "
              f"query median={statistics.median(tq):.3f}s "
              f"total median={statistics.median(tt):.3f}s cum={sum(tt):.1f}s")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="acpica")
    ap.add_argument("--n", type=int, default=40)
    ap.add_argument("--out", default=None)
    ap.add_argument("--aggregate", default=None)
    args = ap.parse_args()
    if args.aggregate:
        aggregate(args.aggregate)
        return
    out_path = args.out or f"eval/results/replay_{args.repo}.jsonl"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    repo_dir = os.path.join(REPOS_DIR, args.repo)
    chain = commit_chain(repo_dir, args.n)
    print(f"replaying {len(chain) - 1} commits of {args.repo} "
          f"({chain[0][:10]} .. {chain[-1][:10]})", flush=True)
    with open(out_path, "w") as out:
        for mode in ("incremental", "rebuild"):
            t0 = time.time()
            run_mode(mode, repo_dir, chain, out)
            print(f"{mode}: {time.time() - t0:.1f}s wall", flush=True)
    print("\n== aggregate ==")
    aggregate(out_path)


if __name__ == "__main__":
    main()
