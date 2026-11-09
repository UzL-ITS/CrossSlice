"""Commit-level enrichment: the intra-procedural pipeline (statement IR, GumTree
change classification, bidirectional def-use slice) plus the optional
cross-function expansion (callees/callers/macros resolved through the
gtags -> tree-sitter -> clangd cascade), for one commit or a JSONL dataset.
"""
from __future__ import annotations

import contextlib
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, field
from typing import Iterator, Optional, TextIO

C_SUFFIXES = (".c", ".h")
EMPTY_TREE = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # git's empty tree: the "parent" of a root commit


@dataclass
class EnrichResult:
    repo_path: str
    commit: str
    parent: str
    changed_files: list
    text: str
    cross_stats: dict = field(default_factory=dict)
    seconds: float = 0.0
    note: str = ""  # set when nothing was analyzed (e.g. "no C files changed")
    functions: list = field(default_factory=list)  # changed functions, file order
    cross_error: str = ""  # cross-function step failed; text holds the intra result


def _git(repo: str, *args: str) -> str:
    return subprocess.check_output(["git", "-C", repo, *args], stderr=subprocess.DEVNULL,
                                   text=True).strip()


def resolve_commit(repo: str, ref: str) -> str:
    """Full SHA for any revision expression (HEAD, HEAD~1, a tag, a short SHA)."""
    from crossslice.paths import git_toplevel, has_commits, NotAGitRepository, NO_GIT
    if not git_toplevel(repo):
        raise NotAGitRepository(f"{repo}: {NO_GIT}")
    if ref in ("HEAD", "@") and not has_commits(repo):
        raise ValueError(f"{repo} has no commits yet")
    try:
        return _git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    except subprocess.CalledProcessError:
        raise ValueError(f"{ref!r} is not a commit in {repo}") from None


def enrich_commit(repo_path: str, commit: str, *, parent: Optional[str] = None,
                  cross: bool = True, slice_level: int = 2, cross_slice_level: int = 2,
                  log: Optional[TextIO] = None,
                  cache_dir: Optional[str] = None) -> EnrichResult:
    """Enriched context for `commit` (vs. its first parent, or `parent`).

    `log` receives the analysis logs (default: discarded).
    The result text is returned, not printed. If the cross-function step
    fails, the intra-procedural result is returned with `cross_error` set.
    """
    from crossslice.intra.github_loader import get_changed_files, extract_file_from_commit
    from crossslice.intra.data_diff import create_diff
    from crossslice.intra.parse_diff import parse_diff
    from crossslice.intra.gen_dataflow import gen_dataflow

    repo_path = os.path.abspath(repo_path)
    t0 = time.time()
    new = resolve_commit(repo_path, commit)
    if parent:
        old = resolve_commit(repo_path, parent)
    else:
        try:
            old = _git(repo_path, "rev-parse", "--verify", f"{new}^")
        except subprocess.CalledProcessError:
            old = EMPTY_TREE  # root commit: everything is new

    changed = get_changed_files(repo_path, old, new)
    c_files = [f for f in changed if f and f.endswith(C_SUFFIXES)]
    if not c_files:
        return EnrichResult(repo_path, new, old, [], "", {}, time.time() - t0,
                            note="no C files changed")

    work = tempfile.mkdtemp(prefix="crossslice_")
    old_dir = os.path.join(work, "old_version")
    new_dir = os.path.join(work, "new_version")
    os.makedirs(old_dir)
    os.makedirs(new_dir)
    sink = log if log is not None else io.StringIO()
    stats: dict = {}
    try:
        with contextlib.redirect_stdout(sink):
            for f in c_files:
                extract_file_from_commit(repo_path, old, f, os.path.join(old_dir, f))
                extract_file_from_commit(repo_path, new, f, os.path.join(new_dir, f))
            diff = create_diff(old_dir, new_dir, c_files)
            changes = parse_diff(diff, work, old_dir, new_dir, use_hungarian=True,
                                 debug_matching=False)
            text, internals = gen_dataflow(changes, old_dir, new_dir, level=slice_level,
                                           collect_internals=True)
            functions = list(dict.fromkeys(
                name for d in (changes or {}).values() for name in d.get("functions", {})
                if not name.startswith("__")))  # drop synthetic scopes
            cross_error = ""
            if cross and internals:
                from crossslice.cross.enrich import CrossFunctionEnricher
                from crossslice.paths import repo_cache
                try:
                    enricher = CrossFunctionEnricher(repo_path=repo_path, old_commit=old,
                                                     new_commit=new,
                                                     slice_level=cross_slice_level,
                                                     cache_dir=repo_cache(repo_path, cache_dir))
                    cross_text, cross_json = enricher.enrich(internals)
                    if cross_text:
                        text = (text or "") + "\n" + cross_text
                    stats = (cross_json or {}).get("stats", {}) or {}
                except Exception as e:  # keep the intra result (as the original pipeline did)
                    cross_error = f"{type(e).__name__}: {e}"
                    print(f"[cross] failed, returning the intra-procedural result: "
                          f"{cross_error}")
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return EnrichResult(repo_path, new, old, c_files, text or "", stats, time.time() - t0,
                        functions=functions, cross_error=cross_error,
                        note="root commit: every file is new" if old == EMPTY_TREE else "")


def iter_jsonl(path: str) -> Iterator[dict]:
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                yield json.loads(line)


def enrich_dataset(dataset_path: str, repos_dir: str, out_dir: str, *, cross: bool = True,
                   slice_level: int = 2, cross_slice_level: int = 2,
                   log: Optional[TextIO] = None) -> Iterator[tuple]:
    """Batch mode: one JSONL entry per commit (`project_url`, `commit_id`); repositories
    are cloned into `repos_dir` on demand and one `<repo>_<sha>.txt` is written per
    commit into `out_dir`. Yields (entry, EnrichResult | Exception, output_path)."""
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(repos_dir, exist_ok=True)
    for entry in iter_jsonl(dataset_path):
        url = entry["project_url"].rstrip("/")
        sha = entry["commit_id"]
        name = url.split("/")[-1]
        clone = os.path.join(repos_dir, name)
        out_path = os.path.join(out_dir, f"{name}_{sha}.txt")
        try:
            if not os.path.isdir(clone):
                subprocess.run(["git", "clone", "--quiet", url, clone], check=True)
            res = enrich_commit(clone, sha, cross=cross, slice_level=slice_level,
                                cross_slice_level=cross_slice_level, log=log)
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(res.text if res.text else f"[{res.note}]\n")
            yield entry, res, out_path
        except Exception as e:  # keep the batch going; the caller decides what to do
            yield entry, e, out_path


_SECTION_RE = {
    "change": re.compile(r"^Context for merged statement of old file: (.*) with new file: (.*):$"),
    "callee": re.compile(r"^-- called (function|macro): (\S+) — (.+):(\d+) \[([^\],]+)(?:, (old|new) version)?\] --$"),
    "caller": re.compile(r"^-- caller of (\S+): (\S+) — (.+):(\d+) --$"),
    "ring2": re.compile(r"^-- 2nd-level context \(summaries\) --$"),
}


def split_sections(text: str) -> list[dict]:
    """Split an enriched commit text into its parts, for front ends that show
    them separately: `change` (one per file: the diff merged with its def-use
    slice), `callee` / `macro` (a called definition, sliced), `caller` (a call
    site of a changed function) and `ring2` (second-level summaries)."""
    sections: list[dict] = []
    cur = None
    for line in (text or "").split("\n"):
        if line.startswith("==== Cross-function context"):
            cur = None
            continue
        m = _SECTION_RE["change"].match(line)
        if m:
            old, new = m.groups()
            cur = {"kind": "change", "file": new, "old_file": old,
                   "title": new if old == new else f"{old} → {new}", "body": []}
            sections.append(cur)
            continue
        m = _SECTION_RE["callee"].match(line)
        if m:
            what, name, file, ln, method, version = m.groups()
            cur = {"kind": "macro" if what == "macro" else "callee", "name": name,
                   "file": file, "line": int(ln), "method": method.strip(),
                   "version": version, "body": []}
            sections.append(cur)
            continue
        m = _SECTION_RE["caller"].match(line)
        if m:
            of, name, file, ln = m.groups()
            cur = {"kind": "caller", "of": of, "name": name, "file": file,
                   "line": int(ln), "body": []}
            sections.append(cur)
            continue
        if _SECTION_RE["ring2"].match(line):
            cur = {"kind": "ring2", "body": []}
            sections.append(cur)
            continue
        if cur is not None:
            cur["body"].append(line)
    for s in sections:
        s["body"] = "\n".join(s["body"]).strip("\n")
    return sections
