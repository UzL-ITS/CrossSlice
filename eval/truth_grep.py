"""
Ground truth for the hard impact cases: every call of F at the parent revision.

The first truth (eval/truth_sites.py) takes the call lines that a
signature-changing commit removed. That is complete when the commit edits
every call of one function, and it was verified for those 18 cases. It does
not carry over to the hard cases: a name with several definitions of which
the commit changes some, calls in generated files that git does not diff,
work-in-progress commits, and bulk library upgrades. Here the truth is built
from the parent tree alone and does not use any of the tools under test:

  occurrence  every line of the parent revision that contains the word F
              (`git grep -w`, all tracked text files)
  scope       a `static` definition in a .c file can only be called from that
              file; any other definition (external linkage, or static inline
              in a header) from anywhere
  class       call       F( in code, inside a function body        -> required
              in-macro   F( inside a #define body                  -> optional
              ref        F without ( in code: address taken, table -> optional
              decl       column-0 line with F( : definition or prototype
              comment    F only inside a comment or a string
              non-code   file that is not source code (docs, tests, changelogs)
              scope      file of another static definition
  enclosing   truth_sites.enclosing(): the nearest preceding column-0 header
              line; a `MACRO(args)` header is kept verbatim

Required callers are the functions that contain a call. Optional names are
accepted in an answer but not required and not counted as errors: a macro
whose body calls F, the functions that use such a macro, the function that
holds a non-call reference (a function pointer), and F itself when it is
recursive.

Every occurrence is written to a review sheet. The sheet was checked by hand
before the cases file was used; `--drop FILE:LINE` removes an occurrence that
the review rejected.

  uv run python -m eval.truth_grep --cases eval/cases_impact_hard_raw.jsonl \\
      --out eval/cases_impact_hard_v3.jsonl --sheet eval/cases_impact_hard_review.txt
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from eval.truth_sites import _git, enclosing  # noqa: E402

C_EXT = (".c", ".h")
CODE_EXT = C_EXT + (".y", ".l", ".re", ".dasc", ".inc", ".def", ".m", ".mm", ".cc", ".cpp", ".cxx",
                    ".hh", ".hpp", ".S", ".s")


def code_only(text):
    """`text` with comments and the contents of string and character literals
    replaced by spaces; line structure and columns are preserved."""
    out, i, n = [], 0, len(text)
    while i < n:
        c = text[i]
        if c in "\"'":
            j = i + 1
            while j < n and text[j] != c and text[j] != "\n":
                j += 2 if text[j] == "\\" else 1
            out.append(c + " " * max(0, j - i - 1) + (c if j < n and text[j] == c else ""))
            i = j + 1
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            out.append("".join(ch if ch == "\n" else " " for ch in text[i:j]))
            i = j
        elif text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j == -1 else j
            out.append(" " * (j - i))
            i = j
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _definition(lines, fname):
    """(1-based line, is_static) of the first definition of fname in a file:
    a column-0 header line with `fname(` followed by `{` before any `;`."""
    pat = re.compile(rf"\b{re.escape(fname)}\s*\(")
    for i, l in enumerate(lines):
        if not re.match(r"[A-Za-z_]", l) or not pat.search(l):
            continue
        tail = " ".join(lines[i:i + 12])
        brace, semi = tail.find("{"), tail.find(";")
        if brace != -1 and (semi == -1 or brace < semi):
            head = " ".join(lines[max(0, i - 1):i + 1])
            return i + 1, bool(re.search(r"\bstatic\b", head))
    return None, False


def _macro_of(lines, lineno):
    """Name of the #define whose (continued) body contains 1-based lineno."""
    i = lineno - 1
    while i > 0 and lines[i - 1].rstrip().endswith("\\"):
        i -= 1
    m = re.match(r"\s*#\s*define\s+([A-Za-z_]\w*)", lines[i])
    return m.group(1) if m else None


class Tree:
    """Files of one revision, raw and with comments and strings blanked."""

    def __init__(self, repo, rev):
        self.repo, self.rev, self._raw, self._code = repo, rev, {}, {}

    def raw(self, path):
        if path not in self._raw:
            self._raw[path] = _git(self.repo, "show", f"{self.rev}:{path}").split("\n")
        return self._raw[path]

    def code(self, path):
        if path not in self._code:
            self._code[path] = code_only("\n".join(self.raw(path))).split("\n")
        return self._code[path]

    def grep(self, word):
        for hit in _git(self.repo, "grep", "-n", "-w", "-a", "-e", word, self.rev).split("\n"):
            m = re.match(rf"{re.escape(self.rev)}:(.+?):(\d+):", hit)
            if m and "\0" not in hit:
                yield m.group(1), int(m.group(2))


def occurrences(repo, sha, fname, def_file):
    tree = Tree(repo, sha + "^")
    def_line, static = _definition(tree.raw(def_file), fname)
    file_scope = static and def_file.endswith(".c")
    word_re = re.compile(rf"\b{re.escape(fname)}\b")
    call_re = re.compile(rf"(?<![\w.>])\b{re.escape(fname)}\s*\(")
    out = []
    for path, lineno in tree.grep(fname):
        raw = tree.raw(path)
        text = raw[lineno - 1] if lineno <= len(raw) else ""
        name = None
        if file_scope and path != def_file:
            cls = "scope"
        elif not path.endswith(CODE_EXT):
            cls = "non-code"
        else:
            code = tree.code(path)[lineno - 1] if lineno <= len(tree.code(path)) else ""
            macro = _macro_of(raw, lineno)
            if not word_re.search(code):
                cls = "comment"
            elif macro and macro != fname:
                cls, name = ("in-macro" if call_re.search(code) else "ref"), macro
            elif macro == fname:
                cls = "decl"                               # #define F(...)
            elif re.match(r"[A-Za-z_]", text):
                cls = "decl"                               # file scope: definition, prototype, declaration
            else:
                _, name = enclosing(raw, lineno)
                if not call_re.search(code):
                    cls = "ref"
                elif not name:
                    cls = "decl"
                elif name == fname:
                    cls = "recursive"
                else:
                    cls = "call"
        out.append({"file": path, "line": lineno, "class": cls, "name": name, "text": text.strip()})
    return tree, {"def_line": def_line, "static": static, "file_scope": file_scope, "occurrences": out}


def macro_users(tree, macro):
    """Enclosing functions of the code lines that use `macro` (not its #define)."""
    names = set()
    for path, lineno in tree.grep(macro):
        if not path.endswith(CODE_EXT):
            continue
        raw, code = tree.raw(path), tree.code(path)
        if lineno > len(code) or not re.search(rf"\b{re.escape(macro)}\b", code[lineno - 1]):
            continue
        if _macro_of(raw, lineno) or re.match(r"\s*#", raw[lineno - 1]):
            continue
        _, name = enclosing(raw, lineno)
        if name:
            names.add(name)
    return names


def build(cases_path, out_path, sheet_path, drops):
    seen, cases = set(), []
    for l in open(cases_path):
        if l.strip():
            c = json.loads(l)
            if (c["sha"], c["function"]) not in seen:
                seen.add((c["sha"], c["function"]))
                cases.append(c)
    sheet = open(sheet_path, "w")
    with open(out_path, "w") as fh:
        for c in cases:
            repo, fn = c["repo"], c["function"]
            tree, o = occurrences(repo, c["sha"], fn, c["file"])
            occ = o["occurrences"]
            for x in occ:
                if f"{x['file']}:{x['line']}" in drops:
                    x["class"] = "dropped"
            calls = [x for x in occ if x["class"] == "call"]
            sites = [[x["file"], x["line"], x["name"]] for x in calls]
            truth = sorted({(x["file"], x["name"]) for x in calls})
            required = {n for _, n in truth}
            optional = set()
            for x in occ:
                if x["class"] == "in-macro":
                    optional |= {x["name"]} | macro_users(tree, x["name"])
                elif x["class"] == "ref" and x["name"]:
                    optional.add(x["name"])
                elif x["class"] == "recursive":
                    optional.add(fn)
            optional -= required
            opt_sites = [[x["file"], x["line"]] for x in occ if x["class"] in ("in-macro", "ref", "recursive")]
            rec = {k: c[k] for k in ("repo", "sha", "function", "file", "arity_old", "arity_new") if k in c}
            rec.update(n_defs=c.get("n_defs"), n_refs=c.get("n_refs"), file_scope=o["file_scope"],
                       truth=[list(t) for t in truth], truth_sites=sites,
                       optional=sorted(optional), optional_sites=opt_sites)
            fh.write(json.dumps(rec) + "\n")
            cnt = {}
            for x in occ:
                cnt[x["class"]] = cnt.get(x["class"], 0) + 1
            nonc = sorted({x["file"] for x in calls if not x["file"].endswith(C_EXT)})
            sheet.write(f"\n==== {fn}  {os.path.basename(repo)} @ {c['sha'][:10]}^  defined in "
                        f"{c['file']}:{o['def_line']}  static={o['static']} file_scope={o['file_scope']}\n"
                        f"     {cnt} -> {len(sites)} call sites, {len(required)} required names, "
                        f"{len(optional)} optional\n")
            if nonc:
                sheet.write(f"     calls in files that are not .c/.h: {nonc}\n")
            if optional:
                sheet.write(f"     optional: {sorted(optional)[:40]}\n")
            for x in occ:
                if x["class"] == "scope":
                    continue
                sheet.write(f"  {x['class']:9s} {x['file']}:{x['line']:<6} [{x['name'] or ''}]  {x['text'][:110]}\n")
            print(f"{fn:32s} {cnt} -> {len(sites)} sites, {len(required)} names, {len(optional)} optional")
    sheet.close()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cases", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheet", required=True)
    ap.add_argument("--drop", action="append", default=[],
                    help="FILE:LINE of an occurrence rejected in the manual review (repeatable)")
    a = ap.parse_args()
    build(a.cases, a.out, a.sheet, set(a.drop))
