"""
Impact-analysis benchmark with ground truth from git history.

A commit that changes the *arity* of a C function must update every call
site, so the functions edited in that commit are the true caller list at the
parent revision — ground truth that owes nothing to our resolver. Three uses:

  mine       find such commits in a full clone and record (function, file,
             old/new arity, true callers) -> eval/cases_impact.jsonl
  tool-eval  score the tool's own get_callers against the truth, no model
  run        the agent task: "F's signature is about to change; list every
             function that calls it" — arms self / tool / semantic, scored by
             precision/recall of the submitted list, plus tokens and calls
  report     tables

  uv run python -m eval.impact mine --repo data/repos/ffmpeg --n 8000
  uv run python -m eval.impact tool-eval
  uv run python -m eval.impact run --model openrouter:qwen/qwen3-coder-30b-a3b-instruct --budget 20000
  uv run python -m eval.impact report
"""
import argparse, asyncio, contextlib, io, json, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import eval._env  # noqa
from eval import providers

CASES = "eval/cases_impact.jsonl"
CASES_V2 = "eval/cases_impact_all_v2.jsonl"      # parser-independent truth, see eval/truth_sites.py
TOOL_RESULTS = "eval/results/impact_tool.jsonl"
TRANSCRIPTS = "eval/results/agent_transcripts"
_KW = {"if", "while", "for", "switch", "return", "sizeof", "else", "do", "case"}


def _git(repo, *args, text=True):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=text, errors="replace").stdout


# ------------------------------- mining -------------------------------------

def _paren_args(s, start):
    """Content of the balanced parentheses starting at s[start]=='('; None if unbalanced."""
    depth = 0
    for i in range(start, len(s)):
        if s[i] == "(":
            depth += 1
        elif s[i] == ")":
            depth -= 1
            if depth == 0:
                return s[start + 1:i]
    return None


def _arity(args):
    a = re.sub(r"/\*.*?\*/", "", args or "", flags=re.S).strip()
    if a in ("", "void"):
        return 0
    if "..." in a:
        return -1                              # variadic: skip
    depth, n = 0, 1
    for ch in a:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        elif ch == "," and depth == 0:
            n += 1
    return n


_DEF_RE = re.compile(r"(?<![\w.>])([A-Za-z_]\w*)\s*\(")


def _def_headers(text):
    """{name: arity} for function-definition-looking headers in a block of
    removed (or added) diff lines: `type NAME(params) {` possibly multi-line,
    not a call (a type token precedes NAME) and not a prototype (`;`)."""
    out = {}
    joined = _strip_comments(text)
    for m in _DEF_RE.finditer(joined):
        name = m.group(1)
        if name in _KW:
            continue
        before = joined[max(0, m.start() - 80):m.start()]
        # a definition header has a type-ish token before the name at line start
        line_start = before.rfind("\n") + 1
        prefix = before[line_start:]
        if not re.search(r"(^|\s|\*)(\w+)\s*\*?\s*$", prefix) or re.search(r"[=(,+\-]\s*$", prefix):
            continue
        if re.match(r"\s*(return|else|case|goto)\b", prefix):
            continue
        args = _paren_args(joined, m.end() - 1)
        if args is None:
            continue
        after = joined[m.end() - 1 + len(args) + 2: m.end() - 1 + len(args) + 40]
        if re.match(r"\s*;", after):            # prototype
            continue
        if not re.match(r"\s*(\{|$|\n)", after) and "{" not in after.split("\n")[0] + after.split("\n")[1] if "\n" in after else True:
            pass
        out[name] = _arity(args)
    return out


def _hunks(diff_text):
    """Yield (path, [(line_no, kind, text)]) from a -U0 unified diff; the
    line number is in the NEW file for '+' lines and in the OLD file for '-'."""
    path, lines = None, []
    cur_new = cur_old = 0
    for line in diff_text.split("\n"):
        if line.startswith("+++ "):
            if path and lines:
                yield path, lines
            path = line[6:] if line.startswith("+++ b/") else line[4:]
            lines = []
        elif line.startswith("@@"):
            m = re.search(r"-(\d+)(?:,\d+)? \+(\d+)", line)
            cur_old, cur_new = (int(m.group(1)), int(m.group(2))) if m else (0, 0)
        elif path and line.startswith("+") and not line.startswith("+++"):
            lines.append((cur_new, "+", line[1:])); cur_new += 1
        elif path and line.startswith("-") and not line.startswith("---"):
            lines.append((cur_old, "-", line[1:])); cur_old += 1
    if path and lines:
        yield path, lines


def _strip_comments(text):
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.S)
    text = re.sub(r"//[^\n]*", " ", text)
    # continuation lines of block comments that the -U0 hunk cut open
    return "\n".join(l for l in text.split("\n") if not l.lstrip().startswith("*"))


def mine(repo, n, out, min_callers=3, min_files=2, max_per_repo=12):
    from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC
    shas = _git(repo, "log", "--format=%H", "--no-merges", f"-n{n}", "--", "*.c", "*.h").split()
    found, seen_fn = [], set()
    print(f"{repo}: scanning {len(shas)} commits", flush=True)
    for i, sha in enumerate(shas):
        if len(found) >= max_per_repo:
            break
        stat = _git(repo, "show", "--format=", "--numstat", sha)
        files = [l.split("\t")[2] for l in stat.split("\n") if l.count("\t") == 2]
        cfiles = [f for f in files if f.endswith((".c", ".h"))]
        if len(cfiles) < min_files or len(cfiles) > 40:
            continue
        diff = _git(repo, "show", "--format=", "-U0", "--diff-filter=M", sha, "--", "*.c", "*.h")
        # candidate: same function name defined with different arity in -/+ lines of one file
        cands = []
        for path, lines in _hunks(diff):
            old = "\n".join(t for _, k, t in lines if k == "-")
            new = "\n".join(t for _, k, t in lines if k == "+")
            do, dn = _def_headers(old), _def_headers(new)
            for name in set(do) & set(dn):
                if do[name] >= 0 and dn[name] >= 0 and do[name] != dn[name] and name not in seen_fn:
                    cands.append((name, path, do[name], dn[name]))
        if not cands:
            continue
        for name, dpath, a_old, a_new in cands:
            call_re = re.compile(rf"(?<![\w.>])\b{re.escape(name)}\s*\(")
            truth, parsers = set(), {}
            # truth = call sites that had to change, i.e. the REMOVED lines,
            # attributed to their enclosing function in the PARENT version —
            # the revision the tool is asked about
            for path, lines in _hunks(diff):
                for lineno, kind, text in lines:
                    if kind != "-" or not call_re.search(_strip_comments(text)):
                        continue
                    if re.match(r"\s*[\w\s\*]+\b" + re.escape(name) + r"\s*\(.*\)\s*;\s*$", text):
                        continue                     # prototype
                    if path not in parsers:
                        src = _git(repo, "show", f"{sha}^:{path}")
                        tmp = f"/tmp/impact_{os.getpid()}.c"
                        open(tmp, "w").write(src)
                        try:
                            parsers[path] = SourceCodeParserC(tmp)
                        except Exception:
                            parsers[path] = None
                    p = parsers[path]
                    if p is None:
                        continue
                    try:
                        node = p.find_function_containing_line(lineno - 1)
                    except Exception:
                        node = None
                    if node is None:
                        continue
                    decl = node.child_by_field_name("declarator")
                    m = re.search(r"(\w+)\s*\(", decl.text.decode("utf-8", "replace")) if decl else None
                    caller = m.group(1) if m else None
                    if caller and caller != name:
                        truth.add((path, caller))
            nfiles = len({p for p, _ in truth})
            if len(truth) >= min_callers and nfiles >= min_files:
                seen_fn.add(name)
                rec = {"repo": os.path.abspath(repo), "sha": sha, "function": name,
                       "file": dpath, "arity_old": a_old, "arity_new": a_new,
                       "truth": sorted(truth)}
                found.append(rec)
                print(f"  [{i}] {sha[:10]} {name} {a_old}->{a_new} params, "
                      f"{len(truth)} callers in {nfiles} files", flush=True)
    with open(out, "a") as fh:
        for r in found:
            fh.write(json.dumps(r) + "\n")
    print(f"{repo}: {len(found)} cases -> {out}")


# ---------------------------- scoring helpers -------------------------------

_MACRO_NAME = re.compile(r"^([A-Z_][A-Z0-9_]*)\s*\(([^()]*)\)$")


def _norm(name):
    """Canonical spelling of a submitted or true function name: `f`, or the
    macro form `PHP_METHOD(Phar, loadPhar)` for a macro-defined function."""
    s = (name or "").strip().strip("`").strip()
    m = _MACRO_NAME.match(s)
    if m:
        return f"{m.group(1)}({', '.join(a.strip() for a in m.group(2).split(','))})"
    return s.split("(")[0].strip()


def aliases(name):
    """Spellings (whitespace removed) that count as naming the function
    `name`. A macro-defined function also matches its expansion and the
    method-style spelling: PHP_METHOD(C, m) ~ zim_C_m ~ C::m,
    PHP_FUNCTION(f) ~ zif_f ~ f."""
    out = {re.sub(r"\s+", "", name)}
    m = _MACRO_NAME.match(name)
    if m:
        macro, args = m.group(1), [a.strip() for a in m.group(2).split(",")]
        if macro == "PHP_METHOD" and len(args) == 2:
            out |= {f"zim_{args[0]}_{args[1]}", f"{args[0]}::{args[1]}"}
        elif macro == "PHP_FUNCTION" and len(args) == 1:
            out |= {f"zif_{args[0]}", args[0]}
    return out


def match_names(pnames, tnames):
    """One-to-one, alias-aware matching of predicted to true names.
    Returns (matched predicted names, matched true names)."""
    talias = [(t, aliases(t)) for t in tnames]
    mp, mt = [], set()
    for fn in pnames:
        k = re.sub(r"\s+", "", fn)
        for t, al in talias:
            if t not in mt and k in al:
                mt.add(t); mp.append(fn)
                break
    return mp, mt


def score(pred, truth):
    """pred: [{function, file}] or names; truth: [(file, function)]. Match on
    the function name only (one-to-one, alias-aware, see aliases()); the file
    is informative. Names are deduplicated on both sides, so a caller defined
    in several files (init_filter in ten Vulkan filters) counts once."""
    tnames = []
    for _, fn in truth:
        if fn not in tnames:
            tnames.append(fn)
    pnames = []
    for p in pred or []:
        fn = _norm(p.get("function") if isinstance(p, dict) else str(p))
        if fn and fn not in pnames:
            pnames.append(fn)
    mp, mt = match_names(pnames, tnames)
    prec = len(mp) / len(pnames) if pnames else 0.0
    rec = len(mt) / len(tnames) if tnames else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return {"n_pred": len(pnames), "n_truth": len(tnames), "tp": len(mp),
            "precision": prec, "recall": rec, "f1": f1}


def rescore(results_path, cases_path, out_path):
    """Re-score a stored agent run — the submitted caller lists — against
    another truth file (eval/truth_sites.py builds one from the diffs)."""
    import ast
    cases = {c["sha"]: c for c in map(json.loads, open(cases_path))}
    rows = []
    for r in map(json.loads, open(results_path)):
        truth = [tuple(t) for t in cases[r["sha"]]["truth"]]
        r["n_truth"] = len({fn for _, fn in truth})
        r["cases"] = cases_path
        for arm in ("self", "tool", "semantic"):
            a = r.get(arm)
            if not a:
                continue
            sub = a.get("submission")
            if isinstance(sub, str):
                try:
                    sub = ast.literal_eval(sub)
                except (ValueError, SyntaxError):
                    sub = None
            a.update(score((sub or {}).get("callers") if isinstance(sub, dict) else None, truth))
        rows.append(r)
    with open(out_path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    print(f"{results_path} -> {out_path} ({len(rows)} cases, truth {cases_path})")
    return out_path


def cmd_rescore(a):
    outs = [rescore(f, a.cases, re.sub(r"\.jsonl$", "", f) + a.suffix + ".jsonl") for f in a.results]
    cmd_report(argparse.Namespace(results=outs))


# ----------------------------- tool-eval ------------------------------------

def tool_eval(cases_path, out):
    """Deterministic: get_callers(F) at the parent revision vs. history truth."""
    from crossslice.cross.graph import RepoGraph
    rows = []
    for c in map(json.loads, open(cases_path)):
        prev = _git(c["repo"], "rev-parse", c["sha"] + "^").strip()
        with contextlib.redirect_stdout(io.StringIO()):
            g = RepoGraph(c["repo"], commit=prev)
            try:
                g._ensure_gtags()
                found = g.resolver.find_callers([c["function"]], g.gtags, max_callers_per_fn=200)
            finally:
                g.close()
        pred = [{"function": s.caller_name, "file": s.rel_file}
                for s in found.get(c["function"], []) if s.caller_name]
        sc = score(pred, [tuple(t) for t in c["truth"]])
        sc.update(sha=c["sha"], function=c["function"], repo=os.path.basename(c["repo"]),
                  pred=[p["function"] for p in pred],
                  missed=[fn for _, fn in c["truth"] if fn not in {p["function"] for p in pred}],
                  extra=[p["function"] for p in pred if p["function"] not in {fn for _, fn in c["truth"]}])
        rows.append(sc)
        print(f"{sc['repo']:10} {c['function']:32} truth {sc['n_truth']:3} pred {sc['n_pred']:3} "
              f"P {sc['precision']:.2f} R {sc['recall']:.2f}  missed={sc['missed'][:4]} extra={sc['extra'][:4]}")
    with open(out, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    if rows:
        print(f"\nmean precision {sum(r['precision'] for r in rows)/len(rows):.3f}  "
              f"mean recall {sum(r['recall'] for r in rows)/len(rows):.3f}  "
              f"mean F1 {sum(r['f1'] for r in rows)/len(rows):.3f}  (n={len(rows)})")


# ------------------------------- agent task ---------------------------------

SUBMIT_CALLERS = {
    "name": "submit_callers",
    "description": "Submit the complete list of functions that call the target. "
                   "Call exactly once, when done.",
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "callers": {"type": "array", "items": {
                "type": "object",
                "properties": {"function": {"type": "string"}, "file": {"type": "string"}},
                "required": ["function", "file"], "additionalProperties": False}},
            "confidence_overall": {"type": "string", "enum": ["high", "medium", "low"]},
        },
        "required": ["callers", "confidence_overall"], "additionalProperties": False,
    },
}
_TASK = (
    "You are a C developer doing impact analysis. The signature of the function "
    "`{fn}` (defined in `{file}`) is about to change, so EVERY call site must be "
    "updated. List every function in this repository that calls `{fn}` — the "
    "enclosing function name and its file — nothing more, nothing less. Do not "
    "list prototypes, comments, or the definition itself. When you are sure the "
    "list is complete, call submit_callers exactly once."
)
SYS_SELF = ("You have generic repository tools: list files, read a file by line range, "
            "and grep (regular expressions over file contents).")
SYS_TOOL = ("You have generic repository tools (list/read/grep) AND semantic tools: "
            "get_callers(name, limit) returns the functions that call a symbol with "
            "their call sites (raise `limit` for widely used functions); "
            "get_neighborhood, resolve_symbol, get_function_source and others are "
            "available for detail.")
SYS_SEM = ("You have semantic tools only: get_callers(name, limit) returns the "
           "functions that call a symbol with their call sites (raise `limit` for "
           "widely used functions); get_neighborhood, resolve_symbol, "
           "get_function_source and others give detail. There is no grep.")


async def run_case(cfg, c, arms):
    import eval.agent_probe as ap
    from mcp import ClientSession
    from mcp.client.stdio import stdio_client
    from crossslice.cross.resolve import Worktree
    repo, sha = c["repo"], c["sha"]
    prev = _git(repo, "rev-parse", sha + "^").strip()
    run_tag = os.path.basename(cfg.out).replace(".jsonl", "")
    path = os.path.join(TRANSCRIPTS, f"{run_tag}_{os.path.basename(repo)}_{sha[:12]}.md")
    lg = ap.Logger(path, cfg.quiet)
    lg.file(f"# Impact-analysis transcript — {os.path.basename(repo)} @ {sha[:12]} — "
            f"{cfg.model}\n\n- target: `{c['function']}` ({c['file']}), arity "
            f"{c['arity_old']}->{c['arity_new']}\n- truth: {c['truth']}\n")
    rec = {"sha": sha, "repo": os.path.basename(repo), "function": c["function"],
           "n_truth": len(c["truth"]), "model": cfg.model, "budget": cfg.budget,
           "transcript": path}
    first = _TASK.format(fn=c["function"], file=c["file"])
    route = dict(provider_order=cfg.provider, provider_ignore=cfg.ignore_provider)
    truth = [tuple(t) for t in c["truth"]]

    def finish(arm, sub, st):
        sc = score((sub or {}).get("callers"), truth)
        lg.file(f"**Score ({arm}):** `{json.dumps(sc)}`\n")
        lg.term(f"    {arm:9} P {sc['precision']:.2f} R {sc['recall']:.2f} "
                f"({sc['n_pred']} listed, {sc['n_truth']} true)  {st['total']:,} tok, "
                f"{st['tool_calls']} calls, {st['stop']}")
        rec[arm] = {**{k: v for k, v in st.items() if k != "transcript"},
                    "submission": sub, **sc}

    try:
        with Worktree(repo, prev) as wo:
            fs = ap.RepoFS({"old": wo.path})
            if "self" in arms:
                lg.both("  [self arm]", "## Self-navigation arm\n")
                sess = providers.make_session(cfg.model, SYS_SELF, first, cfg.effort,
                                              ap.MAX_TOKENS, **route)
                sub, st = await ap.run_agent(sess, fs.schemas() + [SUBMIT_CALLERS],
                                             ap._fs_dispatch(fs), "submit_callers", lg,
                                             cfg.max_iters, cfg.budget)
                finish("self", sub, st)
            if "tool" in arms or "semantic" in arms:
                params = ap._server_params(repo, sha, lock="old")
                async with stdio_client(params, errlog=open(os.devnull, "w")) as (r, w):
                    async with ClientSession(r, w) as session:
                        await asyncio.wait_for(session.initialize(), timeout=60)
                        tools = ap._mcp_schemas((await session.list_tools()).tools, lock="old")
                        # warm the index before the clock starts
                        await asyncio.wait_for(session.call_tool(
                            "resolve_symbol", {"name": c["function"]}), timeout=ap.WARMUP_TIMEOUT)
                        if "tool" in arms:
                            lg.both("  [tool arm]", "## Tool arm\n")
                            sess = providers.make_session(cfg.model, SYS_TOOL, first,
                                                          cfg.effort, ap.MAX_TOKENS, **route)
                            sub, st = await ap.run_agent(
                                sess, fs.schemas() + tools + [SUBMIT_CALLERS],
                                ap._combined_dispatch(fs, session), "submit_callers", lg,
                                cfg.max_iters, cfg.budget)
                            finish("tool", sub, st)
                        if "semantic" in arms:
                            lg.both("  [semantic arm]", "## Semantic arm\n")
                            sess = providers.make_session(cfg.model, SYS_SEM, first,
                                                          cfg.effort, ap.MAX_TOKENS, **route)
                            sub, st = await ap.run_agent(
                                sess, tools + [SUBMIT_CALLERS], ap._mcp_dispatch(session),
                                "submit_callers", lg, cfg.max_iters, cfg.budget)
                            finish("semantic", sub, st)
    finally:
        lg.close()
    return rec


async def _run(args):
    import eval.agent_probe as ap
    args.provider = [p.strip() for p in args.provider.split(",")] if args.provider else None
    args.ignore_provider = ([p.strip() for p in args.ignore_provider.split(",")]
                            if args.ignore_provider else None)
    arms = [a.strip() for a in args.arms.split(",")]
    cases = [json.loads(l) for l in open(args.cases)]
    if args.n:
        cases = cases[:args.n]
    args.out = args.out or f"eval/results/impact_{providers.slug(args.model)}.jsonl"
    done = {json.loads(l)["sha"] for l in open(args.out)} if os.path.exists(args.out) else set()
    print(f"model {args.model} | arms {arms} | budget {args.budget} | {len(cases)} cases | -> {args.out}")
    with open(args.out, "a") as out:
        for i, c in enumerate(cases, 1):
            if c["sha"] in done:
                print(f"[{i}/{len(cases)}] {c['sha'][:10]} already done — skipped"); continue
            print(f"\n[{i}/{len(cases)}] {os.path.basename(c['repo'])} {c['function']} "
                  f"({len(c['truth'])} true callers) ...", flush=True)
            try:
                rec = await run_case(args, c, arms)
            except Exception as e:
                for leaf in ap._leaf_errors(e):
                    print(f"  error: {type(leaf).__name__}: {str(leaf)[:300]}")
                continue
            out.write(json.dumps(rec) + "\n"); out.flush()
    cmd_report(argparse.Namespace(results=[args.out]))


def cmd_report(args):
    import glob
    files = args.results or sorted(glob.glob("eval/results/impact_*.jsonl"))
    files = [f for f in files if os.path.basename(f) != "impact_tool.jsonl"]
    if os.path.exists(TOOL_RESULTS):
        rows = [json.loads(l) for l in open(TOOL_RESULTS)]
        print(f"\nTool alone (get_callers vs. history truth, n={len(rows)}): "
              f"precision {sum(r['precision'] for r in rows)/len(rows):.3f}  "
              f"recall {sum(r['recall'] for r in rows)/len(rows):.3f}  "
              f"F1 {sum(r['f1'] for r in rows)/len(rows):.3f}")
    for f in files:
        recs = [json.loads(l) for l in open(f)]
        if not recs:
            continue
        arms = [a for a in ("self", "tool", "semantic") if any(a in r for r in recs)]
        print(f"\n{f}  ({recs[0]['model']}, budget {recs[0].get('budget')}, n={len(recs)})")
        print(f"{'arm':9} {'prec':>6} {'recall':>7} {'F1':>6} {'R=1.0':>6} {'mean tok':>9} "
              f"{'median tok':>11} {'calls':>6} {'no sub':>7}")
        for arm in arms:
            rs = [r[arm] for r in recs if arm in r]
            n = len(rs)
            toks = sorted(r["total"] for r in rs)
            print(f"{arm:9} {sum(r['precision'] for r in rs)/n:>6.2f} "
                  f"{sum(r['recall'] for r in rs)/n:>7.2f} {sum(r['f1'] for r in rs)/n:>6.2f} "
                  f"{sum(1 for r in rs if r['recall'] >= 0.999):>3}/{n:<2} "
                  f"{sum(toks)/n:>9,.0f} {toks[n//2]:>11,} "
                  f"{sum(r['tool_calls'] for r in rs)/n:>6.1f} "
                  f"{sum(1 for r in rs if not r.get('submission')):>7}")
        print("\nper case:")
        print(f"{'repo':10} {'function':30} {'truth':>5}" + "".join(f" {a+' P/R':>12} {'tok':>7}" for a in arms))
        for r in recs:
            row = f"{r['repo']:10} {r['function'][:30]:30} {r['n_truth']:>5}"
            for a in arms:
                if a in r:
                    row += f" {r[a]['precision']:.2f}/{r[a]['recall']:.2f}   {r[a]['total']:>7,}"
            print(row)


def main():
    ap_ = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap_.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("mine"); m.add_argument("--repo", required=True); m.add_argument("--n", type=int, default=6000)
    m.add_argument("--out", default=CASES); m.add_argument("--max", type=int, default=12)
    m.set_defaults(func=lambda a: mine(a.repo, a.n, a.out, max_per_repo=a.max))
    t = sub.add_parser("tool-eval"); t.add_argument("--cases", default=CASES); t.add_argument("--out", default=TOOL_RESULTS)
    t.set_defaults(func=lambda a: tool_eval(a.cases, a.out))
    r = sub.add_parser("run")
    r.add_argument("--cases", default=CASES); r.add_argument("--n", type=int, default=0)
    r.add_argument("--model", default="anthropic:claude-sonnet-5-5")
    r.add_argument("--effort", default="high"); r.add_argument("--arms", default="self,tool,semantic")
    r.add_argument("--budget", type=int, default=20000); r.add_argument("--max-iters", type=int, default=16)
    r.add_argument("--provider", default=None); r.add_argument("--ignore-provider", default=None)
    r.add_argument("--out", default=None); r.add_argument("--quiet", action="store_true")
    r.set_defaults(func=lambda a: asyncio.run(_run(a)))
    p = sub.add_parser("report"); p.add_argument("results", nargs="*", default=None)
    p.set_defaults(func=cmd_report)
    rs = sub.add_parser("rescore", help="re-score stored agent runs against another truth file")
    rs.add_argument("results", nargs="+"); rs.add_argument("--cases", default=CASES_V2)
    rs.add_argument("--suffix", default="_v2truth"); rs.set_defaults(func=cmd_rescore)
    a = ap_.parse_args(); a.func(a)


if __name__ == "__main__":
    main()
