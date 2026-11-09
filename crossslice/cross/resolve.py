"""
Resolution cascade for cross-function targets.

Given callee names observed at call sites of a specific commit, resolve each
name to its defining location using a cheap-to-expensive cascade:

  1. gtags:       candidate definitions (name-based, repo-wide, ~ms)
  2. tree-sitter: verify a function/macro definition actually exists at the
                  candidate location and that its arity matches the call site
  3. clangd:      only when several candidates survive — LSP definition query
                  at the call site, against a scoped synthesized compile DB

Each resolution records how it was decided (resolution_method) so fallback
rates can be reported. Works on a temporary git worktree so the analyzed
commit never disturbs the main checkout.
"""

import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

import sys

from crossslice.cross.gtags_handler import GtagsHandler
from crossslice.cross.lsp_function_resolver import STANDARD_LIB_FUNCTIONS
from crossslice.cross.py_clangd_bridge import CompileDBBuilder, ClangdSession
from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC


@dataclass
class CallSite:
    """A call observed in the enriched diff (positions in the version's file)"""
    callee: str
    arg_count: int
    rel_file: str          # path relative to repo root
    line: int              # 0-based
    col: int               # 0-based
    hot_arg_positions: Optional[List[int]] = None  # arg positions carrying variables
    result_used: bool = True                       # call result consumed at the site
    object_macro: bool = False                     # bare identifier, likely object-like macro
    from_control_flow: bool = False                # harvested from a CF statement's subtree
                                                   # aggregate, not a relevant leaf statement


@dataclass
class ResolvedTarget:
    name: str
    rel_file: str
    line: int                       # 0-based line of the definition
    is_macro: bool
    signature: str
    resolution_method: str          # gtags_unique | gtags+ts | lsp | priority_fallback
    candidates_total: int = 0
    candidates_after_ts: int = 0
    code: str = ""                  # full source of the definition (filled by extractor)
    alternatives: list = field(default_factory=list)  # other verified definitions of the same name


@dataclass
class CallerSite:
    """A reference to a changed function, located inside some caller"""
    target: str                     # the changed function being referenced
    rel_file: str
    line: int                       # 0-based line of the reference
    caller_name: str = ""
    caller_start_line: int = -1     # 0-based
    caller_header: str = ""         # set when the caller was attributed by enclosing_header()


# ---- attribution fallback for code tree-sitter does not parse as a function:
# `PHP_METHOD(Phar, mount) { … }` bodies (a top-level compound statement to
# tree-sitter), functions wrapped into ERROR nodes by embedded-GLSL macros, and
# a function merged with the one above it by a parse error. The nearest
# preceding column-0 header line names the caller, like a reader would.
_HEADER_MACRO_RE = re.compile(r"^(?:[A-Za-z_]\w*\s+)*([A-Z_][A-Z0-9_]*)\s*\(([^()]*)\)\s*(/\*.*\*/)?\s*(\{.*)?$")
_ATTR_PREFIX_RE = re.compile(r"^(?:[A-Z_][A-Z0-9_]*\s*\([^()]*\)\s*)+")      # ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int f(
_TYPE_PREFIX_RE = re.compile(r"^(?:[A-Za-z_]\w*[\s\*]+)*\**\s*$")             # `static const char *` before the name
_HEADER_NAME_RE = re.compile(r"([A-Za-z_]\w*)\s*\(")
_LABEL_RE = re.compile(r"^\w+:\s*$")
_KEYWORDS = {"if", "while", "for", "switch", "return", "sizeof", "else", "do", "case", "defined", "typedef",
             "int", "char", "void", "long", "short", "unsigned", "signed", "float", "double", "bool"}


def _without_comments(line: str) -> str:
    return re.sub(r"//.*", "", re.sub(r"/\*.*?\*/", " ", line))


def header_name(line: str) -> str:
    """Function name of a column-0 definition header line, "" if the line is
    not one. A bare `MACRO(args)` header is kept verbatim with normalised
    spacing (`PHP_METHOD(Phar, mount)`), as there is no C name to give."""
    m = _HEADER_MACRO_RE.match(line.rstrip())
    if m:
        return f"{m.group(1)}({', '.join(a.strip() for a in m.group(2).split(','))})"
    rest = _ATTR_PREFIX_RE.sub("", _without_comments(line))
    m = _HEADER_NAME_RE.search(rest)
    if m and m.group(1) not in _KEYWORDS and _TYPE_PREFIX_RE.match(rest[:m.start()]):
        return m.group(1)
    return ""


def enclosing_header(lines: List[str], line0: int, stop_at: int = 0):
    """(header line0, name, header text) of the definition whose body contains
    `line0`, by scanning column-0 lines upwards, or None when `line0` is at
    file scope (a prototype, a macro definition, an initialiser) or no header
    lies above it down to `stop_at`. Indented lines are body text; a `}` at
    column 0 ends a body; a header must open its body with `{` before `line0`
    (a `;` first makes it a prototype)."""
    for i in range(line0 - 1, stop_at - 1, -1):
        l = lines[i]
        if not l or l[0] in " \t":
            continue
        if l[0] == "}":
            return None
        if l[0] in "#{*/" or _LABEL_RE.match(l) or "(" not in l:
            continue
        name = header_name(l)
        if not name:
            continue
        j = i
        while j < line0 and "{" not in _without_comments(lines[j]):
            if ";" in _without_comments(lines[j]):
                return None
            j += 1
        if j >= line0:
            return None
        head = " ".join(_without_comments(p).strip() for p in lines[i:j + 1] if p.strip())
        return i, name, head.split("{")[0].strip()[:200]
    return None


_TEST_PATH_HINTS = ("test", "tests", "testing", "mock", "fixture", "example", "demo", "doc")


def _path_priority(rel_file: str) -> int:
    score = 100
    parts = Path(rel_file).parts
    if any(h in p.lower() for p in parts for h in _TEST_PATH_HINTS):
        score -= 50
    if rel_file.endswith((".c", ".h")):
        score += 10
    score -= max(0, len(parts) - 8)
    return score


# headers that exist to switch real code off (table generators, test doubles)
_STUB_PATH_HINTS = ("tableprint", "stub", "dummy", "fake")
# macro bodies that do nothing: `while(0)`, `do {} while (0)`, `((void)0)`, `(void)0`, `0`, empty
_STUB_BODY_RE = re.compile(
    r"^(?:\(\s*\(?\s*void\s*\)?\s*0\s*\)|\(\s*void\s*\)\s*0|while\s*\(\s*0\s*\)\s*;?"
    r"|do\s*\{\s*\}\s*while\s*\(\s*0\s*\)\s*;?|0|\{\s*\})?$")


def _macro_body(define_line: str) -> str:
    m = re.match(r"#\s*define\s+[A-Za-z_]\w*(?:\([^)]*\))?\s*(.*)$", define_line.strip())
    return m.group(1).strip() if m else ""


def _definition_score(verified: dict, rel_file: str) -> int:
    """Rank the verified definitions of an ambiguous name when no call site
    can disambiguate: a function beats a macro, a macro beats an alias macro
    (`#define get_bits bits_read_nz`), anything beats a stub
    (`#define av_log(a, ...) while(0)`), and test or table-generator paths lose."""
    score = _path_priority(rel_file)
    if verified.get("is_macro"):
        body = _macro_body(verified.get("signature", ""))
        if _STUB_BODY_RE.match(body):
            score -= 40
        elif re.fullmatch(r"[A-Za-z_]\w*", body):
            score -= 25
        else:
            score -= 10
    if any(h in p.lower() for p in Path(rel_file).parts for h in _STUB_PATH_HINTS):
        score -= 30
    return score


class Worktree:
    """Detached git worktree for one (repo, commit); removed on exit."""

    def __init__(self, repo_path: str, commit: str):
        self.repo_path = os.path.abspath(repo_path)
        self.commit = commit
        self.path: Optional[str] = None

    def __enter__(self):
        tmp = tempfile.mkdtemp(prefix="cce_wt_")
        target = os.path.join(tmp, "wt")
        subprocess.run(
            ["git", "worktree", "add", "--detach", target, self.commit],
            cwd=self.repo_path, check=True, capture_output=True, text=True,
        )
        self.path = target
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.path:
            subprocess.run(
                ["git", "worktree", "remove", "--force", self.path],
                cwd=self.repo_path, capture_output=True, text=True,
            )
            # `git worktree remove` deletes the checkout but not the temp
            # parent directory we created for it
            shutil.rmtree(os.path.dirname(self.path), ignore_errors=True)
            self.path = None


class TargetResolver:
    """Runs the cascade for a set of call sites inside one worktree."""

    def __init__(self, worktree_path: str, max_lsp_targets: int = 20,
                 audit_lsp: bool = False, debug: bool = False,
                 work_dir: Optional[str] = None):
        self.root = Path(worktree_path).resolve()
        self.work_dir = work_dir  # compile database location (None: inside the tree)
        self.debug = debug
        self.max_lsp_targets = max_lsp_targets
        self.audit_lsp = audit_lsp  # cross-check cheap-tier decisions with clangd
        self._parsers: Dict[str, SourceCodeParserC] = {}
        self._clangd: Optional[ClangdSession] = None
        # audit only: compile databases from a real configure/make of the
        # projects, JSON {repository root: compile_commands.json}; when set, the
        # audit queries clangd with that database and covers every tier
        self._audit_db_map = os.environ.get("CROSSSLICE_AUDIT_COMPILE_DB_MAP") or None
        self._clangd_audit: Optional[ClangdSession] = None
        self.stats = {"gtags_unique": 0, "gtags+ts": 0, "lsp": 0,
                      "priority_fallback": 0, "unresolved": 0, "stdlib_skipped": 0}
        self.failures: Dict[str, str] = {}  # name -> reason for unresolved
        self.audit: List[dict] = []         # agreement records (audit_lsp mode)

    # ---- helpers -----------------------------------------------------------

    def _parser(self, abs_file: str) -> Optional[SourceCodeParserC]:
        if abs_file not in self._parsers:
            try:
                self._parsers[abs_file] = SourceCodeParserC(abs_file)
            except Exception:
                self._parsers[abs_file] = None
        return self._parsers[abs_file]

    def _ts_verify(self, candidate: dict, arg_count: int) -> Optional[dict]:
        """Confirm a definition exists at the candidate line; check arity.

        Returns the candidate annotated with is_macro/signature/span or None.
        """
        abs_file = candidate["file_path"]
        if not os.path.isabs(abs_file):
            abs_file = str(self.root / abs_file)
        line0 = candidate["line_number"] - 1  # gtags is 1-based

        # object-like macro: '#define NAME ...' with no '(' directly after the
        # name. Not a function definition, so tree-sitter's function collector
        # won't see it — accept it from the gtags code line directly.
        code_line = candidate.get("code_line", "")
        if re.match(rf"#\s*define\s+{re.escape(candidate['symbol'])}\b(?!\()",
                    code_line):
            return {
                **candidate,
                "abs_file": abs_file,
                "line0": line0,
                "is_macro": True,
                "signature": code_line.strip(),
                "node_span": (line0, line0),
            }

        parser = self._parser(abs_file)
        if parser is None:
            return None
        try:
            for node, name, start_line, end_line in parser.collect_function_definitions():
                if name != candidate["symbol"] and not name.startswith(candidate["symbol"]):
                    continue
                if not (start_line <= line0 <= end_line):
                    continue
                is_macro = node.type == "preproc_function_def"
                text = node.text.decode("utf-8", errors="replace")
                if is_macro:
                    signature = text.split("\n")[0].strip()
                else:  # the whole head (GNU style puts the return type on its own line)
                    head = text.split("{")[0]
                    signature = " ".join(p.strip() for p in head.split("\n") if p.strip())[:200]
                n_params = self._count_params(node, is_macro)
                if arg_count >= 0 and n_params >= 0 and n_params != arg_count:
                    # variadic definitions report -1 and are never filtered out
                    return None
                return {
                    **candidate,
                    "abs_file": abs_file,
                    "line0": start_line,
                    "is_macro": is_macro,
                    "signature": signature,
                    "node_span": (start_line, end_line),
                }
        except Exception:
            return None
        return None

    @staticmethod
    def _count_params(node, is_macro: bool) -> int:
        """Parameter count of a definition node; -1 if variadic/unknown."""
        text = node.text.decode("utf-8", errors="replace")
        m = re.search(r"\(([^)]*)\)", text)
        if not m:
            return -1
        params = m.group(1).strip()
        if not params or params == "void":
            return 0
        if "..." in params:
            return -1
        depth, count = 0, 1
        for ch in params:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                count += 1
        return count

    def _audit_compile_db(self) -> Optional[Path]:
        """Audit mode only: pick the mapped compile database whose files exist
        in this worktree, rewrite its paths to the worktree and return the
        directory holding the rewritten compile_commands.json (or None)."""
        try:
            mapping = json.load(open(self._audit_db_map))
        except Exception:
            return None
        best: List[dict] = []
        for orig_root, db_path in mapping.items():
            try:
                entries = json.load(open(db_path))
            except Exception:
                continue
            orig_root = orig_root.rstrip("/")

            def rewrite(v):
                if isinstance(v, str):
                    return v.replace(orig_root, str(self.root))
                if isinstance(v, list):
                    return [rewrite(x) for x in v]
                return v
            rewritten = []
            for e in entries:
                e2 = {k: rewrite(v) for k, v in e.items()}
                f = Path(e2["file"])
                if not f.is_absolute():
                    f = Path(e2["directory"]) / f
                if f.is_file():
                    rewritten.append(e2)
            if len(rewritten) > len(best):
                best = rewritten
        if not best:
            return None
        out_dir = Path(self.work_dir or (self.root / ".py_clangd_bridge")) / "audit_db"
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "compile_commands.json").write_text(json.dumps(best))
        return out_dir

    def _lsp_definition(self, call_site: CallSite, audit: bool = False) -> Optional[dict]:
        """Ask clangd for the definition at the call site; returns {file, line0}.
        audit=True with CROSSSLICE_AUDIT_COMPILE_DB_MAP set uses the mapped
        real compile database instead of the heuristic one."""
        if not call_site.rel_file:
            return None
        try:
            if audit and self._audit_db_map:
                if self._clangd_audit is None:
                    ccdir = self._audit_compile_db()
                    if ccdir is None:
                        return None
                    self._clangd_audit = ClangdSession(
                        project_root=self.root, compile_commands_dir=ccdir,
                        wait_for_indexing=False,
                    )
                    self._clangd_audit.start()
                session = self._clangd_audit
            else:
                if self._clangd is None:
                    db = CompileDBBuilder(self.root, self.work_dir).ensure_compile_commands(
                        target_files=[str(self.root / call_site.rel_file)]
                    )
                    self._clangd = ClangdSession(
                        project_root=self.root, compile_commands_dir=db.parent,
                        wait_for_indexing=False,
                    )
                    self._clangd.start()
                session = self._clangd
            abs_file = self.root / call_site.rel_file
            session.open(str(abs_file), language_id="c")
            res = session.definition(str(abs_file), call_site.line, call_site.col)
            if isinstance(res, list) and res:
                res = res[0]
            if res and "uri" in res:
                path = res["uri"].replace("file://", "")
                line0 = res["range"]["start"]["line"]
                # a "definition" pointing back at the call site means clangd
                # could not resolve (implicit declaration)
                if Path(path).resolve() == abs_file.resolve() and line0 == call_site.line:
                    return None
                return {"file": path, "line0": line0}
        except Exception as e:
            if self.debug:
                print(f"[lsp] definition failed for {call_site.callee}: {e}")
        return None

    # ---- main entry --------------------------------------------------------

    def resolve(self, call_sites_by_name: Dict[str, List[CallSite]],
                gtags: GtagsHandler) -> Dict[str, ResolvedTarget]:
        """Resolve every callee name to a single definition (or skip it)."""
        resolved: Dict[str, ResolvedTarget] = {}
        for name, sites in call_sites_by_name.items():
            if name in STANDARD_LIB_FUNCTIONS:
                self.stats["stdlib_skipped"] += 1
                continue
            candidates = gtags.find_function_definition_detailed(name)
            if not candidates:
                self.stats["unresolved"] += 1
                self.failures[name] = "no_definition_in_repo"
                continue
            arg_count = sites[0].arg_count if sites else -1

            verified = []
            for c in candidates:
                v = self._ts_verify(c, arg_count)
                if v:
                    verified.append(v)

            method = None
            chosen = None
            if len(candidates) == 1 and len(verified) == 1:
                chosen, method = verified[0], "gtags_unique"
            elif len(verified) == 1:
                chosen, method = verified[0], "gtags+ts"
            elif len(verified) > 1:
                # ambiguous -> LSP at the first call site. Only with a real
                # site: a bare-name lookup (graph queries, MCP tools) carries no
                # file/position, and handing clangd an empty path costs minutes
                # (compile DB for the whole tree + timed-out requests) for nothing.
                lsp = (self._lsp_definition(sites[0])
                       if sites and sites[0].rel_file else None)
                if lsp:
                    for v in verified:
                        same_file = Path(v["abs_file"]).resolve() == Path(lsp["file"]).resolve()
                        if same_file and abs(v["line0"] - lsp["line0"]) <= 2:
                            chosen, method = v, "lsp"
                            break
                if chosen is None:
                    # equal scores: the later definition in a file wins — in an
                    # `#if X ... #else ... #endif` pair that is the fallback branch
                    verified.sort(key=lambda v: (-_definition_score(
                        v, os.path.relpath(v["abs_file"], self.root)), v["abs_file"], -v["line0"]))
                    chosen, method = verified[0], "priority_fallback"
            else:
                self.stats["unresolved"] += 1
                # candidates existed but none verified: distinguish arity
                # mismatches from locations tree-sitter could not confirm
                if any(self._ts_verify(c, -1) for c in candidates):
                    self.failures[name] = "arity_mismatch"
                else:
                    self.failures[name] = "no_verifiable_definition"
                continue

            self.stats[method] += 1
            rel = os.path.relpath(chosen["abs_file"], self.root)
            alternatives = [
                {"file": os.path.relpath(v["abs_file"], self.root), "line": v["line0"],
                 "is_macro": v["is_macro"]}
                for v in verified if v is not chosen]

            # audit mode: cross-check decisions the cheap tiers made on their
            # own against clangd (ground-truth proxy where it can answer)
            audit_methods = (("gtags_unique", "gtags+ts", "lsp", "priority_fallback")
                             if self._audit_db_map else ("gtags_unique", "gtags+ts"))
            if self.audit_lsp and method in audit_methods \
                    and sites and not chosen["is_macro"] and not sites[0].object_macro:
                lsp = self._lsp_definition(sites[0], audit=True)
                if lsp is None:
                    verdict = "lsp_no_answer"
                else:
                    def hits(cand):
                        span = cand.get("node_span",
                                        (cand["line0"], cand["line0"]))
                        return (Path(lsp["file"]).resolve()
                                == Path(cand["abs_file"]).resolve()
                                and span[0] - 2 <= lsp["line0"] <= span[1])
                    if hits(chosen):
                        verdict = "agree"
                    elif any(hits(v) for v in verified if v is not chosen):
                        verdict = "disagree"  # clangd picked another known definition
                    else:
                        # clangd's answer is no known definition — without a
                        # build it typically returns the in-TU declaration
                        # (prototype in a header); not evidence against us
                        verdict = "lsp_declaration_only"
                self.audit.append({
                    "name": name, "method": method, "verdict": verdict,
                    "db": "map" if self._audit_db_map else "heuristic",
                    "cheap": f"{rel}:{chosen['line0'] + 1}",
                    "lsp": lsp and f"{os.path.relpath(lsp['file'], self.root)}:{lsp['line0'] + 1}",
                })
            resolved[name] = ResolvedTarget(
                name=name,
                rel_file=rel,
                line=chosen["line0"],
                is_macro=chosen["is_macro"],
                signature=chosen["signature"],
                resolution_method=method,
                candidates_total=len(candidates),
                candidates_after_ts=len(verified),
                alternatives=alternatives,
            )
        return resolved

    def find_callers(self, function_names: List[str], gtags: GtagsHandler,
                     max_callers_per_fn: int = 5) -> Dict[str, List[CallerSite]]:
        """Locate reference sites of the given functions and their enclosing callers."""
        out: Dict[str, List[CallerSite]] = {}
        for name in function_names:
            refs = gtags.find_function_callers_detailed(name)
            # how many reference sites exist in total, so callers can be
            # reported as "N of M" when the cap below truncates the list
            if not hasattr(self, "last_caller_totals"):
                self.last_caller_totals = {}
            self.last_caller_totals[name] = len(refs)
            sites: List[CallerSite] = []
            # prefer non-test files, stable order
            refs.sort(key=lambda r: -_path_priority(r["file_path"]))
            for r in refs:
                if len(sites) >= max_callers_per_fn:
                    break
                abs_file = r["file_path"]
                if not os.path.isabs(abs_file):
                    abs_file = str(self.root / abs_file)
                parser = self._parser(abs_file)
                if parser is None:
                    continue
                line0 = r["line_number"] - 1
                try:
                    fn_node = parser.find_function_containing_line(line0)
                except Exception:
                    fn_node = None
                fallback = None
                if fn_node is None or fn_node.has_error:
                    lines = self._file_lines(abs_file, parser)
                    if fn_node is None:
                        fallback = enclosing_header(lines, line0)
                        if fallback is None:
                            continue  # file scope: prototype, macro definition, initialiser
                    else:
                        # a parse error can merge a function with the one above it:
                        # a header strictly inside the node's range is the real caller
                        cand = enclosing_header(lines, line0, stop_at=fn_node.start_point[0] + 1)
                        if cand is not None and cand[0] > fn_node.start_point[0]:
                            fallback = cand
                if fallback is not None:
                    start_line, caller_name, caller_header = fallback
                else:
                    start_line, caller_header, caller_name = fn_node.start_point[0], "", ""
                    decl = fn_node.child_by_field_name("declarator")
                    if decl is not None:
                        m = re.search(r"(\w+)\s*\(", decl.text.decode("utf-8", errors="replace"))
                        caller_name = m.group(1) if m else ""
                    if not caller_name or caller_name.isupper():
                        # `PHP_FUNCTION(f) { … }`: tree-sitter takes PHP_FUNCTION as the type
                        # and `(f)` as the declarator; name it as the header reads
                        lines = self._file_lines(abs_file, parser)
                        caller_name = header_name(lines[fn_node.start_point[0]]) or caller_name
                if caller_name == name:
                    continue  # the definition itself / recursion
                sites.append(CallerSite(
                    target=name,
                    rel_file=os.path.relpath(abs_file, self.root),
                    line=line0,
                    caller_name=caller_name,
                    caller_start_line=start_line,
                    caller_header=caller_header,
                ))
            if sites:
                out[name] = sites
        return out

    def invalidate(self) -> None:
        """Forget parsed trees and line caches: the working tree changed
        (RepoGraph.update). clangd, when in use, watches the files itself."""
        self._parsers.clear()
        getattr(self, "_lines_cache", {}).clear()

    def _file_lines(self, abs_file: str, parser) -> List[str]:
        cache = getattr(self, "_lines_cache", None)
        if cache is None:
            cache = self._lines_cache = {}
        if abs_file not in cache:
            cache[abs_file] = parser.get_code().split("\n")
        return cache[abs_file]

    def close(self):
        for attr in ("_clangd", "_clangd_audit"):
            session = getattr(self, attr)
            if session is not None:
                try:
                    session.stop()
                except Exception:
                    pass
                setattr(self, attr, None)
