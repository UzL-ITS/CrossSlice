"""
Context recall per token — a judge-free, model-agnostic measurement of how
efficiently each arm reaches the code that matters, computed from the saved
transcripts and the per-case relevant sets (eval/relevant_sets.py).

Relevant set per case: the definitions (file, line span) of the functions the
real fix touched, their direct callees and callers, and the project types they
use, in the pre-commit version. Walking a transcript turn by turn we track:

  seen     the model has the definition's text (a read window covering it,
           its source or sliced body, its one-line summary, or a neighborhood
           listing it)
  located  the model knows where it is (grep hit / resolve / expand listing)

and report, per arm: tokens and calls until 50 % / 80 % of the relevant set
is seen, final coverage, and retrieval precision (share of retrieved text that
belongs to a relevant definition). Seeded runs start with the target
functions already seen.

  uv run python -m eval.coverage                      # every agent_fix*.jsonl
  uv run python -m eval.coverage eval/results/agent_fix_qwen-..._seeded.jsonl
"""
import argparse, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SETS = "eval/results/relevant_sets.json"
ARMS = ("self", "tool", "semantic")
ARM_HEAD = {"Self-navigation": "self", "Tool": "tool", "Semantic": "semantic"}

TURN = re.compile(r"^### Turn (\d+)  _\(tok (\d+)\+(\d+)", re.M)
CALL = re.compile(r"^- `(\w+)\((.*?)\)` →\n\n```\n(.*?)\n```", re.S | re.M)
SUBMIT = re.compile(r"^- \*\*submit_fix\*\*", re.M)


def parse_args_str(s):
    out = {}
    for part in re.split(r", (?=\w+=)", s):
        if "=" in part:
            k, v = part.split("=", 1)
            out[k] = v
    return out


def split_arms(text):
    parts = re.split(r"^## (Self-navigation|Tool|Semantic) arm.*$", text, flags=re.M)
    arms = {}
    for i in range(1, len(parts), 2):
        arms[ARM_HEAD[parts[i]]] = parts[i + 1]
    return arms


def items_of(rel):
    """Flatten the relevant set into [(key, kind, file, start, end)]."""
    out = []
    for group in ("functions", "callees", "callers", "types"):
        for d in rel.get(group, []):
            out.append((f"{group}:{d['name']}", group, d["name"], d["file"], d["start"], d["end"]))
    return out


def analyze_arm(body, items, seeded, target_names):
    seen, located = set(), set()
    if seeded:
        for key, group, name, *_ in items:
            if group == "functions":
                seen.add(key)
    n = len(items) or 1
    cum_tok = 0
    calls = 0
    rel_chars = tot_chars = 0
    curve = [(0, 0, len(seen) / n, len(located) / n)]
    first_seen_call = None
    # walk turns in order; each turn block holds its calls
    turns = list(TURN.finditer(body))
    for ti, tm in enumerate(turns):
        cum_tok += int(tm.group(2)) + int(tm.group(3))
        block = body[tm.end(): turns[ti + 1].start() if ti + 1 < len(turns) else len(body)]
        for cm in CALL.finditer(block):
            calls += 1
            name, args, res = cm.group(1), parse_args_str(cm.group(2)), cm.group(3)
            tot_chars += len(res)
            hit_chars = 0
            if name == "read_file":
                path = args.get("path", "")
                try:
                    s0 = int(args.get("start_line", 1) or 1)
                except ValueError:
                    s0 = 1
                try:
                    e0 = int(args.get("end_line", s0 + 249) or s0 + 249)
                except ValueError:
                    e0 = s0 + 249
                for key, group, nm, f, a, b in items:
                    if f == path and s0 <= a <= e0:         # window covers the signature
                        seen.add(key); located.add(key)
                        hit_chars += min(b, e0) - max(a, s0) + 1
                hit_chars = min(len(res), hit_chars * 60)   # ~60 chars per line
            elif name in ("get_function_source", "get_sliced_body", "get_summary",
                          "get_type_definition"):
                nm = args.get("name", "")
                for key, group, n2, *_ in items:
                    if n2 == nm:
                        seen.add(key); located.add(key); hit_chars = len(res)
            elif name == "get_neighborhood":
                nm = args.get("name", "")
                names = {it[2] for it in items}
                if nm in names:
                    for key, group, n2, *_ in items:
                        if n2 == nm:
                            seen.add(key); located.add(key)
                # a neighborhood line "  name (file:line): ..." / "  name — file:line"
                # about a relevant item is relevant text; the rest is not
                block_lines = res.split("\n")
                for i, line in enumerate(block_lines):
                    m2 = re.match(r"  (\w+)\b", line)
                    if m2 and m2.group(1) in names and not line.startswith("    "):
                        for key, group, n2, *_ in items:
                            if n2 == m2.group(1):
                                seen.add(key); located.add(key)
                        hit_chars += len(line) + 1
                        # a type's indented body lines belong to it
                        j = i + 1
                        while j < len(block_lines) and block_lines[j].startswith("    "):
                            hit_chars += len(block_lines[j]) + 1
                            j += 1
                if nm in names:
                    hit_chars += sum(len(l) + 1 for l in block_lines[:2])
                hit_chars = min(hit_chars, len(res))
            elif name in ("resolve_symbol", "expand_function", "get_callers"):
                # navigation: tells where things are, is not context itself
                nm = args.get("name", "")
                for key, group, n2, f, a, b in items:
                    if n2 == nm or re.search(rf'"(name|caller)": "{re.escape(n2)}"', res):
                        located.add(key)
            elif name == "grep":
                for key, group, n2, f, a, b in items:
                    for hm in re.finditer(rf"^{re.escape(f)}:(\d+):", res, re.M):
                        if a <= int(hm.group(1)) <= b:
                            located.add(key)
            rel_chars += hit_chars
            if first_seen_call is None and len(seen) > (n if seeded else 0) * 0 and \
                    any(k.startswith(("callees", "callers", "types")) for k in seen):
                first_seen_call = calls
            curve.append((cum_tok, calls, len(seen) / n, len(located) / n))
    def tokens_to(frac):
        for tok, c, s, _ in curve:
            if s >= frac:
                return tok
        return None
    def calls_to(frac):
        for tok, c, s, _ in curve:
            if s >= frac:
                return c
        return None
    return {"n_items": len(items), "seen": len(seen) / n, "located": len(located) / n,
            "tokens": cum_tok, "calls": calls,
            "tok50": tokens_to(0.5), "tok80": tokens_to(0.8), "tok100": tokens_to(1.0),
            "calls50": calls_to(0.5), "calls80": calls_to(0.8), "calls100": calls_to(1.0),
            "precision": rel_chars / tot_chars if tot_chars else 0.0,
            "curve": curve}


def fix_relevant(items, transcript_text, target_names):
    """The narrower set: neighborhood items whose name occurs in the real fix
    (the diff is recorded at the top of every transcript), plus the targets."""
    m = re.search(r"```diff\n(.*?)\n```", transcript_text, re.S)
    if not m:
        return items
    idents = set(re.findall(r"[A-Za-z_]\w*", m.group(1)))
    return [it for it in items if it[2] in idents or it[2] in target_names]


def analyze_file(path, sets):
    recs = [json.loads(l) for l in open(path)]
    rows = []
    for r in recs:
        rel = sets.get(r["commit"])
        if not rel or not os.path.exists(r.get("transcript", "")):
            continue
        items = items_of(rel)
        if not items:
            continue
        text = open(r["transcript"]).read()
        arms = split_arms(text)
        narrow = fix_relevant(items, text, set(r["functions"]))
        for arm, body in arms.items():
            a = analyze_arm(body, items, bool(r.get("seed_source")), set(r["functions"]))
            b = analyze_arm(body, narrow, bool(r.get("seed_source")), set(r["functions"]))
            a.update(commit=r["commit"], repo=r["url"].split("/")[-1], arm=arm,
                     model=r.get("model", "?"), seeded=bool(r.get("seed_source")),
                     fix_seen=b["seen"], fix_tok50=b["tok50"], fix_tok100=b["tok100"],
                     fix_calls100=b["calls100"], fix_n=len(narrow),
                     fix_precision=b["precision"])
            rows.append(a)
    return rows


def _mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else float("nan")


def _median(xs):
    xs = sorted(x for x in xs if x is not None)
    return xs[len(xs) // 2] if xs else float("nan")


def report(rows, label):
    if not rows:
        print(f"{label}: no cases with relevant sets"); return
    print(f"\n{label}  (model {rows[0]['model']}, seeded={rows[0]['seeded']}, "
          f"cases={len({r['commit'] for r in rows})})")
    print(f"{'arm':9} {'nbhd seen':>9} {'located':>8} {'prec':>6} {'tok→80%':>9} {'reach80':>8} | "
          f"{'fix seen':>8} {'fix prec':>8} {'tok→all':>9} {'calls→all':>9} {'reach all':>9} | "
          f"{'tokens':>8} {'calls':>6}")
    for arm in ARMS:
        rs = [r for r in rows if r["arm"] == arm]
        if not rs:
            continue
        reach = sum(1 for r in rs if r["tok80"] is not None)
        reach_all = sum(1 for r in rs if r["fix_tok100"] is not None)
        print(f"{arm:9} {_mean([r['seen'] for r in rs]):>9.2f} "
              f"{_mean([r['located'] for r in rs]):>8.2f} "
              f"{_mean([r['precision'] for r in rs]):>6.2f} "
              f"{_median([r['tok80'] for r in rs]):>9,.0f} "
              f"{reach:>5}/{len(rs):<2} | "
              f"{_mean([r['fix_seen'] for r in rs]):>8.2f} "
              f"{_mean([r['fix_precision'] for r in rs]):>8.2f} "
              f"{_median([r['fix_tok100'] for r in rs]):>9,.0f} "
              f"{_median([r['fix_calls100'] for r in rs]):>9.1f} "
              f"{reach_all:>6}/{len(rs):<2} | "
              f"{_mean([r['tokens'] for r in rs]):>8,.0f} {_mean([r['calls'] for r in rs]):>6.1f}")
    print(f"  relevant set: neighborhood {_mean([r['n_items'] for r in rows]):.1f} items/case, "
          f"fix-relevant {_mean([r['fix_n'] for r in rows]):.1f} items/case")
    # paired: per case, tokens to 50% (only where both reach it)
    by = {}
    for r in rows:
        by.setdefault(r["commit"], {})[r["arm"]] = r
    for other in ("tool", "semantic"):
        pairs = [(v["self"], v[other]) for v in by.values() if "self" in v and other in v]
        both = [(a, b) for a, b in pairs if a["fix_tok100"] and b["fix_tok100"]]
        line = f"  fix-relevant set fully seen — only {other}: " \
               f"{sum(1 for a, b in pairs if b['fix_tok100'] is not None and a['fix_tok100'] is None)}, " \
               f"only self: {sum(1 for a, b in pairs if a['fix_tok100'] is not None and b['fix_tok100'] is None)}, " \
               f"both: {len(both)}, neither: " \
               f"{sum(1 for a, b in pairs if a['fix_tok100'] is None and b['fix_tok100'] is None)}"
        if both:
            ratios = sorted(b["fix_tok100"] / max(a["fix_tok100"], 1) for a, b in both)
            line += f"; paired {other}/self tokens→all: median {ratios[len(ratios)//2]:.2f}"
        print(line)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("results", nargs="*")
    ap.add_argument("--csv", default=None, help="write per-turn curves here")
    ap.add_argument("--sets", default=SETS, help="relevant sets file (default eval/results/relevant_sets.json)")
    a = ap.parse_args()
    sets = json.load(open(a.sets))
    files = a.results or sorted(glob.glob("eval/results/agent_fix*.jsonl"))
    all_rows = []
    for f in files:
        rows = analyze_file(f, sets)
        report(rows, os.path.basename(f))
        all_rows += rows
    if a.csv:
        with open(a.csv, "w") as fh:
            fh.write("model,seeded,commit,arm,cum_tokens,calls,seen,located\n")
            for r in all_rows:
                for tok, c, s, l in r["curve"]:
                    fh.write(f"{r['model']},{r['seeded']},{r['commit'][:10]},{r['arm']},{tok},{c},{s:.3f},{l:.3f}\n")
        print(f"\ncurves -> {a.csv}")


if __name__ == "__main__":
    main()
