"""
E12 / E13 — external baselines on the inputs of E1 and E10 (added 2026-11-02).

  rescore         re-score stored caller files against a truth file, in place
  joern-time      per repository: Joern import (joern-parse, c2cpg) of one H100
                  commit's checkout — wall-clock and peak RSS — then one callers
                  query from the stored CPG; next to CrossSlice's cold/warm time
                  of the same commit from bench_h100.jsonl
  joern-callers   the 18 E10 cases: every call site of F at the parent revision
                  (cpg.call.nameExact(F): file, enclosing method, call line)
  global-callers  same cases, GNU Global alone (global -rx F; enclosing function
                  = nearest preceding definition from global -f; prototypes
                  filtered by a regex)
  cscope-callers  same cases, cscope -L -3 F ("functions calling this function")
  crossslice-callers  same cases, the tool's own get_callers (gtags references
                  attributed to their enclosing function by tree-sitter)
  report          two tables — function level (names, alias-aware, the E10
                  metric) and call-site level (file, line) — plus Joern import
                  time per repository next to CrossSlice's per-commit median

The truth is eval/cases_impact_all_v2.jsonl (eval/truth_sites.py): the call
sites the commit had to edit, attributed to their enclosing function without
any of the compared tools.

  uv run python -m eval.baselines joern-time --out eval/results/joern_time.jsonl
  uv run python -m eval.baselines joern-callers      # -> eval/results/callers_joern_v2.jsonl
  uv run python -m eval.baselines global-callers     # -> eval/results/callers_global_v2.jsonl
  uv run python -m eval.baselines cscope-callers     # -> eval/results/callers_cscope_v2.jsonl
  uv run python -m eval.baselines crossslice-callers # -> eval/results/callers_crossslice_v2.jsonl
  uv run python -m eval.baselines report

Every checkout is a detached scratch worktree under --work (default: a temp
dir), removed afterwards. Joern is expected at /opt/joern/joern-cli (or
$JOERN_HOME); the JVM heap is set with --heap (default 32g). Each command
appends to its --out file and skips finished entries, so a run resumes.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval.impact import score, match_names, _norm, _git  # noqa: E402

JOERN_HOME = os.environ.get("JOERN_HOME", "/opt/joern/joern-cli")
CASES = "eval/cases_impact_all_v2.jsonl"
H100 = "eval/results/bench_h100.sample.txt"
BENCH = "eval/results/bench_h100.jsonl"
OURS = "eval/results/callers_crossslice_v2.jsonl"
REPOS = ["zlib", "libexpat", "acpica", "ffmpeg", "php-src"]

CALLERS_SC = r'''
@main def exec(cpgFile: String, name: String, outFile: String) = {
  importCpg(cpgFile)
  val rows = cpg.call.nameExact(name)
    .map(c => s"${c.method.filename}\t${c.method.name}\t${c.method.lineNumber.getOrElse(-1)}\t${c.lineNumber.getOrElse(-1)}").dedup.l
  java.nio.file.Files.write(java.nio.file.Paths.get(outFile), rows.mkString("\n").getBytes("UTF-8"))
  println(s"call sites of $name: ${rows.size}")
}
'''


# ------------------------------------------------------------------ helpers

_RUSAGE_WRAPPER = r"""
import resource, subprocess, sys
rc = subprocess.call(sys.argv[2:])
open(sys.argv[1], "w").write(str(resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss))
sys.exit(rc)
"""


def _run(cmd, cwd=None, env=None, timeout=None):
    """Run a command; returns (returncode, wall seconds, peak RSS of the
    command's process tree in MB, stdout+stderr). The command runs under a
    tiny Python wrapper whose RUSAGE_CHILDREN counter is this run's alone —
    the caller's own counter is a running maximum over all its children.
    The wall time includes the wrapper's start (~30 ms)."""
    fd, rss_file = tempfile.mkstemp(prefix="rss-", suffix=".txt")
    os.close(fd)
    t0 = time.time()
    p = subprocess.run([sys.executable, "-I", "-c", _RUSAGE_WRAPPER, rss_file, *cmd], cwd=cwd, env=env,
                       capture_output=True, text=True, timeout=timeout)
    wall = time.time() - t0
    try:
        kb = int(open(rss_file).read().strip() or 0)
        peak_mb = kb / 1024.0 if kb else None
    except (OSError, ValueError):
        peak_mb = None
    finally:
        try:
            os.remove(rss_file)
        except OSError:
            pass
    return p.returncode, wall, peak_mb, (p.stdout or "") + (p.stderr or "")


def _worktree(repo, sha, work):
    d = os.path.join(work, f"wt-{os.path.basename(repo)}-{sha[:12]}")
    if os.path.isdir(d):
        subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", d], capture_output=True)
        shutil.rmtree(d, ignore_errors=True)
    subprocess.run(["git", "-C", repo, "worktree", "add", "--detach", d, sha], check=True, capture_output=True)
    return d


def _drop_worktree(repo, d):
    subprocess.run(["git", "-C", repo, "worktree", "remove", "--force", d], capture_output=True)
    shutil.rmtree(d, ignore_errors=True)


def _done(out, key):
    if not os.path.exists(out):
        return set()
    return {json.loads(l).get(key) for l in open(out) if l.strip()}


def _append(out, rec):
    with open(out, "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def _joern_env(heap):
    env = dict(os.environ)
    env["_JAVA_OPTIONS"] = f"-Xmx{heap}"
    return env


def _joern_version():
    """From the jar names (joern has no --version flag)."""
    lib = os.path.join(JOERN_HOME, "lib")
    if os.path.isdir(lib):
        for f in os.listdir(lib):
            m = re.match(r"io\.joern\.joern-cli-(.+)\.jar$", f)
            if m:
                return m.group(1)
    return "unknown"


def _joern_import(src_dir, cpg_path, heap, log, cwd):
    """joern-parse the directory into cpg_path. Returns (ok, wall, peak_mb).
    cwd is the scratch dir: joern writes its `workspace/` there."""
    cmd = [os.path.join(JOERN_HOME, "joern-parse"), src_dir, "--language", "c", "--output", cpg_path]
    rc, wall, peak, txt = _run(cmd, cwd=cwd, env=_joern_env(heap), timeout=6 * 3600)
    with open(log, "a") as fh:
        fh.write(f"$ {' '.join(cmd)}\n{txt}\n[rc={rc} wall={wall:.1f}s peak={peak}]\n")
    return rc == 0 and os.path.exists(cpg_path), wall, peak


def _joern_callers(cpg_path, name, heap, work, log):
    """Enclosing methods of all call sites of `name`. Returns (rows, wall)."""
    sc = os.path.join(work, "callers.sc")
    with open(sc, "w") as fh:
        fh.write(CALLERS_SC)
    out = os.path.join(work, f"callers-{name}.tsv")
    if os.path.exists(out):
        os.remove(out)
    cmd = [os.path.join(JOERN_HOME, "joern"), "--script", sc,
           "--param", f"cpgFile={cpg_path}", "--param", f"name={name}", "--param", f"outFile={out}"]
    rc, wall, _, txt = _run(cmd, cwd=work, env=_joern_env(heap), timeout=3600)
    with open(log, "a") as fh:
        fh.write(f"$ {' '.join(cmd)}\n{txt[-3000:]}\n[rc={rc} wall={wall:.1f}s]\n")
    rows = []
    if os.path.exists(out):
        for line in open(out):
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1]:
                nums = [int(x) if x.lstrip("-").isdigit() else -1 for x in parts[2:4]] + [-1, -1]
                rows.append({"file": parts[0], "function": parts[1], "fn_line": nums[0], "line": nums[1]})
    return rows, wall, rc == 0


def _hunk_functions(repo, sha):
    """Function names from the -U0 hunk headers of a commit (C files only)."""
    txt = _git(repo, "show", "--format=", "-U0", sha, "--", "*.c")
    names = []
    for line in txt.splitlines():
        m = re.match(r"^@@ .* @@\s*(.*)$", line)
        if not m:
            continue
        m2 = re.search(r"([A-Za-z_]\w*)\s*\(", m.group(1))
        if m2 and m2.group(1) not in names and m2.group(1) not in ("if", "for", "while", "switch", "return"):
            names.append(m2.group(1))
    return names


def _cases(path):
    return [json.loads(l) for l in open(path) if l.strip()]


def _rel(path, wt=None):
    """Tool output paths relative to the repository root, no leading ./"""
    if wt and path.startswith(wt.rstrip("/") + "/"):
        path = path[len(wt.rstrip("/")) + 1:]
    while path.startswith("./"):
        path = path[2:]
    return path


def _score_rec(c, pred, extra):
    """Function level: distinct names, alias-aware, one-to-one (the E10
    metric). Call-site level: (file, line) of every call the commit edited."""
    truth = [tuple(t) for t in c["truth"]]
    sc = score(pred, truth)
    tnames = []
    for _, fn in truth:
        if fn not in tnames:
            tnames.append(fn)
    pnames = []
    for p in pred:
        fn = _norm(p["function"])
        if fn and fn not in pnames:
            pnames.append(fn)
    mp, mt = match_names(pnames, tnames)
    sites_t = {(f, int(ln)) for f, ln, _ in c.get("truth_sites", [])}
    sites_p = {(p["file"], int(p["line"])) for p in pred if p.get("line", -1) and p.get("line", -1) > 0}
    tp_s = len(sites_t & sites_p)
    sp = tp_s / len(sites_p) if sites_p else 0.0
    sr = tp_s / len(sites_t) if sites_t else 0.0
    sc.update(sha=c["sha"], function=c["function"], repo=os.path.basename(c["repo"]),
              pred=pnames, missed=[fn for fn in tnames if fn not in mt],
              extra_pred=[fn for fn in pnames if fn not in mp],
              site_n_truth=len(sites_t), site_n_pred=len(sites_p), site_tp=tp_s,
              site_precision=sp, site_recall=sr, site_f1=2 * sp * sr / (sp + sr) if sp + sr else 0.0,
              site_missed=sorted(sites_t - sites_p), site_extra=sorted(sites_p - sites_t),
              pred_sites=sorted({(p["file"], p["function"], int(p.get("line", -1))) for p in pred}), **extra)
    return sc


def _print_case(tool, sc):
    print(f"{tool:10s} {sc['repo']:8s} {sc['function']:32s} fn P {sc['precision']:.2f} R {sc['recall']:.2f} "
          f"({sc['n_pred']}/{sc['n_truth']})  sites P {sc['site_precision']:.2f} R {sc['site_recall']:.2f} "
          f"({sc['site_n_pred']}/{sc['site_n_truth']})  missed={sc['missed'][:3]} extra={sc['extra_pred'][:3]}",
          flush=True)


# ------------------------------------------------------------------ E12a

def cmd_joern_time(a):
    sample = [l.split() for l in open(a.commits) if l.strip()]
    bench = {}
    if os.path.exists(a.bench):
        for l in open(a.bench):
            r = json.loads(l)
            bench[(r["repo"], r["commit"])] = r
    done = _done(a.out, "repo")
    version = _joern_version()
    print("joern:", version)
    work = a.work or tempfile.mkdtemp(prefix="crossslice-baselines-")
    os.makedirs(work, exist_ok=True)
    log = os.path.join(work, "joern_time.log")
    for repo in a.repos.split(","):
        if repo in done:
            print(f"{repo}: done"); continue
        row = next((s for s in sample if s[0] == repo), None)
        if not row:
            print(f"{repo}: not in {a.commits}"); continue
        sha = row[1]
        repo_dir = os.path.join("data/repos", repo)
        fns = _hunk_functions(repo_dir, sha)
        print(f"{repo} {sha[:12]} functions {fns[:3]} …", flush=True)
        wt = _worktree(repo_dir, sha, work)
        try:
            n_files, n_lines = 0, 0
            for root, _, files in os.walk(wt):
                for f in files:
                    if f.endswith((".c", ".h")):
                        n_files += 1
                        try:
                            with open(os.path.join(root, f), "rb") as fh:
                                n_lines += sum(1 for _ in fh)
                        except OSError:
                            pass
            reps = []
            for i in range(a.repeat):
                cpg = os.path.join(work, f"{repo}-{sha[:12]}.cpg.bin")
                if os.path.exists(cpg):
                    os.remove(cpg)
                ok, wall, peak = _joern_import(wt, cpg, a.heap, log, work)
                rec = {"import_ok": ok, "t_import": wall, "peak_rss_mb": peak,
                       "cpg_bytes": os.path.getsize(cpg) if ok else None}
                if ok and fns:
                    rows, qwall, qok = _joern_callers(cpg, fns[0], a.heap, work, log)
                    rec.update(query_function=fns[0], t_query=qwall, query_ok=qok, n_callers=len(rows))
                reps.append(rec)
                print(f"   run {i + 1}: import {wall:.1f}s peak {peak and round(peak)} MB"
                      f"{' query ' + format(rec.get('t_query', 0), '.1f') + 's' if 't_query' in rec else ''}", flush=True)
                if not a.keep_cpg and os.path.exists(cpg):
                    os.remove(cpg)
            b = bench.get((repo, sha), {})
            _append(a.out, {"repo": repo, "commit": sha, "joern_version": version, "heap": a.heap,
                            "n_c_h_files": n_files, "n_c_h_lines": n_lines, "runs": reps,
                            "crossslice_t_total_cold": b.get("t_total"), "crossslice_t_total_warm": b.get("t_total_warm"),
                            "crossslice_t_cross_cold": b.get("t_cross"), "crossslice_t_cross_warm": b.get("t_cross_warm")})
        finally:
            _drop_worktree(repo_dir, wt)
    print("done")


# ------------------------------------------------------------------ E12b / E13

def cmd_joern_callers(a):
    cases = _cases(a.cases)
    done = _done(a.out, "sha")
    version = _joern_version()
    print("joern:", version)
    work = a.work or tempfile.mkdtemp(prefix="crossslice-baselines-")
    os.makedirs(work, exist_ok=True)
    log = os.path.join(work, "joern_callers.log")
    for c in cases:
        if c["sha"] in done:
            continue
        prev = _git(c["repo"], "rev-parse", c["sha"] + "^").strip()
        wt = _worktree(c["repo"], prev, work)
        try:
            cpg = os.path.join(work, f"{os.path.basename(c['repo'])}-{prev[:12]}.cpg.bin")
            ok, wall, peak = _joern_import(wt, cpg, a.heap, log, work)
            rows, qwall, qok = ([], None, False)
            if ok:
                rows, qwall, qok = _joern_callers(cpg, c["function"], a.heap, work, log)
            # the function's own definition is not a caller unless it recurses
            pred = [dict(r, file=_rel(r["file"], wt)) for r in rows
                    if r["function"] != c["function"] or any(fn == c["function"] for _, fn in c["truth"])]
            sc = _score_rec(c, pred, {"tool": "joern", "joern_version": version, "import_ok": ok,
                                      "t_import": wall, "peak_rss_mb": peak, "t_query": qwall, "query_ok": qok})
            _print_case("joern", sc)
            _append(a.out, sc)
            if not a.keep_cpg and os.path.exists(cpg):
                os.remove(cpg)
        finally:
            _drop_worktree(c["repo"], wt)
    print("done")


_PROTO = re.compile(r"^\s*(?:[A-Za-z_]\w*[\s\*]+)+{name}\s*\([^;{{]*\)\s*;\s*$")


def _global_callers(wt, name):
    """GNU Global alone: references by name, enclosing function = nearest
    preceding function definition in the same file (global -f)."""
    rc, t_index, _, txt = _run(["gtags"], cwd=wt, timeout=3600)
    rc, t_q, _, refs = _run(["global", "-rx", name], cwd=wt, timeout=600)
    proto = re.compile(_PROTO.pattern.format(name=re.escape(name)))
    defs_cache = {}
    pred = []
    n_refs = 0
    for line in refs.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 4:
            continue
        _, lineno, path, code = parts
        n_refs += 1
        if proto.match(code):
            continue  # a prototype, not a use
        if path not in defs_cache:
            _, _, _, d = _run(["global", "-fx", path], cwd=wt, timeout=600)
            entries = []
            for dl in d.splitlines():
                dp = dl.split(None, 3)
                if len(dp) < 4:
                    continue
                dname, dline, _, dcode = dp
                if "(" in dcode and not dcode.lstrip().startswith("#"):
                    entries.append((int(dline), dname))
            defs_cache[path] = sorted(entries)
        enclosing = None
        for dline, dname in defs_cache[path]:
            if dline <= int(lineno):
                enclosing = dname
            else:
                break
        if enclosing and enclosing != name:
            pred.append({"file": _rel(path, wt), "function": enclosing, "line": int(lineno)})
    return pred, n_refs, t_index, t_q


def cmd_global_callers(a):
    cases = _cases(a.cases)
    done = _done(a.out, "sha")
    work = a.work or tempfile.mkdtemp(prefix="crossslice-baselines-")
    os.makedirs(work, exist_ok=True)
    for c in cases:
        if c["sha"] in done:
            continue
        prev = _git(c["repo"], "rev-parse", c["sha"] + "^").strip()
        wt = _worktree(c["repo"], prev, work)
        try:
            pred, n_refs, t_index, t_q = _global_callers(wt, c["function"])
            sc = _score_rec(c, pred, {"tool": "global", "n_refs": n_refs, "t_index": t_index, "t_query": t_q})
            _print_case("global", sc)
            _append(a.out, sc)
        finally:
            _drop_worktree(c["repo"], wt)
    print("done")


def _cscope_callers(wt, name):
    rc, t_index, _, txt = _run(["cscope", "-b", "-q", "-k", "-R"], cwd=wt, timeout=3600)
    rc, t_q, _, out = _run(["cscope", "-d", "-k", "-L", "-3", name], cwd=wt, timeout=600)
    pred = []
    for line in out.splitlines():
        parts = line.split(None, 3)
        if len(parts) < 3:
            continue
        path, fn, lineno = parts[0], parts[1], parts[2]
        if fn and fn != name and fn != "<global>":
            pred.append({"file": _rel(path, wt), "function": fn, "line": int(lineno) if lineno.isdigit() else -1})
    return pred, t_index, t_q, rc


def cmd_cscope_callers(a):
    cases = _cases(a.cases)
    done = _done(a.out, "sha")
    work = a.work or tempfile.mkdtemp(prefix="crossslice-baselines-")
    os.makedirs(work, exist_ok=True)
    for c in cases:
        if c["sha"] in done:
            continue
        prev = _git(c["repo"], "rev-parse", c["sha"] + "^").strip()
        wt = _worktree(c["repo"], prev, work)
        try:
            pred, t_index, t_q, rc = _cscope_callers(wt, c["function"])
            sc = _score_rec(c, pred, {"tool": "cscope", "t_index": t_index, "t_query": t_q, "rc": rc})
            _print_case("cscope", sc)
            _append(a.out, sc)
        finally:
            _drop_worktree(c["repo"], wt)
    print("done")


def cmd_crossslice_callers(a):
    """The tool's own get_callers at the parent revision (as eval/impact.py
    tool-eval), recorded with call lines so it scores at both levels."""
    import contextlib
    import io
    from crossslice.cross.graph import RepoGraph
    cases = _cases(a.cases)
    done = _done(a.out, "sha")
    for c in cases:
        if c["sha"] in done:
            continue
        prev = _git(c["repo"], "rev-parse", c["sha"] + "^").strip()
        t0 = time.time()
        with contextlib.redirect_stdout(io.StringIO()):
            g = RepoGraph(c["repo"], commit=prev)
            try:
                g._ensure_gtags()
                t_setup = time.time() - t0
                t1 = time.time()
                found = g.resolver.find_callers([c["function"]], g.gtags, max_callers_per_fn=200)
                t_q = time.time() - t1
            finally:
                g.close()
        pred = [{"file": s.rel_file, "function": s.caller_name, "line": s.line + 1}
                for s in found.get(c["function"], []) if s.caller_name]
        sc = _score_rec(c, pred, {"tool": "crossslice", "t_index": t_setup, "t_query": t_q})
        _print_case("crossslice", sc)
        _append(a.out, sc)
    print("done")


# ------------------------------------------------------------------ report

def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return float("nan")
    n = len(xs)
    return xs[n // 2] if n % 2 else (xs[n // 2 - 1] + xs[n // 2]) / 2


def _bench_medians(bench):
    """Per-repository median cold/warm total time of the E1 run."""
    by = {}
    if bench and os.path.exists(bench):
        for l in open(bench):
            r = json.loads(l)
            if r.get("status") == "ok" and r.get("t_total") is not None:
                by.setdefault(r["repo"], []).append((r["t_total"], r.get("t_total_warm")))
    return {k: (_median([a for a, _ in v]), _median([b for _, b in v]), len(v)) for k, v in by.items()}


def cmd_report(a):
    rows = {}
    files = {"CrossSlice get_callers": a.ours, "Joern (cpg.call)": a.joern,
             "GNU Global (-rx + -f)": a.global_, "cscope (-L -3)": a.cscope}
    for label, path in files.items():
        if path and os.path.exists(path):
            rows[label] = [json.loads(l) for l in open(path) if l.strip()]
    n_truth = {r["sha"]: r["n_truth"] for recs in rows.values() for r in recs}
    n_sites = {r["sha"]: r["site_n_truth"] for recs in rows.values() for r in recs}
    print(f"Callers of F at the parent revision, {len(n_truth)} cases, {sum(n_truth.values())} distinct caller names, "
          f"{sum(n_sites.values())} call sites (truth: eval/cases_impact_all_v2.jsonl)\n")
    print("function level (distinct names, alias-aware; the E10 metric):")
    print(f"{'tool':24s} {'n':>3s} {'prec':>6s} {'recall':>6s} {'F1':>6s} {'exact':>7s} {'t_setup':>8s} {'t_query':>8s}")
    for label, recs in rows.items():
        exact = sum(1 for r in recs if r["precision"] == 1.0 and r["recall"] == 1.0)
        t_i = _median([r.get("t_index", r.get("t_import")) for r in recs])
        t_q = _median([r.get("t_query") for r in recs])
        print(f"{label:24s} {len(recs):3d} {_mean([r['precision'] for r in recs]):6.2f} "
              f"{_mean([r['recall'] for r in recs]):6.2f} {_mean([r['f1'] for r in recs]):6.2f} "
              f"{exact:3d}/{len(recs):<3d} {t_i:8.1f} {t_q:8.2f}")
    print("\ncall-site level (file, line of every call the commit had to edit):")
    print(f"{'tool':24s} {'n':>3s} {'prec':>6s} {'recall':>6s} {'F1':>6s} {'exact':>7s} {'sites found':>12s}")
    for label, recs in rows.items():
        exact = sum(1 for r in recs if r["site_precision"] == 1.0 and r["site_recall"] == 1.0)
        print(f"{label:24s} {len(recs):3d} {_mean([r['site_precision'] for r in recs]):6.2f} "
              f"{_mean([r['site_recall'] for r in recs]):6.2f} {_mean([r['site_f1'] for r in recs]):6.2f} "
              f"{exact:3d}/{len(recs):<3d} {sum(r['site_tp'] for r in recs):5d}/{sum(r['site_n_truth'] for r in recs):<6d}")
    print("\nmisses and extras per tool (function level):")
    for label, recs in rows.items():
        miss = [(r["repo"], r["function"], m) for r in recs for m in r["missed"]]
        extra = [(r["repo"], r["function"], m) for r in recs for m in r["extra_pred"]]
        print(f"  {label}: missed {len(miss)} {[m for _, _, m in miss][:12]}")
        print(f"  {'':{len(label)}s}  extra  {len(extra)} {[m for _, _, m in extra][:12]}")
    if a.joern_time and os.path.exists(a.joern_time):
        med = _bench_medians(a.bench)
        qmed = {}
        for r in rows.get("Joern (cpg.call)", []):
            qmed.setdefault(r["repo"], []).append(r.get("t_query"))
        print("\nJoern import per revision vs CrossSlice per commit (seconds; CrossSlice covers both versions of a commit):")
        print(f"{'repo':9s} {'.c/.h':>6s} {'kLOC':>6s} {'import':>8s} {'peak MB':>8s} {'query':>7s} "
              f"{'CS median cold':>15s} {'CS median warm':>15s} {'n':>3s}")
        for l in open(a.joern_time):
            r = json.loads(l)
            runs = r["runs"]
            imp = _median([x["t_import"] for x in runs]); peak = max([x.get("peak_rss_mb") or 0 for x in runs]) or float("nan")
            q = _median([x.get("t_query") for x in runs] + qmed.get(r["repo"], []))
            cold, warm, n = med.get(r["repo"], (float("nan"), float("nan"), 0))
            print(f"{r['repo']:9s} {r['n_c_h_files']:6d} {r.get('n_c_h_lines', 0) / 1000:6.0f} {imp:8.1f} {peak:8.0f} {q:7.1f} "
                  f"{cold:15.1f} {warm:15.1f} {n:3d}")
        print("  query = one `joern --script` run: JVM start + CPG load + cpg.call query; peak = max over runs;\n"
              "  CS = CrossSlice full enrichment of one commit (E1 H100, per-repository median over n commits)")



# ------------------------------------------------------------------ rescore

_SCORE_KEYS = {"n_pred", "n_truth", "tp", "precision", "recall", "f1", "sha", "function", "repo", "pred",
               "missed", "extra_pred", "site_n_truth", "site_n_pred", "site_tp", "site_precision",
               "site_recall", "site_f1", "site_missed", "site_extra", "pred_sites"}


def cmd_rescore(a):
    """Re-score stored caller files (their `pred_sites`) against the current
    truth file, in place, without re-running the tools."""
    cases = {c["sha"]: c for c in map(json.loads, open(a.cases))}
    for path in a.results:
        recs = [json.loads(l) for l in open(path) if l.strip()]
        out = []
        for r in recs:
            pred = [{"file": f, "function": fn, "line": ln} for f, fn, ln in r["pred_sites"]]
            extra = {k: v for k, v in r.items() if k not in _SCORE_KEYS}
            out.append(_score_rec(cases[r["sha"]], pred, extra))
        with open(path, "w") as fh:
            for sc in out:
                fh.write(json.dumps(sc) + "\n")
        print(f"{path}: {len(out)} cases re-scored")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    def common(p):
        p.add_argument("--work", default=None, help="scratch dir for worktrees/CPGs (default: temp dir)")
        p.add_argument("--heap", default="32g")
        p.add_argument("--keep-cpg", action="store_true")

    t = sub.add_parser("joern-time"); common(t)
    t.add_argument("--repos", default=",".join(REPOS)); t.add_argument("--commits", default=H100)
    t.add_argument("--bench", default=BENCH); t.add_argument("--repeat", type=int, default=1)
    t.add_argument("--out", default="eval/results/joern_time.jsonl"); t.set_defaults(func=cmd_joern_time)
    for name, fn, out in (("joern-callers", cmd_joern_callers, "eval/results/callers_joern_v2.jsonl"),
                          ("global-callers", cmd_global_callers, "eval/results/callers_global_v2.jsonl"),
                          ("cscope-callers", cmd_cscope_callers, "eval/results/callers_cscope_v2.jsonl"),
                          ("crossslice-callers", cmd_crossslice_callers, "eval/results/callers_crossslice_v2.jsonl")):
        p = sub.add_parser(name); common(p)
        p.add_argument("--cases", default=CASES); p.add_argument("--out", default=out); p.set_defaults(func=fn)
    rs = sub.add_parser("rescore")
    rs.add_argument("results", nargs="+"); rs.add_argument("--cases", default=CASES); rs.set_defaults(func=cmd_rescore)
    r = sub.add_parser("report")
    r.add_argument("--ours", default=OURS); r.add_argument("--joern", default="eval/results/callers_joern_v2.jsonl")
    r.add_argument("--global", dest="global_", default="eval/results/callers_global_v2.jsonl")
    r.add_argument("--cscope", default="eval/results/callers_cscope_v2.jsonl")
    r.add_argument("--joern-time", default="eval/results/joern_time.jsonl"); r.add_argument("--bench", default=BENCH)
    r.set_defaults(func=cmd_report)
    a = ap.parse_args()
    a.func(a)


if __name__ == "__main__":
    main()
