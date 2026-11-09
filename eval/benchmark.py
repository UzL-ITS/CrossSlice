"""
Per-commit benchmark of the released package (crossslice): latency, cascade
tiers, context sizes, slice fractions, and run-to-run stability.

Samples commits (from the repository history, or from the labeled dataset CSV
as in July 2026), runs the full pipeline (intra + cross-function, both program
versions) per commit with per-stage timers, and writes one JSON line per commit.

  uv run python -m eval.benchmark --sample history --per-repo 20 --out eval/results/bench_h100.jsonl
  uv run python -m eval.benchmark --commits eval/results/bench_h100.sample.txt --audit-lsp \
        --out eval/results/bench_h100_audit.jsonl
  uv run python -m eval.benchmark --sample dataset --per-repo 15 --out eval/results/bench_d45.jsonl
  uv run python -m eval.benchmark --aggregate eval/results/bench_h100.jsonl

Every commit is run twice: pass A with an empty cache (cold: the gtags index
and graph store are built from scratch, as on a fresh clone) and pass B with
the cache pass A left behind (warm). Pass B also checks that the texts are
identical (run-to-run stability). The texts of pass A are saved next to the
results (`<out>.texts/`).

Feeds Table I of the tool paper: latency, resolution rate and tier split, size
vs full functions, stability; and the limitations paragraph (slice fraction).
"""

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import random
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval._env  # noqa: F401,E402  (.env + GUMTREE_PATH)

# the released package (installed as an editable dependency of this project)
from crossslice.intra.github_loader import (get_previous_commit, get_changed_files,  # noqa: E402
                                            extract_file_from_commit)
from crossslice.intra.data_diff import create_diff  # noqa: E402
from crossslice.intra.parse_diff import parse_diff  # noqa: E402
from crossslice.intra.gen_dataflow import gen_dataflow  # noqa: E402
from crossslice.intra import general_code_analyzer as _gca  # noqa: E402
from crossslice.cross.enrich import CrossFunctionEnricher  # noqa: E402
from crossslice.cross.graph import ANALYSIS_VERSION  # noqa: E402
from crossslice.paths import repo_cache  # noqa: E402

REPOS_DIR = "./data/repos"
DATASET_CSV = "./data/c_full_dataset_new.csv"
HISTORY_DEPTH = 3000  # commits searched per repository for the history sample
LARGE_FUNCTIONS = 10_000  # chars of full function bodies: "large functions" subset


def _git(repo_dir, *args):
    return subprocess.run(["git", "-C", repo_dir, *args], capture_output=True,
                          text=True, errors="replace").stdout


def commit_exists(repo_dir, sha):
    return subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                          cwd=repo_dir, capture_output=True).returncode == 0


def local_repos():
    return sorted(d for d in os.listdir(REPOS_DIR)
                  if os.path.isdir(os.path.join(REPOS_DIR, d, ".git")))


def sample_dataset(per_repo, seed=42):
    """The July 2026 sample: per locally cloned repo, VFC-balanced rows of the
    labeled dataset CSV (deterministic)."""
    by_repo = defaultdict(list)
    for row in csv.DictReader(open(DATASET_CSV)):
        name = row["project_url"].rstrip("/").split("/")[-1].lower()
        if os.path.isdir(os.path.join(REPOS_DIR, name)):
            by_repo[name].append(row)
    rng = random.Random(seed)
    sampled = []
    for name, rows in by_repo.items():
        vfc = [r for r in rows if r["is_vfc"] == "True"]
        non = [r for r in rows if r["is_vfc"] != "True"]
        rng.shuffle(vfc)
        rng.shuffle(non)
        half = per_repo // 2
        for r in vfc[:half] + non[:per_repo - half]:
            sampled.append((name, r["commit_id"], "vfc" if r["is_vfc"] == "True" else "non-vfc"))
    return sampled


def sample_history(per_repo, seed=42, depth=HISTORY_DEPTH):
    """Non-merge commits touching at least one .c/.h file, drawn uniformly from
    the last `depth` such commits of every local repository."""
    rng = random.Random(seed)
    sampled = []
    for name in local_repos():
        shas = _git(os.path.join(REPOS_DIR, name), "log", "--no-merges", "--format=%H",
                    f"-n{depth}", "--", "*.c", "*.h").split()
        for sha in rng.sample(shas, min(per_repo, len(shas))):
            sampled.append((name, sha, "history"))
    return sampled


def read_commits(path):
    out = []
    for line in open(path):
        parts = line.split()
        if parts and not line.startswith("#"):
            out.append((parts[0], parts[1], parts[2] if len(parts) > 2 else ""))
    return out


def _sha(text):
    return hashlib.sha256((text or "").encode("utf-8", "replace")).hexdigest()[:16]


def _slice_stats(internals):
    """Statements of the merged lists over the changed functions: all,
    relevant (in the slice), changed (seeds)."""
    n = rel = changed = 0
    for blk in internals or []:
        for s in blk.get("merged", []):
            n += 1
            rel += bool(s.get("relevant_to_dataflow"))
            cs = s.get("change_status")
            changed += bool(cs and cs != "matched")
    return n, rel, changed


def _one_pass(repo_dir, prev, commit, files, work, cache_root, audit_lsp, rec, suffix):
    """Extract, diff, slice and enrich once. Fills rec[...] with timings,
    sizes, stats and texts (keys get `suffix`)."""
    old_dir = os.path.join(work, "old_version")
    new_dir = os.path.join(work, "new_version")
    for d in (old_dir, new_dir):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    t_start = time.time()
    for f in files:
        extract_file_from_commit(repo_dir, prev, f, os.path.join(old_dir, f))
        extract_file_from_commit(repo_dir, commit, f, os.path.join(new_dir, f))
    diff = create_diff(old_dir, new_dir, files)
    changes = parse_diff(diff, work, old_dir, new_dir, use_hungarian=True, debug_matching=False)
    rec["t_setup" + suffix] = time.time() - t_start

    t0 = time.time()
    intra_text, internals = gen_dataflow(changes, old_dir, new_dir, level=2,
                                         collect_internals=True)
    rec["t_intra" + suffix] = time.time() - t0

    t0 = time.time()
    cross1_text = cross2_text = ""
    if internals:
        enricher = CrossFunctionEnricher(
            repo_dir, prev, commit, cross_depth=2, audit_lsp=audit_lsp,
            cache_dir=repo_cache(repo_dir, cache_root) if cache_root else None)
        cross2_text, cross_json = enricher.enrich(internals)
        cross1_text = enricher.format_text(include_ring2=False)
        rec["cross_stats" + suffix] = (cross_json or {}).get("stats")
        rec["failures" + suffix] = enricher.resolution_failures
        if audit_lsp:
            rec["audit"] = enricher.lsp_audit
    rec["t_cross" + suffix] = time.time() - t0
    rec["t_total" + suffix] = time.time() - t_start

    texts = {"intra": intra_text or "",
             "inter1": (intra_text or "") + ("\n" + cross1_text if cross1_text else ""),
             "inter2": (intra_text or "") + ("\n" + cross2_text if cross2_text else "")}
    for k, t in texts.items():
        rec["sha_" + k + suffix] = _sha(t)
    return changes, internals, texts


def run_one(repo_name, commit, label, audit_lsp=False, texts_dir=None, warm=True):
    repo_dir = os.path.join(REPOS_DIR, repo_name)
    rec = {"repo": repo_name, "commit": commit, "label": label, "status": "ok",
           "engine": _gca._DEFUSE_ENGINE, "analysis_version": ANALYSIS_VERSION,
           "n_files": 0, "n_functions": 0,
           "size_diff_u3": 0, "size_full_functions": 0,
           "size_intra": 0, "size_inter1": 0, "size_inter2": 0,
           "lines_diff_u3": 0, "lines_full_functions": 0,
           "lines_intra": 0, "lines_inter1": 0, "lines_inter2": 0,
           "n_stmts": 0, "n_stmts_relevant": 0, "n_stmts_changed": 0}
    if not commit_exists(repo_dir, commit):
        rec["status"] = "commit_missing"
        return rec
    work = tempfile.mkdtemp(prefix="cs_bench_")
    cache_root = tempfile.mkdtemp(prefix="cs_bench_cache_")  # empty: pass A is cold
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            prev = get_previous_commit(repo_dir, commit)
            if not prev:
                rec["status"] = "no_parent"
                return rec
            files = [f for f in get_changed_files(repo_dir, prev, commit)
                     if f and f.endswith((".c", ".h"))]
            rec["n_files"] = len(files)
            if not files:
                rec["status"] = "no_c_files"
                return rec

            # pass A: cold
            changes, internals, texts = _one_pass(repo_dir, prev, commit, files, work,
                                                  cache_root, audit_lsp, rec, "")
            u3 = _git(repo_dir, "diff", "-U3", prev, commit, "--", *files)
            rec["size_diff_u3"], rec["lines_diff_u3"] = len(u3), u3.count("\n")
            full = []
            for details in changes.values():
                for fn in details.get("functions", {}).values():
                    full.append(fn.get("old_code") or "")
                    full.append(fn.get("new_code") or "")
            full_text = "\n".join(full)
            rec["size_full_functions"], rec["lines_full_functions"] = len(full_text), full_text.count("\n")
            rec["n_functions"] = len(internals or [])
            rec["n_stmts"], rec["n_stmts_relevant"], rec["n_stmts_changed"] = _slice_stats(internals)
            for k, t in texts.items():
                rec["size_" + k], rec["lines_" + k] = len(t), t.count("\n")
            if not internals:
                rec["status"] = "no_functions"  # only file-level changes
            if texts_dir:
                os.makedirs(texts_dir, exist_ok=True)
                for k, t in texts.items():
                    with open(os.path.join(texts_dir, f"{repo_name}-{commit[:12]}.{k}.txt"), "w") as f:
                        f.write(t)

            # pass B: warm cache, and the stability check
            if warm and not audit_lsp and internals:
                _one_pass(repo_dir, prev, commit, files, work, cache_root, False, rec, "_warm")
                rec["identical_warm"] = all(rec["sha_" + k] == rec["sha_" + k + "_warm"]
                                            for k in ("intra", "inter1", "inter2"))
    except Exception as e:
        rec["status"] = f"error: {type(e).__name__}: {e}"
        rec["log_tail"] = buf.getvalue()[-2000:]
    finally:
        shutil.rmtree(work, ignore_errors=True)
        shutil.rmtree(cache_root, ignore_errors=True)
    return rec


def _p(vals, q):
    vals = sorted(vals)
    return vals[min(len(vals) - 1, int(q * len(vals)))] if vals else float("nan")


def aggregate(path):
    recs = [json.loads(l) for l in open(path)]
    ok = [r for r in recs if r["status"] == "ok"]
    print(f"total={len(recs)} ok={len(ok)} "
          f"other={dict(Counter(r['status'].split(':')[0] for r in recs if r['status'] != 'ok'))}")
    if ok:
        print(f"engine={ok[0].get('engine')} analysis_version={ok[0].get('analysis_version')}")
    if not ok:
        return
    print("\nlatency (cold = empty cache; warm = second run, cache filled):")
    for key in ("t_setup", "t_intra", "t_cross", "t_total", "t_cross_warm", "t_total_warm"):
        vals = [r[key] for r in ok if r.get(key) is not None]
        if vals:
            print(f"  {key:13s} n={len(vals):3d} median={statistics.median(vals):6.2f}s "
                  f"mean={statistics.mean(vals):6.2f}s p90={_p(vals, 0.9):6.2f}s max={max(vals):6.2f}s")
    tiers = Counter()
    for r in ok:
        for version_stats in (r.get("cross_stats") or {}).values():
            tiers.update(version_stats)
    resolved_keys = ("gtags_unique", "gtags+ts", "lsp", "priority_fallback")
    total_resolved = sum(tiers.get(k, 0) for k in resolved_keys)
    print(f"\ncascade tiers (both versions): {dict(tiers)}")
    if total_resolved:
        for k in resolved_keys:
            print(f"  {k:18s} {tiers.get(k, 0):5d} ({100 * tiers.get(k, 0) / total_resolved:5.1f}% of resolved)")
        unres = tiers.get("unresolved", 0)
        print(f"  resolution rate: {100 * total_resolved / (total_resolved + unres):5.1f}% "
              f"of non-stdlib targets ({total_resolved}/{total_resolved + unres})")
    fail = Counter()
    for r in ok:
        fail.update((r.get("failures") or {}).values())
    if fail:
        print(f"  unresolved reasons: {dict(fail)}")

    sized = [r for r in ok if r.get("size_intra") and r.get("size_full_functions")]
    if sized:
        print(f"\ncontext size, n={len(sized)} (median chars / lines; ratio of medians vs full functions; "
              f"median paired ratio):")
        base = statistics.median(r["size_full_functions"] for r in sized) or 1
        for key in ("diff_u3", "full_functions", "intra", "inter1", "inter2"):
            med = statistics.median(r["size_" + key] for r in sized)
            lines = statistics.median(r["lines_" + key] for r in sized)
            paired = statistics.median(r["size_" + key] / r["size_full_functions"] for r in sized)
            print(f"  {key:15s} {med:8.0f} chars {lines:6.0f} lines  {med / base:5.2f}x  paired {paired:5.2f}")
        large = [r for r in sized if r["size_full_functions"] > LARGE_FUNCTIONS]
        if large:
            for key in ("intra", "inter1"):
                paired = statistics.median(r["size_" + key] / r["size_full_functions"] for r in large)
                print(f"  large functions (full > {LARGE_FUNCTIONS} chars, n={len(large)}): "
                      f"median paired {key}/full {paired:5.2f}")
        over = sum(1 for r in sized if r["size_inter1"] > r["size_full_functions"])
        print(f"  commits where inter1 exceeds the full functions: {over}/{len(sized)}")

    frac = [r["n_stmts_relevant"] / r["n_stmts"] for r in ok if r.get("n_stmts")]
    if frac:
        print(f"\nslice fraction (relevant / all statements of the changed functions), n={len(frac)}: "
              f"median {statistics.median(frac):.2f} p90 {_p(frac, 0.9):.2f} max {max(frac):.2f}; "
              f"changed statements median {statistics.median(r['n_stmts_changed'] for r in ok if r.get('n_stmts')):.0f}")

    warm = [r for r in ok if "identical_warm" in r]
    if warm:
        same = sum(1 for r in warm if r["identical_warm"])
        print(f"\nstability: texts identical between the cold and the warm run: {same}/{len(warm)}")
        for r in warm:
            if not r["identical_warm"]:
                print(f"  differs: {r['repo']} {r['commit'][:12]}")

    print("\nper repository (ok commits; median total s; median paired inter1/full):")
    for repo in sorted({r["repo"] for r in ok}):
        rs = [r for r in ok if r["repo"] == repo]
        rsz = [r for r in rs if r.get("size_full_functions")]
        paired = statistics.median(r["size_inter1"] / r["size_full_functions"] for r in rsz) if rsz else float("nan")
        print(f"  {repo:10s} n={len(rs):3d} total {statistics.median(r['t_total'] for r in rs):6.2f}s "
              f"inter1/full {paired:5.2f}")

    audit = Counter()
    disagreements = []
    for r in ok:
        for a in r.get("audit") or []:
            audit[a["verdict"]] += 1
            if a["verdict"] == "disagree":
                disagreements.append(a)
    if audit:
        decided = audit.get("agree", 0) + audit.get("disagree", 0)
        print(f"\nLSP agreement audit: {dict(audit)}"
              + (f" -> agreement {100 * audit.get('agree', 0) / decided:.1f}% "
                 f"where clangd answered ({decided} decisions)" if decided else ""))
        for d in disagreements[:10]:
            print(f"  disagree: {d['name']} cheap={d['cheap']} lsp={d['lsp']}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--sample", choices=["history", "dataset"], default="history")
    ap.add_argument("--per-repo", type=int, default=20)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--commits", default=None, metavar="FILE",
                    help="fixed list: lines `repo sha [label]` (overrides --sample)")
    ap.add_argument("--out", default="eval/results/bench.jsonl")
    ap.add_argument("--aggregate", default=None, metavar="JSONL",
                    help="only aggregate an existing results file")
    ap.add_argument("--audit-lsp", action="store_true",
                    help="cross-check cheap-tier resolutions with clangd (no warm pass)")
    ap.add_argument("--no-warm", action="store_true", help="skip pass B (no warm timings, no stability check)")
    ap.add_argument("--no-texts", action="store_true", help="do not save the enriched texts")
    args = ap.parse_args()

    if args.aggregate:
        aggregate(args.aggregate)
        return

    os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
    if args.commits:
        sampled = read_commits(args.commits)
    elif args.sample == "dataset":
        sampled = sample_dataset(args.per_repo, args.seed)
    else:
        sampled = sample_history(args.per_repo, args.seed)
    base = args.out[:-6] if args.out.endswith(".jsonl") else args.out
    with open(base + ".sample.txt", "w") as f:
        f.write("# repo sha label\n")
        for repo, sha, label in sampled:
            f.write(f"{repo} {sha} {label}\n")
    texts_dir = None if args.no_texts else base + ".texts"
    print(f"benchmarking {len(sampled)} commits ({dict(Counter(s[0] for s in sampled))}); "
          f"engine={_gca._DEFUSE_ENGINE} version={ANALYSIS_VERSION}", flush=True)
    with open(args.out, "w") as out:
        for i, (repo, commit, label) in enumerate(sampled, 1):
            rec = run_one(repo, commit, label, audit_lsp=args.audit_lsp,
                          texts_dir=texts_dir, warm=not args.no_warm)
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(f"[{i}/{len(sampled)}] {repo} {commit[:10]} {rec['status'][:60]} "
                  f"total={rec.get('t_total') and round(rec['t_total'], 2)}s "
                  f"warm={rec.get('t_total_warm') and round(rec['t_total_warm'], 2)}s "
                  f"inter1={rec.get('lines_inter1')} lines", flush=True)
    print("\n== aggregate ==")
    aggregate(args.out)


if __name__ == "__main__":
    main()
