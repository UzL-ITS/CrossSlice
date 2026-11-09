"""
RQ3 — LLM vulnerability-fix classification across context representations.

Central question of the report, tested with an LLM instead of a fine-tuned
model: does inter-procedural context help a model decide whether a commit
fixes a security vulnerability, where the raw diff (too little context) or the
full changed functions (more context, but unselected) do not? The model, the
prompt, and the sample are held fixed; ONLY the representation of each commit
varies. We measure accuracy / precision / recall / F1 and input tokens per
representation — i.e. accuracy per token.

Ground truth is the hand-labeled set in data/dataset_manual.json: ~200 commits
each classified independently by three people and consolidated into
`correct_label` (true = vulnerability-fixing commit). We compare the model's
answer against `correct_label`.

Representations (same five as the size study, eval/benchmark.py):
  diff        raw git diff (-U3)
  full        full changed functions (old+new)
  intra       intra-procedural enriched diff
  inter1      intra + cross-function ring 1 (sliced callees/callers/macros)
  inter2      inter1 + ring-2 summaries

The prompt gives the model ONLY the code — no repository name and no commit
message — so the decision rests on the change itself, which is exactly what the
representations differ on. The model returns a structured object (see
RESPONSE_SCHEMA): a yes/no/unknown verdict, the vulnerability categories fixed,
an overall confidence, and whether runtime verification would be needed.

Workflow (build offline, then one batch request at 50% cost):

  # 1. build the per-commit context artifacts + the exact request messages
  #    (no API key needed; clones/fetches each repo on demand):
  uv run python -m eval.llm_classify build

  # 2. submit one Message Batch (claude-sonnet-5) — 50% cheaper than
  #    per-request calls; prints an estimate and asks before spending:
  uv run python -m eval.llm_classify submit

  # 3. poll the batch and download results once it has ended
  #    (batches usually finish in well under an hour):
  uv run python -m eval.llm_classify fetch

  # 4. re-print the metrics table from the saved results at any time:
  uv run python -m eval.llm_classify report eval/results/llm_results.jsonl

Only `submit`/`fetch` need ANTHROPIC_API_KEY. Everything is resumable: `build`
skips commits already built, `fetch` can be run repeatedly until the batch ends.
"""

import argparse
import contextlib
import io
import json
import os
import re
import subprocess
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import eval._env  # noqa: F401,E402  (.env + GUMTREE_PATH bootstrap)

# the released package (installed as an editable dependency of this project)
from crossslice.intra.github_loader import (get_previous_commit, get_changed_files,
                                            extract_file_from_commit)
from crossslice.intra.data_diff import create_diff
from crossslice.intra.parse_diff import parse_diff
from crossslice.intra.gen_dataflow import gen_dataflow
from crossslice.cross.enrich import CrossFunctionEnricher


def delete_all_folder_and_files_in_dir(path):
    import shutil
    shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)

DATASET = "./data/dataset_manual.json"
REPOS_DIR = "./data/repos"              # existing full clones (ffmpeg, php-src, ...)
CACHE_DIR = "./data/repos_manual"       # on-demand partial clones for everything else
WORK_DIR = "./outputs_eval"

ARTIFACTS = "eval/results/llm_artifacts.jsonl"
BATCH_STATE = "eval/results/llm_batch.json"
RESULTS = "eval/results/llm_results.jsonl"

REPRESENTATIONS = ["diff", "full", "intra", "inter1", "inter2"]

MODEL = "claude-sonnet-5"

CATEGORIES = [
    "input_validation", "authn", "authz", "crypto", "dos",
    "injection_sql", "injection_cmd", "xss", "xxe", "ssrf",
    "path_traversal", "deserialization", "memory_safety",
    "race_condition", "idor", "privilege_escalation",
    "insecure_defaults", "information_disclosure",
    "prototype_pollution", "other",
]

SYSTEM_PROMPT = (
    "You are a security engineer triaging source-code changes. You are shown a "
    "single change from a C/C++ project in one of several context "
    "representations (a raw diff, the full changed functions, or a diff "
    "enriched with data-flow and cross-function context). You are deliberately "
    "NOT given the commit message or the repository name: judge only from the "
    "code itself.\n\n"
    "Decide whether the change is a VULNERABILITY-FIXING COMMIT — a change whose "
    "primary purpose is to fix a security vulnerability (e.g. memory safety, "
    "bounds/overflow, integer issues, input validation, injection, path "
    "traversal, authentication or authorization, race conditions, information "
    "disclosure) — as opposed to an ordinary bug fix, feature, refactor, test, "
    "or documentation change.\n\n"
    "Respond with a single JSON object and nothing else."
)

USER_TEMPLATE = (
    "Analyze the following code change and decide whether it fixes a security "
    "vulnerability. Base your decision only on the code shown.\n\n"
    "```\n{body}\n```"
)

# Structured-output schema (enforced by the Messages API). `notes` is optional;
# everything else is required.
RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "fixes_vulnerability": {"type": "string", "enum": ["yes", "no", "unknown"]},
        "fixed_categories": {"type": "array", "items": {"type": "string", "enum": CATEGORIES}},
        "confidence_overall": {"type": "string", "enum": ["high", "medium", "low"]},
        "needs_runtime_verification": {"type": "string", "enum": ["yes", "no"]},
        "notes": {"type": "string"},
    },
    "required": [
        "fixes_vulnerability", "fixed_categories",
        "confidence_overall", "needs_runtime_verification",
    ],
    "additionalProperties": False,
}


# --------------------------- repository resolution -------------------------

def _has_commit(repo_dir, sha):
    return subprocess.run(["git", "cat-file", "-e", f"{sha}^{{commit}}"],
                          cwd=repo_dir, capture_output=True).returncode == 0


def _slug(url):
    return re.sub(r"[^a-zA-Z0-9]+", "_", url).strip("_")[:80]


def resolve_repo(url, sha):
    """Find or create a local repo that contains `sha`; return its dir or None.

    Reuses an existing full clone under data/repos/ when it already has the
    commit; otherwise maintains a blobless partial clone per URL under
    data/repos_manual/ and fetches just the commit (+ its parent) on demand.
    GitHub serves arbitrary SHAs, so no full history download is needed.
    """
    name = url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    for cand in (os.path.join(REPOS_DIR, name.lower()), os.path.join(REPOS_DIR, name)):
        if os.path.isdir(cand) and _has_commit(cand, sha):
            return cand

    d = os.path.join(CACHE_DIR, _slug(url))
    if not os.path.isdir(os.path.join(d, ".git")):
        os.makedirs(d, exist_ok=True)
        subprocess.run(["git", "init", "-q"], cwd=d, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", url], cwd=d, capture_output=True)
    if not _has_commit(d, sha):
        # blobless + depth 2: commit and parent, blobs fetched lazily on access
        ok = subprocess.run(
            ["git", "fetch", "-q", "--depth", "2", "--filter=blob:none", "origin", sha],
            cwd=d, capture_output=True, text=True, timeout=600)
        if ok.returncode != 0:
            subprocess.run(["git", "fetch", "-q", "--depth", "2", "origin", sha],
                           cwd=d, capture_output=True, timeout=600)
    return d if _has_commit(d, sha) else None


# ----------------------------- build artifacts -----------------------------

def build_reps(repo_dir, commit):
    """Return {rep: body} for one commit. diff/full/intra are required; inter1/
    inter2 are best-effort (need a repo-wide index) and omitted on failure."""
    old_dir = os.path.abspath(os.path.join(WORK_DIR, "old_version"))
    new_dir = os.path.abspath(os.path.join(WORK_DIR, "new_version"))
    os.makedirs(old_dir, exist_ok=True)
    os.makedirs(new_dir, exist_ok=True)
    reps = {}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            prev = get_previous_commit(repo_dir, commit)
            if not prev:
                return None
            files = [f for f in get_changed_files(repo_dir, prev, commit)
                     if f.endswith((".c", ".h"))]
            if not files:
                return None
            for f in files:
                extract_file_from_commit(repo_dir, prev, f, os.path.join(old_dir, f))
                extract_file_from_commit(repo_dir, commit, f, os.path.join(new_dir, f))
            diff = create_diff(old_dir, new_dir, files)
            changes = parse_diff(diff, WORK_DIR, old_dir, new_dir,
                                 use_hungarian=True, debug_matching=False)
            intra_text, internals = gen_dataflow(changes, old_dir, new_dir,
                                                 level=2, collect_internals=True)

        reps["diff"] = subprocess.run(
            ["git", "diff", "-U3", prev, commit, "--", *files],
            cwd=repo_dir, capture_output=True, text=True, errors="replace").stdout
        full = []
        for d in changes.values():
            for fn in d.get("functions", {}).values():
                if fn.get("old_code"):
                    full.append(f"// old:\n{fn['old_code']}")
                if fn.get("new_code"):
                    full.append(f"// new:\n{fn['new_code']}")
        reps["full"] = "\n\n".join(full)
        reps["intra"] = intra_text or ""

        try:
            with contextlib.redirect_stdout(io.StringIO()):
                enricher = CrossFunctionEnricher(repo_dir, prev, commit, cross_depth=2)
                cross2, _ = enricher.enrich(internals)
                cross1 = enricher.format_text(include_ring2=False)
            reps["inter1"] = (intra_text or "") + "\n" + (cross1 or "")
            reps["inter2"] = (intra_text or "") + "\n" + (cross2 or "")
        except Exception as e:
            print(f"  cross-function skipped ({commit[:10]}): {e}", file=sys.stderr)
    except Exception as e:
        print(f"  build failed ({commit[:10]}): {e}", file=sys.stderr)
        return None
    finally:
        with contextlib.redirect_stdout(io.StringIO()):
            delete_all_folder_and_files_in_dir(old_dir)
            delete_all_folder_and_files_in_dir(new_dir)
            delete_all_folder_and_files_in_dir(os.path.join(WORK_DIR, "functions_code"))
    return reps or None


def load_dataset(github_only=True):
    rows = json.load(open(DATASET))
    out = []
    for r in rows:
        if r.get("correct_label") is None:
            continue
        url = r["project_url"]
        host = url.split("/")[2] if "://" in url else ""
        if github_only and host != "github.com":
            continue
        out.append(r)
    return out


def cmd_build(args):
    os.makedirs(os.path.dirname(ARTIFACTS), exist_ok=True)
    rows = load_dataset(github_only=not args.all_sources)
    if args.limit:
        rows = rows[: args.limit]

    done = set()
    if os.path.exists(ARTIFACTS):
        for line in open(ARTIFACTS):
            done.add(json.loads(line)["commit"])

    print(f"building artifacts for {len(rows)} commits -> {ARTIFACTS}"
          f" ({len(done)} already done)")
    kept = 0
    with open(ARTIFACTS, "a") as out:
        for i, r in enumerate(rows, 1):
            commit = r["commit_id"]
            if commit in done:
                continue
            repo_dir = resolve_repo(r["project_url"], commit)
            if repo_dir is None:
                print(f"[{i}/{len(rows)}] {r['project_url']} {commit[:10]} "
                      f"unavailable — skipped", file=sys.stderr)
                continue
            reps = build_reps(repo_dir, commit)
            if not reps:
                continue
            out.write(json.dumps({
                "idx": i, "url": r["project_url"], "commit": commit,
                "label": bool(r["correct_label"]), "reps": reps}) + "\n")
            out.flush()
            kept += 1
            print(f"[{i}/{len(rows)}] {commit[:10]} kept "
                  f"({', '.join(reps)})", flush=True)
    print(f"done: {kept} new commits built")


# ------------------------------- batch requests ----------------------------

def truncate(text, max_chars):
    if len(text) <= max_chars:
        return text
    head = int(max_chars * 0.7)
    return text[:head] + "\n... [truncated] ...\n" + text[-(max_chars - head):]


def build_params(body, max_chars):
    # claude-sonnet-5: adaptive thinking is on by default (thinking omitted);
    # effort "low" keeps it cheap. max_tokens leaves room so a little reasoning
    # can't crowd out the structured JSON (which would truncate to invalid).
    return {
        "model": MODEL,
        "max_tokens": 1024,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user",
                      "content": USER_TEMPLATE.format(body=truncate(body, max_chars))}],
        "output_config": {
            "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
            "effort": "low",
        },
    }


def iter_requests(commits, max_chars):
    """Yield (custom_id, meta, params) for every (commit, representation)."""
    for c in commits:
        for rep in REPRESENTATIONS:
            body = c["reps"].get(rep)
            if not body:
                continue
            cid = f"c{c['idx']:04d}_{rep}"
            meta = {"commit": c["commit"], "url": c["url"],
                    "rep": rep, "label": c["label"]}
            yield cid, meta, build_params(body, max_chars)


def cmd_submit(args):
    if not os.path.exists(ARTIFACTS):
        print(f"no artifacts at {ARTIFACTS} — run `build` first")
        return
    import anthropic
    from anthropic.types.message_create_params import MessageCreateParamsNonStreaming
    from anthropic.types.messages.batch_create_params import Request

    commits = [json.loads(l) for l in open(ARTIFACTS)]
    requests, mapping = [], {}
    total_chars = 0
    for cid, meta, params in iter_requests(commits, args.max_chars):
        requests.append(Request(custom_id=cid,
                                params=MessageCreateParamsNonStreaming(**params)))
        mapping[cid] = meta
        total_chars += len(params["messages"][0]["content"])

    print(f"{len(requests)} requests over {len(commits)} commits "
          f"(~{total_chars // 4:,} input tokens before prompt overhead)")
    print("Message Batches API bills at 50% of standard rates; most batches "
          "finish within the hour.")
    if not args.yes and input("submit batch? [y/N] ").strip().lower() != "y":
        print("aborted")
        return

    client = anthropic.Anthropic()
    batch = client.messages.batches.create(requests=requests)
    json.dump({"batch_id": batch.id, "model": MODEL, "mapping": mapping},
              open(BATCH_STATE, "w"))
    print(f"submitted batch {batch.id}\nstate saved to {BATCH_STATE}\n"
          f"poll with: uv run python -m eval.llm_classify fetch")


def cmd_fetch(args):
    if not os.path.exists(BATCH_STATE):
        print(f"no batch state at {BATCH_STATE} — run `submit` first")
        return
    import anthropic
    state = json.load(open(BATCH_STATE))
    client = anthropic.Anthropic()
    batch = client.messages.batches.retrieve(state["batch_id"])
    print(f"batch {batch.id}: {batch.processing_status} "
          f"({dict(batch.request_counts)})")
    if batch.processing_status != "ended":
        print("not finished yet — re-run `fetch` later")
        return

    mapping = state["mapping"]
    kept = 0
    with open(RESULTS, "w") as out:
        for result in client.messages.batches.results(batch.id):
            meta = mapping.get(result.custom_id)
            if meta is None or result.result.type != "succeeded":
                continue
            msg = result.result.message
            text = next((b.text for b in msg.content if b.type == "text"), "")
            try:
                pred = json.loads(text)
            except Exception:
                continue
            out.write(json.dumps({
                **meta,
                "model": state.get("model", MODEL),
                "fixes_vulnerability": pred.get("fixes_vulnerability"),
                "fixed_categories": pred.get("fixed_categories", []),
                "confidence_overall": pred.get("confidence_overall"),
                "needs_runtime_verification": pred.get("needs_runtime_verification"),
                "notes": pred.get("notes", ""),
                "input_tokens": msg.usage.input_tokens,
                "output_tokens": msg.usage.output_tokens,
            }) + "\n")
            kept += 1
    print(f"wrote {kept} results -> {RESULTS}")
    cmd_report(argparse.Namespace(results=RESULTS))


# --------------------------------- reporting -------------------------------

# Well-known, very-high-visibility projects — a proxy for "likely well
# represented in the model's training data". Used only for the memorization
# split in the report (famous vs. obscure accuracy).
FAMOUS = {
    "ffmpeg", "qemu", "linux", "chromium", "tensorflow", "wireshark",
    "imagemagick", "imagemagick6", "vim", "ruby", "perl5", "php-src",
    "openssl", "curl", "core", "media-tree", "libreoffice",
}


def _repo_name(url):
    n = url.rstrip("/").split("/")[-1]
    return (n[:-4] if n.endswith(".git") else n).lower()


def _is_correct(r):
    """Model's yes/no verdict vs. ground truth (unknown -> treated as 'no')."""
    return (r["fixes_vulnerability"] == "yes") == bool(r["label"])


def _metrics(rows, pos):
    """(n, acc, prec, rec, f1) for a predicate `pos(r)` = predicted positive."""
    n = len(rows)
    if not n:
        return 0, 0.0, 0.0, 0.0, 0.0
    tp = sum(1 for r in rows if r["label"] and pos(r))
    fp = sum(1 for r in rows if not r["label"] and pos(r))
    fn = sum(1 for r in rows if r["label"] and not pos(r))
    tn = sum(1 for r in rows if not r["label"] and not pos(r))
    acc = (tp + tn) / n
    prec = tp / (tp + fp) if tp + fp else 0.0
    rec = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
    return n, acc, prec, rec, f1


def _mcnemar(base, other):
    """Exact binomial McNemar test over commits present in both reps.
    Returns (b, c, p) where b = base right / other wrong, c = the reverse."""
    from math import comb
    shared = set(base) & set(other)
    b = sum(1 for k in shared if base[k] and not other[k])
    c = sum(1 for k in shared if not base[k] and other[k])
    n = b + c
    if n == 0:
        return b, c, 1.0
    lo = min(b, c)
    p = min(1.0, 2 * sum(comb(n, i) for i in range(lo + 1)) / 2 ** n)
    return b, c, p


def cmd_report(args):
    recs = [json.loads(l) for l in open(args.results)]
    by_rep = defaultdict(list)
    for r in recs:
        by_rep[r["rep"]].append(r)

    print(f"\nLLM vulnerability-fix classification — {args.results} "
          f"(model: {recs[0].get('model', MODEL) if recs else MODEL})")
    print(f"{'representation':14s} {'n':>4} {'acc':>6} {'prec':>6} {'rec':>6} "
          f"{'F1':>6} {'unk%':>6} {'tok/ex':>8} {'F1/1k-tok':>10}")
    for rep in REPRESENTATIONS:
        rs = by_rep.get(rep, [])
        if not rs:
            continue
        n = len(rs)
        # predicted positive = "yes"; "unknown" counts as a non-fix for scoring
        def pos(r):
            return r["fixes_vulnerability"] == "yes"
        tp = sum(1 for r in rs if r["label"] and pos(r))
        fp = sum(1 for r in rs if not r["label"] and pos(r))
        fn = sum(1 for r in rs if r["label"] and not pos(r))
        tn = sum(1 for r in rs if not r["label"] and not pos(r))
        unk = sum(1 for r in rs if r["fixes_vulnerability"] == "unknown")
        acc = (tp + tn) / n
        prec = tp / (tp + fp) if tp + fp else 0.0
        rec = tp / (tp + fn) if tp + fn else 0.0
        f1 = 2 * prec * rec / (prec + rec) if prec + rec else 0.0
        tok = sum(r["input_tokens"] for r in rs) / n
        eff = f1 / (tok / 1000) if tok else 0.0
        print(f"{rep:14s} {n:>4} {acc:>6.3f} {prec:>6.3f} {rec:>6.3f} "
              f"{f1:>6.3f} {100 * unk / n:>5.1f}% {tok:>8.0f} {eff:>10.3f}")

    cats = defaultdict(int)
    for r in recs:
        for c in r.get("fixed_categories", []):
            cats[c] += 1
    if cats:
        top = sorted(cats.items(), key=lambda kv: -kv[1])[:8]
        print("\ntop predicted categories: "
              + ", ".join(f"{k} ({v})" for k, v in top))

    # per-commit correctness maps, keyed by commit, for the paired analyses
    correct = {rep: {r["commit"]: _is_correct(r) for r in rs}
               for rep, rs in by_rep.items()}

    # (1) McNemar paired significance test — every representation vs. the raw
    # diff baseline, on the commits both classified. Tells you whether any
    # observed accuracy difference is more than sampling noise.
    if "diff" in correct:
        print("\nMcNemar vs. raw diff (paired; b = diff right/other wrong, "
              "c = diff wrong/other right):")
        print(f"{'representation':14s} {'shared':>6} {'b':>4} {'c':>4} "
              f"{'p':>8}  significance")
        for rep in REPRESENTATIONS:
            if rep == "diff" or rep not in correct:
                continue
            b, c, p = _mcnemar(correct["diff"], correct[rep])
            flag = "significant (p<0.05)" if p < 0.05 else "n.s."
            print(f"{rep:14s} {b + c:>6} {b:>4} {c:>4} {p:>8.3f}  {flag}")

    # (2) metrics on the model's own high-confidence answers only (the yes/no
    # verdict is scored as usual, but the sample is restricted to answers the
    # model marked confidence_overall == 'high').
    yes = lambda r: r["fixes_vulnerability"] == "yes"
    print("\n(2) high-confidence subset only (confidence_overall == 'high'):")
    print(f"{'representation':14s} {'n':>4} {'acc':>6} {'prec':>6} "
          f"{'rec':>6} {'F1':>6}")
    for rep in REPRESENTATIONS:
        rs = [r for r in by_rep.get(rep, []) if r.get("confidence_overall") == "high"]
        if not rs:
            continue
        n, acc, prec, rec, f1 = _metrics(rs, yes)
        print(f"{rep:14s} {n:>4} {acc:>6.3f} {prec:>6.3f} {rec:>6.3f} {f1:>6.3f}")

    # (3) confidence-gated verdict on the FULL sample: count a commit as a
    # predicted fix only if the model says 'yes' AND is highly confident;
    # every 'medium'/'low' (and 'unknown'/'no') counts as a non-fix. This is a
    # stricter operating point — expect higher precision, lower recall.
    gated = lambda r: r["fixes_vulnerability"] == "yes" and \
        r.get("confidence_overall") == "high"
    print("\n(3) confidence-gated verdict (positive = 'yes' AND high confidence; "
          "everything less counts as non-fix):")
    print(f"{'representation':14s} {'n':>4} {'acc':>6} {'prec':>6} "
          f"{'rec':>6} {'F1':>6}")
    for rep in REPRESENTATIONS:
        rs = by_rep.get(rep, [])
        if not rs:
            continue
        n, acc, prec, rec, f1 = _metrics(rs, gated)
        print(f"{rep:14s} {n:>4} {acc:>6.3f} {prec:>6.3f} {rec:>6.3f} {f1:>6.3f}")

    # (4) famous vs. obscure repos — if the model were memorizing verdicts, the
    # well-known projects would score much higher. Similar scores argue against
    # memorization as the explanation for the flat representation ranking.
    print(f"\nfamous vs. obscure repositories (famous = {len(FAMOUS)} well-known "
          "projects):")
    print(f"{'representation':14s} {'n_fam':>6} {'acc_fam':>8} "
          f"{'n_obs':>6} {'acc_obs':>8}")
    for rep in REPRESENTATIONS:
        rs = by_rep.get(rep, [])
        fam = [r for r in rs if _repo_name(r["url"]) in FAMOUS]
        obs = [r for r in rs if _repo_name(r["url"]) not in FAMOUS]
        if not rs:
            continue
        af = sum(_is_correct(r) for r in fam) / len(fam) if fam else float("nan")
        ao = sum(_is_correct(r) for r in obs) / len(obs) if obs else float("nan")
        print(f"{rep:14s} {len(fam):>6} {af:>8.3f} {len(obs):>6} {ao:>8.3f}")
    # pooled across representations, the headline memorization check
    fam_all = [r for r in recs if _repo_name(r["url"]) in FAMOUS]
    obs_all = [r for r in recs if _repo_name(r["url"]) not in FAMOUS]
    if fam_all and obs_all:
        af = sum(_is_correct(r) for r in fam_all) / len(fam_all)
        ao = sum(_is_correct(r) for r in obs_all) / len(obs_all)
        print(f"{'ALL reps':14s} {len(fam_all):>6} {af:>8.3f} "
              f"{len(obs_all):>6} {ao:>8.3f}")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build context artifacts + request messages")
    b.add_argument("--limit", type=int, default=0, help="cap commits (debug)")
    b.add_argument("--all-sources", action="store_true",
                   help="include non-GitHub hosts (default: GitHub only)")
    b.set_defaults(func=cmd_build)

    s = sub.add_parser("submit", help="submit one Message Batch (50%% cost)")
    s.add_argument("--max-chars", type=int, default=48000,
                   help="cap per-representation body")
    s.add_argument("--yes", action="store_true", help="skip the cost prompt")
    s.set_defaults(func=cmd_submit)

    f = sub.add_parser("fetch", help="poll the batch and download results")
    f.set_defaults(func=cmd_fetch)

    p = sub.add_parser("report", help="print the metrics table from a run")
    p.add_argument("results", nargs="?", default=RESULTS)
    p.set_defaults(func=cmd_report)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
