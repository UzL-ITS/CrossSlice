"""
Per-tier report of the clangd audit (`eval.benchmark --audit-lsp`).

The benchmark stores, for every audited resolution, the tool's location and
clangd's location. Its own verdict has three values (agree, lsp_no_answer,
lsp_declaration_only), and the last one is a catch-all for "clangd pointed at
something that is not one of the tool's candidates". This report looks at what
clangd pointed at and splits that class:

  agree         clangd names the definition the tool chose
  other-def     clangd names another definition of the same name   (contradiction)
  system        clangd names a declaration in a system header while the tool
                chose a definition inside the repository           (contradiction
                under the audited build configuration); an installed copy of
                one of the project's own headers counts as a declaration
  declaration   clangd names a prototype of the same name in the repository
                (no evidence: it could not see the definition)
  other-symbol  the target line does not carry the name (clangd resolved a
                macro or another token at the call position, or echoed the call)
  no-answer     clangd returned nothing

  uv run python -m eval.audit_report eval/results/bench_h100_audit_realdb.jsonl
"""
import collections
import json
import os
import re
import subprocess
import sys

REPOS = "data/repos"
ORDER = ("agree", "other-def", "system", "declaration", "other-symbol", "no-answer")


def _show(repo, rev, path, cache):
    key = (repo, rev, path)
    if key not in cache:
        r = subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], capture_output=True,
                           text=True, errors="replace")
        cache[key] = r.stdout.split("\n") if r.returncode == 0 else None
    return cache[key]


def _ls(repo, cache):
    if ("ls", repo) not in cache:
        cache[("ls", repo)] = subprocess.run(["git", "-C", repo, "ls-files"], capture_output=True,
                                             text=True).stdout.split("\n")
    return cache[("ls", repo)]


def _kind(lines, ln, name):
    """prototype / definition / None for the declaration of `name` at 1-based ln (+-2)."""
    for i in range(max(1, ln - 2), min(len(lines), ln + 2) + 1):
        if not re.search(rf"\b{re.escape(name)}\b", lines[i - 1]):
            continue
        if re.match(r"\s*#\s*define", lines[i - 1]):
            return "definition"
        if not re.match(r"[A-Za-z_]", lines[i - 1]) and not re.match(r"[A-Za-z_]", lines[max(0, i - 2)]):
            continue                                   # an indented use, not a file-scope declarator
        tail = re.sub(r"/\*.*?\*/", " ", " ".join(lines[i - 1:i + 14]))
        brace, semi = tail.find("{"), tail.find(";")
        return "definition" if brace != -1 and (semi == -1 or brace < semi) else "prototype"
    return None


def classify(rec, a, cache):
    if a["verdict"] == "agree":
        return "agree"
    if a["verdict"] == "lsp_no_answer" or not a.get("lsp"):
        return "no-answer"
    if a["verdict"] == "disagree":
        return "other-def"
    path, ln = a["lsp"].rsplit(":", 1)
    repo = os.path.join(REPOS, rec["repo"])
    if path.startswith("..") or path.startswith("/"):
        # an installed copy of one of the project's own headers (zlib.h) is a declaration
        base = os.path.basename(path)
        own = [f for f in _ls(repo, cache) if os.path.basename(f) == base]
        for f in own:
            lines = _show(repo, rec["commit"], f, cache) or []
            if any(re.search(rf"\b{re.escape(a['name'])}\b", l) for l in lines):
                return "declaration"
        return "system"
    kinds = set()
    for rev in (rec["commit"], rec["commit"] + "^"):
        lines = _show(repo, rev, path, cache)
        if lines:
            kinds.add(_kind(lines, int(ln), a["name"]))
    tool_path = a["cheap"].rsplit(":", 1)[0]
    if "definition" in kinds and (path != tool_path or abs(int(ln) - int(a["cheap"].rsplit(":", 1)[1])) > 40):
        return "other-def"
    if "prototype" in kinds or "definition" in kinds:
        return "declaration"
    return "other-symbol"


def report(path):
    cache, table, detail = {}, collections.defaultdict(collections.Counter), []
    for l in open(path):
        if not l.strip():
            continue
        rec = json.loads(l)
        if rec.get("status") != "ok":
            continue
        for a in rec.get("audit") or []:
            c = classify(rec, a, cache)
            table[a["method"]][c] += 1
            if c in ("other-def", "system", "other-symbol"):
                detail.append((c, rec["repo"], rec["commit"][:10], a["method"], a["name"], a["cheap"], a["lsp"]))
    print(f"{path}\n{'tier':18s}" + "".join(f"{c:>13s}" for c in ORDER) + f"{'total':>8s}")
    total = collections.Counter()
    for tier in ("gtags_unique", "gtags+ts", "lsp", "priority_fallback"):
        row = table.get(tier, {})
        total.update(row)
        print(f"{tier:18s}" + "".join(f"{row.get(c, 0):>13d}" for c in ORDER) + f"{sum(row.values()):>8d}")
    print(f"{'all':18s}" + "".join(f"{total.get(c, 0):>13d}" for c in ORDER) + f"{sum(total.values()):>8d}")
    named = total["agree"] + total["other-def"] + total["system"]
    print(f"\nclangd names a definition or a system declaration in {named} decisions: "
          f"{total['agree']} agree ({100 * total['agree'] / named:.1f} %), "
          f"{total['other-def']} name another definition, {total['system']} name the system library")
    for d in sorted(detail):
        print("  ", *d)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", nargs="+", help="audit result files of eval.benchmark --audit-lsp")
    ap.add_argument("--repos", default=REPOS, help="directory with the subject clones (default data/repos)")
    a = ap.parse_args()
    REPOS = a.repos
    for p in a.results:
        report(p)
