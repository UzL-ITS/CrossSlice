"""
Parser-independent ground truth for the impact cases (E10 / E12 / E13).

The miner in eval/impact.py attributed each removed call line to its
enclosing function with the tool's own tree-sitter parser. Where that parser
cannot name the function — macro-defined bodies such as
`PHP_METHOD(Phar, loadPhar) { ... }`, or a region tree-sitter wraps into one
big ERROR node (libavfilter/vf_nlmeans_vulkan.c) — the caller silently
dropped out of the truth, and the tool's get_callers drops it the same way,
so the old truth was blind exactly where the tool is. This module rebuilds
the truth from the diff and the parent files alone:

  call site  = a removed line of the commit that contains `F(` and is not
               the definition or a prototype of F (only type tokens before F
               at the start of the line)
  enclosing  = the nearest preceding column-0 line of the PARENT file that
               looks like a function header: contains '(', is not a label,
               not a preprocessor line. A bare `MACRO(args)` header is kept
               verbatim as the name, e.g. `PHP_METHOD(Phar, loadPhar)`.

All 159 candidate lines of the 18 cases were reviewed by hand (2 Nov 2026):
24 are definitions or prototypes, 135 are calls in 120 distinct
(file, function) pairs. The old truth had 98 pairs: 2 named the wrong
function (vf_gblur_vulkan.c — the call is in init_filter, not in
init_gblur_pipeline, tree-sitter had merged the two) and 24 true callers
were missing (PHP_METHOD/PHP_FUNCTION bodies, the nlmeans ERROR region, the
init_filter of three Vulkan filters, and PharFileInfo::__construct whose
call line the old comment stripper cut at the `//` of "phar://").

  uv run python -m eval.truth_sites                     # writes cases_impact_all_v2.jsonl
  uv run python -m eval.truth_sites --diff              # also prints old vs new per case
"""
import argparse
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

CASES_V1 = "eval/cases_impact_all.jsonl"
CASES_V2 = "eval/cases_impact_all_v2.jsonl"


def strip_comments(text):
    """Remove /* */ and // comments; string-aware. (eval.impact._strip_comments
    is not: it cut every line containing "phar://" at the `//`, which hid two
    real call sites of phar_split_fname from the first version of this truth.)"""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c in "\"'":
            j = i + 1
            while j < n and text[j] != c:
                j += 2 if text[j] == "\\" else 1
            out.append(text[i:j + 1])
            i = j + 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            out.append(" ")
            i = n if j < 0 else j + 2
        elif text.startswith("//", i):
            out.append(" ")
            i = n
        else:
            out.append(c)
            i += 1
    return "".join(out)

# a whole header that is one macro call: `PHP_METHOD(Phar, loadPhar)`, optionally
# followed by a comment or the opening brace — not `ATTR(1, 4) int f(...)`
_MACRO_HEADER = re.compile(r"^([A-Z_][A-Z0-9_]*)\s*\(([^()]*)\)\s*(/\*.*\*/)?\s*(\{.*)?$")


def _git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                          text=True, errors="replace").stdout


def header_name(line):
    """Function name of a column-0 header line; `MACRO(args)` kept verbatim."""
    m = _MACRO_HEADER.match(line)
    if m:
        args = ", ".join(a.strip() for a in m.group(2).split(","))
        return f"{m.group(1)}({args})"
    for m in re.finditer(r"([A-Za-z_]\w*)\s*\(", line):
        name = m.group(1)
        # attribute-like macro call in front of the type: ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int f(
        if m.start() == 0 and name.isupper():
            continue
        return name
    return None


def enclosing(lines, lineno):
    """(header line number, name) of the function enclosing 1-based `lineno`."""
    for i in range(lineno - 2, -1, -1):
        l = lines[i]
        if not re.match(r"[A-Za-z_]", l) or l.startswith("#"):
            continue
        if re.match(r"\w+:\s*$", l) or "(" not in l:
            continue                      # label, closing brace, bare macro
        name = header_name(l)
        if name:
            return i + 1, name
    return None, None


def call_sites(repo, sha, fname):
    """[(path, parent line, enclosing name, text)] for every removed line of
    the commit that calls `fname` (definitions and prototypes excluded)."""
    diff = _git(repo, "show", "--format=", "-U0", "--diff-filter=M", sha, "--", "*.c", "*.h")
    call_re = re.compile(rf"(?<![\w.>])\b{re.escape(fname)}\s*\(")
    decl_re = re.compile(rf"^\s*[\w\s\*]+\b{re.escape(fname)}\s*\(")
    path, cur_old, cache, out = None, 0, {}, []
    for line in diff.split("\n"):
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("@@"):
            m = re.search(r"-(\d+)", line)
            cur_old = int(m.group(1)) if m else 0
        elif line.startswith("-") and not line.startswith("---"):
            text = strip_comments(line[1:])
            if call_re.search(text) and not decl_re.match(text):
                if path not in cache:
                    cache[path] = _git(repo, "show", f"{sha}^:{path}").split("\n")
                _, name = enclosing(cache[path], cur_old)
                if name and name != fname:
                    out.append((path, cur_old, name, line[1:].strip()))
            cur_old += 1
    return out


def rebuild(cases_path=CASES_V1, out_path=CASES_V2, show_diff=False):
    rows = []
    for c in map(json.loads, open(cases_path)):
        sites = call_sites(c["repo"], c["sha"], c["function"])
        pairs = sorted({(p, n) for p, _, n, _ in sites})
        rec = dict(c)
        rec["truth_v1"] = c["truth"]
        rec["truth"] = [list(p) for p in pairs]
        rec["truth_sites"] = [[p, ln, n] for p, ln, n, _ in sites]
        rows.append(rec)
        if show_diff:
            old = {tuple(t) for t in c["truth"]}
            new = set(pairs)
            print(f"{os.path.basename(c['repo']):8} {c['sha'][:8]} {c['function']:38} "
                  f"sites {len(sites):2}  pairs {len(pairs):2} (old {len(old):2})"
                  + (f"\n     + {sorted(new - old)}" if new - old else "")
                  + (f"\n     - {sorted(old - new)}" if old - new else ""))
    with open(out_path, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    n_sites = sum(len(r["truth_sites"]) for r in rows)
    n_pairs = sum(len(r["truth"]) for r in rows)
    n_old = sum(len(r["truth_v1"]) for r in rows)
    print(f"{len(rows)} cases: {n_sites} call sites, {n_pairs} (file, function) pairs "
          f"(old truth: {n_old}) -> {out_path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cases", default=CASES_V1)
    ap.add_argument("--out", default=CASES_V2)
    ap.add_argument("--diff", action="store_true")
    a = ap.parse_args()
    rebuild(a.cases, a.out, a.diff)
