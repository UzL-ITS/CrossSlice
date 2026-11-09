"""
RQ3c / RQ3d — Does an *agent* that pulls context on demand through the tool beat
(or cost less than) an agent that has to navigate the repository on its own?

Two tasks, one harness:

  classify  Is this commit a vulnerability fix?  (RQ3c)
            Cases: the batch's *confident mistakes* (eval/llm_classify.py).
            Arms:  no_tool    raw diff, one structured answer
                   self       raw diff + generic file tools (list/read/grep)
                              over BOTH versions — a stock coding agent
                   with_tool  raw diff + the MCP tools (crossslice.cross.mcp_server)

  fix       Repair the vulnerability in the PRE-commit code.  (RQ3d)
            Cases: hand-labeled vulnerability-fixing commits whose real fix is
            small (<= --max-functions functions, <= --max-lines changed lines).
            The agent is told which function(s)/file(s) are affected and must
            find the root cause and write a patch. It never sees the real fix:
            the MCP server is started with --lock-version old.
            Arms:  self       generic file tools only
                   tool       generic file tools + the MCP tools (locked to old)
            A judge model (claude-sonnet-5) scores each submission against the
            real fix: root cause correct/partial/wrong, fix equivalent/partial/
            wrong/none. We also record, per case and without any model call, the
            *static* context sizes: the changed files, the changed functions,
            and what the tool hands over (sliced bodies + callee summaries).

Both tasks measure, per arm: accuracy (or judge score), total tokens across the
whole loop (what is billed without caching), the context size at the final turn
(what the model had to hold), and tool-call counts. The model sees only code —
never the repository name or commit message.

Models are named <provider>:<model> (eval/providers.py): Anthropic directly
(ANTHROPIC_API_KEY) or any tool-capable model on OpenRouter (OPENROUTER_API_KEY),
so the same harness runs frontier and small/cheap models:

  uv run python -m eval.agent_probe run --task fix --n 6            # opus (default)
  uv run python -m eval.agent_probe run --task fix --n 10 \
      --model openrouter:qwen/qwen3-coder-30b-a3b-instruct --budget 40000
  uv run python -m eval.agent_probe models --max-in 0.5             # pick models
  uv run python -m eval.agent_probe report --task fix               # all models

`--dry-run` selects cases, checks the MCP plumbing, and (fix task) computes the
static context sizes without calling the model — no key needed. Results stream
to eval/results/agent_probe.jsonl (classify) / agent_fix.jsonl (fix), resumable.
"""

import argparse
import asyncio
import contextlib
import fnmatch
import io
import json
import os
import random
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import eval._env  # noqa: F401,E402  (.env + GUMTREE_PATH bootstrap)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import eval.llm_classify as base
from eval import providers
from crossslice.cross.resolve import Worktree

MODEL = "anthropic:claude-sonnet-5-5"     # <provider>:<model>; see eval/providers.py
EFFORT = "high"
JUDGE_MODEL = "anthropic:claude-sonnet-5-5"
MAX_ITERS = {"classify": 16, "fix": 24}
MAX_TOKENS = 12000
TOOL_TIMEOUT = 300          # per tool call once the server is warm
WARMUP_TIMEOUT = 1800       # first call on a fresh checkout builds the index
RESULTS = "eval/results/agent_probe.jsonl"
RESULTS_FIX = "eval/results/agent_fix.jsonl"           # legacy name of the first opus run
TRANSCRIPTS = "eval/results/agent_transcripts"
GUMTREE_DEFAULT = "/opt/gumtree/gumtree-4.0.0-beta3/bin/gumtree"
DIFF_TOOLS = ("get_commit_overview", "get_raw_diff", "get_intra_diff",
              "list_changed_functions")


def results_path(task, model_spec):
    """One results file per (task, model), e.g. agent_fix_qwen-qwen3-coder.jsonl."""
    base_name = "agent_probe" if task == "classify" else "agent_fix"
    return f"eval/results/{base_name}_{providers.slug(model_spec)}.jsonl"

# ------------------------------- prompts ------------------------------------

VERDICT_SCHEMA = base.RESPONSE_SCHEMA
SYSTEM_NOTOOL = base.SYSTEM_PROMPT

_EXPLORE_COMMON = (
    "You are a security engineer triaging a source-code change from a C/C++ "
    "project. You are NOT given the commit message or the repository name — "
    "judge only from the code.\n\n"
    "You have tools to explore the codebase on demand. Both the OLD (pre-commit) "
    "and NEW (post-commit) versions are available: pass version=\"old\" or "
    "version=\"new\". The vulnerability signal usually lives in the DIFFERENCE "
    "between versions — e.g. a bound or check that appears in the new version, "
    "or a caller that passes attacker-controlled data into a changed function. "
    "Explore only as much as you need.\n\n"
    "When you are confident, call submit_verdict exactly once with your decision. "
    "Do not call it until you have gathered enough evidence."
)
SYSTEM_TOOL = _EXPLORE_COMMON + (
    "\n\nAvailable: semantic tools that resolve symbols, return def-use-sliced "
    "bodies, side-effect summaries, callers, and a function's neighborhood."
)
SYSTEM_SELF = _EXPLORE_COMMON + (
    "\n\nAvailable: generic repository tools — list files, read a file (by line "
    "range), and grep — over either version."
)
START_TOOL = (
    "Here is the raw diff of the commit. Investigate with the tools as needed, "
    "then call submit_verdict.\n\n```\n{diff}\n```"
)

SUBMIT_TOOL = {
    "name": "submit_verdict",
    "description": "Record your final decision about whether the commit fixes a "
                   "security vulnerability. Call this exactly once, when done.",
    "strict": True,
    "input_schema": VERDICT_SCHEMA,
}

FIX_SCHEMA = {
    "type": "object",
    "properties": {
        "root_cause": {"type": "string",
                       "description": "2-4 sentences: what the vulnerability is, "
                                      "where, and why it is exploitable"},
        "patch": {"type": "string",
                  "description": "A minimal fix as a unified diff (or, if you "
                                 "cannot produce a diff, the exact replacement "
                                 "code with file and line references)"},
        "files_touched": {"type": "array", "items": {"type": "string"}},
        "confidence_overall": {"type": "string", "enum": ["high", "medium", "low"]},
    },
    "required": ["root_cause", "patch", "files_touched", "confidence_overall"],
    "additionalProperties": False,
}
SUBMIT_FIX_TOOL = {
    "name": "submit_fix",
    "description": "Submit your final root-cause analysis and patch. Call this "
                   "exactly once, when done.",
    "strict": True,
    "input_schema": FIX_SCHEMA,
}

_FIX_COMMON = (
    "You are a security engineer. The C repository you can explore contains a "
    "security vulnerability at its current revision. You are NOT told the "
    "repository name; judge only from the code.\n\n"
    "Your task: find the root cause and write a MINIMAL fix. Explore only as "
    "much as you need — the fix is typically a few lines in or around the named "
    "function(s). When you are confident, call submit_fix exactly once with a "
    "short root-cause explanation and the patch (unified diff with exact lines)."
)
SYSTEM_FIX_SELF = _FIX_COMMON + (
    "\n\nAvailable: generic repository tools — list files, read a file (by line "
    "range), and grep."
)
SYSTEM_FIX_TOOL = _FIX_COMMON + (
    "\n\nAvailable: generic repository tools (list/read/grep) AND semantic tools. "
    "Start with get_neighborhood(name): ONE call returns the function's callees "
    "as one-line summaries, its callers with their call sites, and the struct "
    "types it uses. Then get_function_source for exact lines, "
    "get_type_definition for a field's type, get_sliced_body / get_summary / "
    "get_callers for detail. Read whole files only when you must."
)
SYSTEM_FIX_SEMANTIC = _FIX_COMMON + (
    "\n\nAvailable: semantic tools only. Start with get_neighborhood(name): ONE "
    "call returns the function's callees as one-line summaries, its callers "
    "with their call sites, and the struct types it uses. Then "
    "get_function_source for exact lines, get_type_definition for a field's "
    "type, get_sliced_body / get_summary / get_callers for detail. There is no "
    "file reader and no grep: navigate by symbol names."
)
START_FIX = (
    "The vulnerability is in {what}. Investigate with the tools, then call "
    "submit_fix with the root cause and a minimal patch."
)
START_FIX_SEEDED = (
    "The vulnerability is in {what}. Here is the function as it stands:\n\n"
    "```c\n{source}\n```\n\nInvestigate its context with the tools as needed "
    "(what its callees do, how callers use it, the types involved), then call "
    "submit_fix with the root cause and a minimal patch."
)

JUDGE_SYSTEM = (
    "You are grading a security engineer's proposed fix for a real vulnerability "
    "against the actual fix the maintainers committed. Judge SEMANTICS, not "
    "formatting: a proposal is 'equivalent' if it closes the same vulnerability "
    "in the same place with a check or change that has the same effect, even if "
    "the code differs. 'partial' means the right root cause is addressed but the "
    "fix is incomplete, wrong in a detail, or over-restrictive; 'wrong' means it "
    "changes something else; 'none' means no usable patch was given."
)
JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "root_cause_match": {"type": "string", "enum": ["correct", "partial", "wrong"]},
        "fix_quality": {"type": "string",
                        "enum": ["equivalent", "partial", "wrong", "none"]},
        "rationale": {"type": "string"},
    },
    "required": ["root_cause_match", "fix_quality", "rationale"],
    "additionalProperties": False,
}
JUDGE_USER = (
    "ACTUAL FIX (ground truth, unified diff):\n```\n{truth}\n```\n\n"
    "PROPOSED ROOT CAUSE:\n{root_cause}\n\n"
    "PROPOSED PATCH:\n```\n{patch}\n```\n\n"
    "Grade the proposal."
)
JUDGE_SCORE = {"equivalent": 2, "partial": 1, "wrong": 0, "none": 0}


# --------------------------- generic file tools -----------------------------

class RepoFS:
    """The tools a stock coding agent has: list / read / grep over one or two
    checked-out versions of the repository. Results are budget-clipped exactly
    like the MCP tools (20k chars)."""

    MAX_CHARS = 20000
    MAX_LINES = 250
    MAX_ENTRIES = 300

    def __init__(self, roots: dict):
        self.roots = roots                      # {"old": path, "new": path}
        self.versions = list(roots)

    def schemas(self):
        ver = {"type": "string", "enum": self.versions,
               "description": "which version of the repository to look at"}
        return [
            {"name": "list_files",
             "description": "List files under a directory of the repository "
                            "(recursively, up to 300 entries), optionally "
                            "filtered by a substring or glob on the path.",
             "input_schema": {"type": "object", "properties": {
                 "path": {"type": "string", "description": "directory, '' = root"},
                 "pattern": {"type": "string",
                             "description": "substring or glob to filter paths"},
                 "version": ver}, "required": ["version"]}},
            {"name": "read_file",
             "description": "Read a file by line range (1-based, inclusive; at "
                            "most 250 lines per call — page through long files).",
             "input_schema": {"type": "object", "properties": {
                 "path": {"type": "string"},
                 "start_line": {"type": "integer"},
                 "end_line": {"type": "integer"},
                 "version": ver}, "required": ["path", "version"]}},
            {"name": "grep",
             "description": "Search file contents with an extended regular "
                            "expression (git grep -n -E); returns "
                            "file:line: text, up to max_results matches.",
             "input_schema": {"type": "object", "properties": {
                 "pattern": {"type": "string"},
                 "path_glob": {"type": "string",
                               "description": "restrict to paths matching this "
                                              "glob, e.g. 'src/*.c'"},
                 "max_results": {"type": "integer"},
                 "version": ver}, "required": ["pattern", "version"]}},
        ]

    def _root(self, version):
        if version not in self.roots:
            raise ValueError(f"version '{version}' is not available "
                             f"(have: {', '.join(self.versions)})")
        return self.roots[version]

    def _clip(self, text):
        if len(text) > self.MAX_CHARS:
            return text[:self.MAX_CHARS] + "\n... [truncated to budget] ..."
        return text

    def call(self, name, args):
        try:
            fn = {"list_files": self.list_files, "read_file": self.read_file,
                  "grep": self.grep}[name]
            args = dict(args)
            # a model that drops the required `version` (DeepSeek V4 Pro did, repeatedly)
            # gets the task's primary version instead of a TypeError
            args.setdefault("version", self.versions[0])
            return self._clip(fn(**args))
        except Exception as e:
            return f"error: {type(e).__name__}: {e}"

    def list_files(self, version, path="", pattern=""):
        root = self._root(version)
        base_dir = os.path.normpath(os.path.join(root, path or ""))
        if not base_dir.startswith(root):
            return "error: path escapes the repository"
        if not os.path.isdir(base_dir):
            return f"error: not a directory: {path}"
        out, n = [], 0
        for d, dirs, files in os.walk(base_dir):
            dirs[:] = sorted(x for x in dirs if x != ".git")
            for f in sorted(files):
                rel = os.path.relpath(os.path.join(d, f), root)
                if pattern and not (pattern.lower() in rel.lower()
                                    or fnmatch.fnmatch(rel, pattern)):
                    continue
                n += 1
                if n <= self.MAX_ENTRIES:
                    try:
                        size = os.path.getsize(os.path.join(d, f))
                    except OSError:
                        size = -1
                    out.append(f"{rel}\t{size}")
        head = f"{n} files" + (f" (showing {self.MAX_ENTRIES})" if n > self.MAX_ENTRIES else "")
        return head + "\n" + "\n".join(out)

    def read_file(self, version, path, start_line=1, end_line=None):
        root = self._root(version)
        abs_path = os.path.normpath(os.path.join(root, path))
        if not abs_path.startswith(root):
            return "error: path escapes the repository"
        if not os.path.isfile(abs_path):
            return f"error: no such file: {path}"
        lines = open(abs_path, errors="replace").read().split("\n")
        s = max(1, int(start_line or 1))
        e = int(end_line) if end_line else s + self.MAX_LINES - 1
        e = min(e, s + self.MAX_LINES - 1, len(lines))
        body = "\n".join(f"{i:5d}| {lines[i - 1]}" for i in range(s, e + 1))
        return f"{path} lines {s}-{e} of {len(lines)}\n{body}"

    def grep(self, version, pattern, path_glob="", max_results=60):
        root = self._root(version)
        cmd = ["git", "grep", "-n", "-I", "-E", pattern]
        if path_glob:
            cmd += ["--", path_glob]
        r = subprocess.run(cmd, cwd=root, capture_output=True, text=True,
                           errors="replace", timeout=60)
        if r.returncode not in (0, 1):
            return f"error: {r.stderr.strip()[:300]}"
        hits = [h[:200] for h in r.stdout.split("\n") if h]
        cap = max(1, min(int(max_results or 60), 200))
        head = f"{len(hits)} matches" + (f" (showing {cap})" if len(hits) > cap else "")
        return head + "\n" + "\n".join(hits[:cap])


# ------------------------------ case selection -----------------------------

_CPP_EXT = (".cxx", ".cpp", ".cc", ".c++", ".hpp", ".hh", ".hxx")


def _ordered_mistakes():
    """The batch's confident mistakes on the raw diff, class-balanced, ordered
    high-confidence first then medium (full pool; caller caps/filters)."""
    recs = [json.loads(l) for l in open(base.RESULTS)]
    diff = [r for r in recs if r["rep"] == "diff"]
    order = {"high": 0, "medium": 1, "low": 2}
    wrong = [r for r in diff if not base._is_correct(r)]
    wrong.sort(key=lambda r: order.get(r["confidence_overall"], 3))
    pos = [r for r in wrong if r["label"]]       # missed fixes (model said no)
    neg = [r for r in wrong if not r["label"]]   # false alarms (model said yes)
    out, i, j = [], 0, 0
    while i < len(pos) or j < len(neg):
        if i < len(pos):
            out.append(pos[i]); i += 1
        if j < len(neg):
            out.append(neg[j]); j += 1
    return out


def is_c_commit(repo_dir, sha):
    """True if the commit's deep analysis is C (the slicer's supported language).
    C++ (explicit extension, or .h-only changes in a C++-dominant repo) → False."""
    changed = subprocess.run(["git", "diff", "--name-only", f"{sha}^", sha],
                             cwd=repo_dir, capture_output=True, text=True).stdout.split()
    changed = [f for f in changed if f]
    if any(f.endswith(_CPP_EXT) for f in changed):
        return False
    if any(f.endswith(".c") for f in changed):
        return True
    # only headers/other: decide by the repo's dominant source language
    tree = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha],
                          cwd=repo_dir, capture_output=True, text=True).stdout.split()
    c = sum(f.endswith(".c") for f in tree)
    cpp = sum(f.endswith((".cxx", ".cpp", ".cc", ".c++")) for f in tree)
    return c >= cpp


def select_cases(n, include_cpp=False, skip=0):
    """Pick `n` confident-mistake cases, skipping C++ commits by default (the
    def-use slicer is C-only) and the first `skip` qualifying cases (to fetch
    the next batch). Fetches each candidate to classify it; skips are printed."""
    cases, passed = [], 0
    for c in _ordered_mistakes():
        if len(cases) >= n:
            break
        repo = c["url"].rstrip("/").split("/")[-1]
        repo_dir = base.resolve_repo(c["url"], c["commit"])
        if repo_dir is None:
            print(f"  skip (unavailable): {repo} {c['commit'][:10]}")
            continue
        if not include_cpp and not is_c_commit(repo_dir, c["commit"]):
            print(f"  skip (C++): {repo} {c['commit'][:10]}")
            continue
        passed += 1                     # a qualifying case
        if passed <= skip:              # already covered by an earlier batch
            continue
        cases.append(c)
    return cases


def _commit_shape(repo_dir, sha):
    """(changed C/H files, added+deleted lines over them) of a commit."""
    r = subprocess.run(["git", "diff", "--numstat", f"{sha}^", sha],
                       cwd=repo_dir, capture_output=True, text=True)
    files, lines = [], 0
    for row in r.stdout.split("\n"):
        parts = row.split("\t")
        if len(parts) != 3:
            continue
        a, d, f = parts
        if not f.endswith((".c", ".h")):
            continue
        files.append(f)
        lines += (int(a) if a.isdigit() else 0) + (int(d) if d.isdigit() else 0)
    return files, lines


def _changed_functions(repo_dir, sha):
    """Changed files / functions of a commit via the pipeline (in-process), plus
    the raw diff — the ground truth for the fix task."""
    from crossslice.cross.mcp_server import CommitContext
    ctx = CommitContext(repo_dir, sha)
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            changed = ctx.changed()
            raw = ctx.raw_diff()
    finally:
        ctx.close()
    return changed, raw


def _tree_size(repo_dir, sha):
    r = subprocess.run(["git", "ls-tree", "-r", "--name-only", sha], cwd=repo_dir,
                       capture_output=True, text=True)
    return r.stdout.count("\n")


def _all_in_old(repo_dir, sha, files, functions):
    """Every hinted function must be defined in the pre-commit version of the
    changed files (textually: `name(` present in some old file)."""
    old = ""
    for f in files:
        r = subprocess.run(["git", "show", f"{sha}^:{f}"], cwd=repo_dir,
                           capture_output=True, text=True, errors="replace")
        old += r.stdout
    return all(f"{fn}(" in old or f"{fn} (" in old for fn in functions)


def select_fix_cases(n, skip=0, max_functions=2, max_lines=80, seed=42,
                     max_files=2, max_tree_files=30000):
    """Hand-labeled vulnerability-fixing commits whose real fix is small and in
    C: <= max_files changed C/H files, <= max_lines changed lines, and
    1..max_functions changed functions as attributed by the pipeline. Shuffled
    deterministically so cases spread across repositories."""
    rows = [r for r in base.load_dataset(github_only=True) if r["correct_label"]]
    random.Random(seed).shuffle(rows)
    cases, passed = [], 0
    for r in rows:
        if len(cases) >= n:
            break
        sha, url = r["commit_id"], r["project_url"]
        repo = url.rstrip("/").split("/")[-1]
        repo_dir = base.resolve_repo(url, sha)
        if repo_dir is None:
            print(f"  skip (unavailable): {repo} {sha[:10]}")
            continue
        files, lines = _commit_shape(repo_dir, sha)
        if not files or len(files) > max_files or lines > max_lines:
            print(f"  skip (shape: {len(files)} files, {lines} lines): {repo} {sha[:10]}")
            continue
        if (tree := _tree_size(repo_dir, sha)) > max_tree_files:
            # a worktree of a blobless partial clone fetches every blob of the
            # tree; keep the on-demand fetch bounded
            print(f"  skip (tree too large for on-demand checkout: {tree:,} files): "
                  f"{repo} {sha[:10]}")
            continue
        if not is_c_commit(repo_dir, sha):
            print(f"  skip (C++): {repo} {sha[:10]}")
            continue
        try:
            changed, raw = _changed_functions(repo_dir, sha)
        except Exception as e:
            print(f"  skip (pipeline: {type(e).__name__}: {str(e)[:120]}): {repo} {sha[:10]}")
            continue
        fns = changed["functions"]
        if not fns or len(fns) > max_functions:
            print(f"  skip ({len(fns)} changed functions): {repo} {sha[:10]}")
            continue
        if not _all_in_old(repo_dir, sha, changed["files"], fns):
            # a function the fix introduces cannot be hinted at in the old code
            print(f"  skip (function missing in pre-commit version): {repo} {sha[:10]}")
            continue
        passed += 1
        if passed <= skip:
            continue
        cases.append({"commit": sha, "url": url, "label": True, "repo_dir": repo_dir,
                      "files": changed["files"], "functions": fns,
                      "changed_lines": lines, "truth_diff": raw})
    return cases


# ------------------------------- static sizes -------------------------------

async def static_context_mcp(session, repo_dir, prev, files, functions):
    """Static context sizes measured through the (locked) MCP server, i.e. in
    the exact text the model would receive: the changed files in full (what a
    file-reading agent pays at minimum), the named functions in full, and the
    tool's ring — sliced body + summary of each named function, summaries of
    its direct callees, and its caller list. Also warms the server's index."""
    async def call(name, args, timeout=TOOL_TIMEOUT):
        try:
            r = await asyncio.wait_for(session.call_tool(name, args), timeout=timeout)
        except asyncio.TimeoutError:
            out["timeouts"] = out.get("timeouts", 0) + 1
            return ""
        return r.content[0].text if r.content else ""

    out = {"file_chars": 0, "fn_chars": 0, "tool_chars": 0, "nbhd_chars": 0,
           "n_callees": 0, "n_callers": 0, "sources": {}}
    for f in files:
        r = subprocess.run(["git", "show", f"{prev}:{f}"], cwd=repo_dir,
                           capture_output=True, text=True, errors="replace")
        out["file_chars"] += len(r.stdout)
    first = True
    for fn in functions:
        # the very first call builds the gtags index (or restores it from cache)
        src = await call("get_function_source", {"name": fn},
                         WARMUP_TIMEOUT if first else TOOL_TIMEOUT)
        first = False
        if not src.lstrip().startswith("{"):
            out["fn_chars"] += len(src)
            out["sources"][fn] = src
        nb = await call("get_neighborhood", {"name": fn})
        if not nb.lstrip().startswith("{"):
            out["nbhd_chars"] += len(nb)
        body = await call("get_sliced_body", {"name": fn})
        if not body.lstrip().startswith("{"):
            out["tool_chars"] += len(body)
        hood = await call("expand_function", {"name": fn, "levels": 1})
        try:
            h = json.loads(hood)
        except json.JSONDecodeError:
            h = {}
        if "callees" in h:
            seen = set()
            for c in h["callees"]:
                if c["name"] in seen:
                    continue
                seen.add(c["name"])
                out["n_callees"] += 1
                out["tool_chars"] += len(await call("get_summary", {"name": c["name"]}))
            out["n_callers"] += len(h.get("callers", []))
            out["tool_chars"] += len(json.dumps(h.get("callers", [])))
    return out


def static_context(repo_dir, sha, files, functions):
    """Context sizes in characters for the pre-commit version, no model calls:
    the changed files in full (what an agent reading files pays at minimum),
    the changed functions in full, and what the tool hands over — the sliced
    bodies + summaries of the changed functions, the summaries of their direct
    callees, and their caller lists."""
    from crossslice.cross.mcp_server import CommitContext
    ctx = CommitContext(repo_dir, sha)
    out = {"file_chars": 0, "fn_chars": 0, "tool_chars": 0,
           "n_callees": 0, "n_callers": 0}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            for f in files:
                r = subprocess.run(["git", "show", f"{ctx.prev}:{f}"], cwd=repo_dir,
                                   capture_output=True, text=True, errors="replace")
                out["file_chars"] += len(r.stdout)
            for fn in functions:
                src = ctx.function_source(fn, "old")
                if "source" in src:
                    out["fn_chars"] += len(src["source"])
                sb = ctx.sliced_body(fn, "old")
                if "body" in sb:
                    out["tool_chars"] += len(sb["body"]) + len(json.dumps(sb.get("summary") or {}))
                hood = ctx.expand(fn, "old", 1)
                if "callees" in hood:
                    seen = set()
                    for c in hood["callees"]:
                        if c["name"] in seen:
                            continue
                        seen.add(c["name"])
                        out["n_callees"] += 1
                        s = ctx.summary(c["name"], "old")
                        out["tool_chars"] += len(json.dumps(s))
                    out["n_callers"] += len(hood["callers"])
                    out["tool_chars"] += len(json.dumps(hood["callers"]))
    finally:
        ctx.close()
    return out


# --------------------------------- logging ----------------------------------

def _leaf_errors(exc):
    """Flatten anyio/asyncio ExceptionGroups to their real leaf exceptions."""
    subs = getattr(exc, "exceptions", None)
    if subs:
        out = []
        for s in subs:
            out.extend(_leaf_errors(s))
        return out
    return [exc]


def _preview(text, n=280):
    text = (text or "").strip().replace("\n", " ")
    return text if len(text) <= n else text[:n] + " …"


def _blocks(content):
    """Pull (thinking_summary, assistant_text, tool_use_blocks) from a response."""
    thinking = " ".join(b.thinking for b in content
                        if b.type == "thinking" and b.thinking)
    text = " ".join(b.text for b in content if b.type == "text")
    tools = [b for b in content if b.type == "tool_use"]
    return thinking, text, tools


class Logger:
    """Dual sink: concise (truncated) lines to the terminal + full,
    untruncated Markdown to a per-case file, flushed after every write so the
    file can be followed live (`tail -f`)."""

    def __init__(self, path, quiet):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fh = open(path, "w")
        self.path = path
        self.quiet = quiet

    def term(self, msg=""):
        if not self.quiet:
            print(msg, flush=True)

    def file(self, md=""):
        self.fh.write(md + "\n")
        self.fh.flush()

    def both(self, term_msg, file_md):
        self.term(term_msg)
        self.file(file_md)

    def close(self):
        self.fh.close()


# ------------------------------ the agent loop ------------------------------

async def run_agent(session, tools, dispatch, final_tool, lg, max_iters,
                    budget=None):
    """Generic tool-use loop over a providers.Session. `dispatch(name, args)
    -> str` executes a tool; `final_tool` ends the loop. `budget` (total
    tokens, input+output summed over turns) forces the submission once
    exceeded. Returns (final_args or None, stats)."""
    tin = tout = ncalls = 0
    cache_read = 0
    cost = 0.0
    cost_known = True
    final_ctx = 0
    used = {}
    final = None
    transcript = []
    stop = "final_tool"
    step = 0
    nudged = False
    over_budget = False
    force_next = False          # set after repeated turns without a tool call
    while step < max_iters:
        step += 1
        force = final is None and (step == max_iters or over_budget or force_next)
        lg.term(f"    --- turn {step} --- (calling model…{' forced' if force else ''})")
        turn = await session.step(tools, force_tool=final_tool if force else None)
        u = turn.usage
        tin += u.inp
        tout += u.out
        cache_read += u.cache_read
        if u.cost is None:
            cost_known = False
        else:
            cost += u.cost
        final_ctx = u.inp               # the full prompt of the last turn (cache reads included)
        rec = {"step": step, "thinking": turn.thinking, "text": turn.text,
               "usage": {"in": u.inp, "out": u.out}, "stop_reason": turn.stop_reason,
               "forced": force, "tool_calls": []}
        lg.file(f"### Turn {step}  _(tok {u.inp}+{u.out}, stop={turn.stop_reason}"
                f"{', forced' if force else ''})_\n")
        if turn.thinking:
            lg.term(f"    reasoning: {_preview(turn.thinking, 400)}")
            lg.file(f"**Reasoning:** {turn.thinking}\n")
        if turn.text:
            lg.term(f"    says: {_preview(turn.text)}")
            lg.file(f"**Says:** {turn.text}\n")

        if not turn.tool_calls:
            transcript.append(rec)
            if force:                      # even a forced call produced nothing
                stop = "no_submission"
                break
            if step >= max_iters:
                break
            if not nudged:
                # cut off, or answered in prose instead of calling a tool:
                # remind once, then let it continue exploring
                nudged = True
                what = ("Your previous response was cut off. " if turn.stop_reason == "max_tokens"
                        else "You did not call a tool. ")
                session.add_user(what + "Use the tools to investigate, and call "
                                 f"{final_tool} when you are done.")
                lg.file("_(no tool call — nudged)_\n")
                continue
            # second time without a tool call: force the submission next turn
            force_next = True
            session.add_user(f"Call {final_tool} now with your best decision.")
            lg.file("_(no tool call again — forcing submission)_\n")
            continue

        results = []
        for cid, name, args in turn.tool_calls:
            ncalls += 1
            used[name] = used.get(name, 0) + 1
            argstr = ", ".join(f"{k}={str(v)[:60]}" for k, v in args.items())
            call = {"tool": name, "input": args}
            if name == final_tool:
                if "_raw" in args:            # unparseable JSON: salvage what we can
                    args = providers.lenient_json(args["_raw"])
                final = args
                call["result"] = "(final submission)"
                lg.both(f"    -> {final_tool}: {_preview(json.dumps(args), 160)}",
                        f"- **{final_tool}** → `{json.dumps(args)}`\n")
                results.append((cid, name, "recorded"))
            else:
                lg.term(f"    -> {name}({argstr}) … running")
                try:
                    txt = await asyncio.wait_for(dispatch(name, args), timeout=TOOL_TIMEOUT)
                except asyncio.TimeoutError:
                    txt = (f"error: {name} timed out after {TOOL_TIMEOUT}s; the "
                           "symbol may be in an unsupported language (C++) or the "
                           "repository index is still building. Try another tool.")
                except Exception as e:
                    txt = f"error: {type(e).__name__}: {str(e)[:300]}"
                call["result"] = txt
                lg.term(f"    -> {name}({argstr}) -> {_preview(txt)}")
                lg.file(f"- `{name}({argstr})` →\n\n```\n{txt}\n```\n")
                results.append((cid, name, txt))
            rec["tool_calls"].append(call)
        transcript.append(rec)
        session.add_tool_results(results)
        if final is not None:
            break
        if budget and tin + tout >= budget and not over_budget:
            over_budget = True
            session.add_user(f"Token budget exhausted. Call {final_tool} now "
                             "with your best decision based on what you have seen.")
            lg.file(f"_(budget of {budget:,} tokens exhausted — forcing submission)_\n")
    if final is None and stop == "final_tool":
        stop = "max_iters"
    elif final is not None and over_budget:
        stop = "budget"
    elif final is not None and force_next:
        stop = "forced_no_tool"     # model stopped calling tools; submission forced
    stats = {"in": tin, "out": tout, "total": tin + tout, "final_ctx": final_ctx,
             "cache_read": cache_read, "cost": cost if cost_known else None,
             "tool_calls": ncalls, "tools_used": used, "turns": step,
             "stop": stop, "providers": getattr(session, "providers_seen", None),
             "served_models": getattr(session, "served_models", None),   # Anthropic: fallbacks show up here
             "refusals": getattr(session, "refusals", None) or None,
             "empty_from": getattr(session, "empty_from", None) or None,
             "text_tool_calls": getattr(session, "text_tool_calls", 0),
             "transcript": transcript}
    return final, stats


def _mcp_dispatch(session):
    async def dispatch(name, args):
        r = await session.call_tool(name, args)
        return r.content[0].text if r.content else ""
    return dispatch


def _fs_dispatch(fs):
    async def dispatch(name, args):
        return await asyncio.to_thread(fs.call, name, args)
    return dispatch


def _combined_dispatch(fs, session):
    fs_names = {t["name"] for t in fs.schemas()}
    mcp_d = _mcp_dispatch(session)
    fs_d = _fs_dispatch(fs)

    async def dispatch(name, args):
        return await (fs_d if name in fs_names else mcp_d)(name, args)
    return dispatch


def _mcp_schemas(mcp_tools, lock=None):
    """Tool schemas for the model; under a version lock the diff/overview tools
    are hidden entirely (the server would only return an error for them)."""
    out = []
    for t in mcp_tools:
        if lock and t.name in DIFF_TOOLS:
            continue
        schema = json.loads(json.dumps(t.inputSchema))
        if lock:  # the server answers for the locked version regardless
            schema.get("properties", {}).pop("version", None)
            schema["required"] = [r for r in schema.get("required", []) if r != "version"]
        out.append({"name": t.name, "description": t.description, "input_schema": schema})
    return out


def _server_params(repo_dir, sha, lock=None):
    env = dict(os.environ)
    env.setdefault("GUMTREE_PATH", GUMTREE_DEFAULT)
    args = ["run", "python", "-m", "crossslice.cross.mcp_server",
            repo_dir, "--commit", sha]
    if lock:
        args += ["--lock-version", lock]
    return StdioServerParameters(command="uv", args=args, env=env)


# ------------------------------ classify task -------------------------------

async def arm_notool(cfg, raw_diff, lg):
    lg.both("  [no-tool arm]", "## No-tool arm (raw diff, one shot)\n")
    lg.term("    (calling model…)")
    session = providers.make_session(cfg.model, SYSTEM_NOTOOL, "", cfg.effort, MAX_TOKENS)
    pred, thinking, u = await session.one_shot(
        SYSTEM_NOTOOL, base.USER_TEMPLATE.format(body=raw_diff), VERDICT_SCHEMA)
    if thinking:
        lg.term(f"    reasoning: {_preview(thinking, 400)}")
        lg.file(f"**Reasoning (summary):** {thinking}\n")
    lg.both(f"    verdict: {pred.get('fixes_vulnerability')} "
            f"({pred.get('confidence_overall')})",
            f"**Verdict:** `{pred.get('fixes_vulnerability')}` "
            f"({pred.get('confidence_overall')}) — categories: "
            f"{pred.get('fixed_categories')}\n_Tokens: {u.inp}+{u.out}_\n")
    stats = {"in": u.inp, "out": u.out, "total": u.inp + u.out, "final_ctx": u.inp,
             "cost": u.cost, "tool_calls": 0, "tools_used": {}, "turns": 1,
             "stop": "one_shot"}
    return pred, stats


def _score_verdict(pred, label):
    """None (no verdict submitted) is scored as WRONG, and flagged."""
    if not pred:
        return {"pred": None, "correct": False, "no_verdict": True}
    yes = pred.get("fixes_vulnerability") == "yes"
    return {"pred": pred.get("fixes_vulnerability"), "correct": yes == bool(label)}


_KEEP = ("in", "out", "total", "final_ctx", "cost", "tool_calls", "tools_used",
         "turns", "stop", "providers", "empty_from", "text_tool_calls")


def _arm_record(pred, stats, label):
    return {**_score_verdict(pred, label), **{k: stats.get(k) for k in _KEEP}}


async def run_classify_case(cfg, case, arms, dry_run, quiet=False):
    repo_dir = base.resolve_repo(case["url"], case["commit"])
    if repo_dir is None:
        print(f"  unavailable: {case['url']} {case['commit'][:10]}", file=sys.stderr)
        return None
    repo = case["url"].rstrip("/").split("/")[-1]
    params = _server_params(repo_dir, case["commit"])
    errlog = open(os.devnull, "w")
    async with stdio_client(params, errlog=errlog) as (read, write):
        async with ClientSession(read, write) as session:
            await asyncio.wait_for(session.initialize(), timeout=60)
            tools = (await session.list_tools()).tools
            raw = (await asyncio.wait_for(
                session.call_tool("get_raw_diff", {}), timeout=180)).content[0].text

            if dry_run:
                print(f"  [dry] {case['commit'][:10]} tools={len(tools)} "
                      f"diff={len(raw)} chars — plumbing OK")
                return None

            run_tag = os.path.basename(cfg.results_file).replace(".jsonl", "")
            path = os.path.join(TRANSCRIPTS, f"{run_tag}_{repo}_{case['commit'][:12]}.md")
            lg = Logger(path, quiet)
            lg.file(f"# Agent transcript — {repo} @ {case['commit'][:12]}\n")
            lg.file(f"- Ground truth: **{'FIX' if case['label'] else 'not a fix'}**")
            lg.file(f"- Batch (raw diff, one-shot): said "
                    f"`{case['fixes_vulnerability']}` @ "
                    f"{case['confidence_overall']} confidence\n")
            rec = {"commit": case["commit"], "url": case["url"],
                   "label": case["label"],
                   "batch_diff_pred": case["fixes_vulnerability"],
                   "batch_confidence": case["confidence_overall"],
                   "model": cfg.model, "effort": cfg.effort, "budget": cfg.budget,
                   "transcript": path}
            iters = cfg.max_iters or MAX_ITERS["classify"]
            try:
                if "no_tool" in arms:
                    pred, st = await arm_notool(cfg, raw, lg)
                    rec["no_tool"] = _arm_record(pred, st, case["label"])
                if "self" in arms:
                    lg.both("  [self-navigation arm]",
                            "## Self-navigation arm (generic file tools)\n")
                    prev = subprocess.run(["git", "rev-parse", f"{case['commit']}^"],
                                          cwd=repo_dir, capture_output=True,
                                          text=True).stdout.strip()
                    with Worktree(repo_dir, prev) as wo, \
                            Worktree(repo_dir, case["commit"]) as wn:
                        fs = RepoFS({"old": wo.path, "new": wn.path})
                        sess = providers.make_session(
                            cfg.model, SYSTEM_SELF, START_TOOL.format(diff=raw),
                            cfg.effort, MAX_TOKENS, provider_order=cfg.provider,
                            provider_ignore=cfg.ignore_provider)
                        pred, st = await run_agent(
                            sess, fs.schemas() + [SUBMIT_TOOL], _fs_dispatch(fs),
                            "submit_verdict", lg, iters, cfg.budget)
                    rec["self"] = _arm_record(pred, st, case["label"])
                if "with_tool" in arms:
                    lg.both("  [with-tool arm]", "## With-tool arm (MCP exploration)\n")
                    sess = providers.make_session(
                        cfg.model, SYSTEM_TOOL, START_TOOL.format(diff=raw),
                        cfg.effort, MAX_TOKENS, provider_order=cfg.provider,
                        provider_ignore=cfg.ignore_provider)
                    pred, st = await run_agent(
                        sess, _mcp_schemas(tools) + [SUBMIT_TOOL], _mcp_dispatch(session),
                        "submit_verdict", lg, iters, cfg.budget)
                    rec["with_tool"] = _arm_record(pred, st, case["label"])
            finally:
                lg.close()
    print(f"  transcript -> {path}")
    return rec


# -------------------------------- fix task ----------------------------------

async def judge_fix(cfg, truth_diff, submission):
    if not submission or not (submission.get("patch") or submission.get("root_cause")):
        return {"root_cause_match": "wrong", "fix_quality": "none",
                "rationale": "no submission", "score": 0}
    session = providers.make_session(cfg.judge, JUDGE_SYSTEM, "", "low", 1500)
    j, _, _ = await session.one_shot(
        JUDGE_SYSTEM, JUDGE_USER.format(
            truth=truth_diff[:30000],
            root_cause=submission.get("root_cause", ""),
            patch=submission.get("patch", "")),
        JUDGE_SCHEMA, max_tokens=1500)
    j["score"] = JUDGE_SCORE.get(j.get("fix_quality"), 0)
    return j


def _hint(case, mode="function"):
    """'function': names only — localization is part of the task.
    'function+file': names and files (what the first opus run used)."""
    parts = [f"function `{fn}`" for fn in case["functions"]]
    if mode == "function+file":
        return (", ".join(parts) + " (in " + ", ".join(f"`{f}`" for f in case["files"]) + ")")
    return ", ".join(parts)


async def run_fix_case(cfg, case, arms, dry_run, quiet=False):
    repo_dir = case["repo_dir"]
    sha = case["commit"]
    repo = case["url"].rstrip("/").split("/")[-1]
    prev = subprocess.run(["git", "rev-parse", f"{sha}^"], cwd=repo_dir,
                          capture_output=True, text=True).stdout.strip()

    rec = {"commit": sha, "url": case["url"], "files": case["files"],
           "functions": case["functions"], "changed_lines": case["changed_lines"],
           "model": cfg.model, "effort": cfg.effort,
           "hint": cfg.hint, "budget": cfg.budget, "judge": cfg.judge}
    first = START_FIX.format(what=_hint(case, cfg.hint))
    iters = cfg.max_iters or MAX_ITERS["fix"]
    route = dict(provider_order=cfg.provider, provider_ignore=cfg.ignore_provider)

    # One locked MCP server per case. Its first call builds (or restores) the
    # index; we do that here, before any model clock starts, and measure the
    # static context sizes through the same session.
    params = _server_params(repo_dir, sha, lock="old")
    async with stdio_client(params, errlog=open(os.devnull, "w")) as (r, w):
        async with ClientSession(r, w) as session:
            await asyncio.wait_for(session.initialize(), timeout=60)
            tools = _mcp_schemas((await session.list_tools()).tools, lock="old")
            print("  warming the index / measuring static context …", flush=True)
            static = await static_context_mcp(session, repo_dir, prev,
                                              case["files"], case["functions"])
            sources = static.pop("sources")
            rec["static"] = static
            print(f"  static chars: files {static['file_chars']:,} | functions "
                  f"{static['fn_chars']:,} | tool ring-1 {static['tool_chars']:,} | "
                  f"neighborhood {static['nbhd_chars']:,} "
                  f"({static['n_callees']} callees, {static['n_callers']} callers)")
            if cfg.seed_source:
                seed = "\n\n".join(sources.get(fn, f"// {fn}: source unavailable")
                                    for fn in case["functions"])
                first = START_FIX_SEEDED.format(what=_hint(case, cfg.hint), source=seed)
                rec["seed_source"] = True
            if dry_run:
                blocked = (await session.call_tool("get_raw_diff", {})).content[0].text
                assert "not available" in blocked, blocked
                print(f"  [dry] {sha[:10]} hint={_hint(case, cfg.hint)} "
                      f"lines={case['changed_lines']} — locked server OK "
                      f"({len(tools)} tools exposed)")
                return rec

            run_tag = os.path.basename(cfg.results_file).replace(".jsonl", "")
            path = os.path.join(TRANSCRIPTS, f"{run_tag}_{repo}_{sha[:12]}.md")
            lg = Logger(path, quiet)
            lg.file(f"# Fix-task transcript — {repo} @ {sha[:12]} — "
                    f"{cfg.model} @ {cfg.effort}\n")
            lg.file(f"- Hint given: {_hint(case, cfg.hint)}")
            lg.file(f"- Real fix: {case['changed_lines']} changed lines\n")
            lg.file(f"```diff\n{case['truth_diff'][:8000]}\n```\n")
            rec["transcript"] = path

            async def finish(arm, sub, st):
                j = await judge_fix(cfg, case["truth_diff"], sub)
                lg.file(f"**Judge:** `{json.dumps(j)}`\n")
                lg.term(f"    judge: {j['fix_quality']} / root cause "
                        f"{j['root_cause_match']}")
                rec[arm] = {**{k: st[k] for k in st if k != "transcript"},
                            "submission": sub, "judge": j}

            try:
                with Worktree(repo_dir, prev) as wo:
                    fs = RepoFS({"old": wo.path})
                    if "self" in arms:
                        lg.both("  [self arm]",
                                "## Self-navigation arm (generic file tools)\n")
                        sess = providers.make_session(
                            cfg.model, SYSTEM_FIX_SELF, first, cfg.effort, MAX_TOKENS,
                            **route)
                        sub, st = await run_agent(
                            sess, fs.schemas() + [SUBMIT_FIX_TOOL], _fs_dispatch(fs),
                            "submit_fix", lg, iters, cfg.budget)
                        await finish("self", sub, st)
                    if "tool" in arms:
                        lg.both("  [tool arm]",
                                "## Tool arm (generic + MCP, locked to old)\n")
                        sess = providers.make_session(
                            cfg.model, SYSTEM_FIX_TOOL, first, cfg.effort, MAX_TOKENS,
                            **route)
                        sub, st = await run_agent(
                            sess, fs.schemas() + tools + [SUBMIT_FIX_TOOL],
                            _combined_dispatch(fs, session), "submit_fix", lg,
                            iters, cfg.budget)
                        await finish("tool", sub, st)
                    if "semantic" in arms:
                        lg.both("  [semantic arm]",
                                "## Semantic arm (MCP tools only, locked to old)\n")
                        sess = providers.make_session(
                            cfg.model, SYSTEM_FIX_SEMANTIC, first, cfg.effort,
                            MAX_TOKENS, **route)
                        sub, st = await run_agent(
                            sess, tools + [SUBMIT_FIX_TOOL], _mcp_dispatch(session),
                            "submit_fix", lg, iters, cfg.budget)
                        await finish("semantic", sub, st)
            finally:
                lg.close()
    print(f"  transcript -> {path}")
    return rec


# --------------------------------- driver ----------------------------------

def load_case_list(path):
    """Curated cases: one `<repo url> <sha>` per line (# comments allowed).
    Each is fetched on demand and shaped like the automatic selection."""
    cases = []
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        url, sha = line.split()[:2]
        repo = url.rstrip("/").split("/")[-1]
        repo_dir = base.resolve_repo(url, sha)
        if repo_dir is None:
            print(f"  unavailable: {repo} {sha[:10]}")
            continue
        full = subprocess.run(["git", "rev-parse", sha], cwd=repo_dir,
                              capture_output=True, text=True).stdout.strip()
        files, lines = _commit_shape(repo_dir, full)
        try:
            changed, raw = _changed_functions(repo_dir, full)
        except Exception as e:
            print(f"  skip (pipeline: {type(e).__name__}: {str(e)[:100]}): {repo} {sha[:10]}")
            continue
        fns = changed["functions"]
        if not fns or not _all_in_old(repo_dir, full, changed["files"], fns):
            print(f"  skip (no pre-existing changed function): {repo} {sha[:10]}")
            continue
        cases.append({"commit": full, "url": url, "label": True, "repo_dir": repo_dir,
                      "files": changed["files"], "functions": fns,
                      "changed_lines": lines, "truth_diff": raw})
    return cases


def _adhoc_case(repo, sha):
    """A single ad-hoc fix case from a local repository (smoke tests, examples)."""
    repo_dir = os.path.abspath(repo)
    full = subprocess.run(["git", "rev-parse", sha], cwd=repo_dir,
                          capture_output=True, text=True).stdout.strip()
    files, lines = _commit_shape(repo_dir, full)
    changed, raw = _changed_functions(repo_dir, full)
    return {"commit": full, "url": f"file://{repo_dir}", "label": True,
            "repo_dir": repo_dir, "files": changed["files"],
            "functions": changed["functions"], "changed_lines": lines,
            "truth_diff": raw}


async def _run(args):
    cfg = args  # model, effort, judge, hint, budget, max_iters live on args
    cfg.provider = [p.strip() for p in args.provider.split(",")] if args.provider else None
    cfg.ignore_provider = ([p.strip() for p in args.ignore_provider.split(",")]
                           if args.ignore_provider else None)
    if args.task == "classify":
        arms = [a.strip() for a in args.arms.split(",")] if args.arms \
            else ["no_tool", "with_tool"]
        results = args.out or results_path("classify", args.model)
        print(f"selecting {args.n} confident-mistake cases "
              f"({'C only' if not args.include_cpp else 'C and C++'}"
              f"{f', skipping first {args.skip}' if args.skip else ''}) …")
        cases = select_cases(args.n, include_cpp=args.include_cpp, skip=args.skip)
        print(f"selected {len(cases)} cases (label True/False = "
              f"{sum(c['label'] for c in cases)}/{sum(not c['label'] for c in cases)})")
        for c in cases:
            print(f"  {c['label']!s:5} batch_said={c['fixes_vulnerability']:7} "
                  f"{c['url'].split('/')[-1]:14} {c['commit'][:10]}")
        runner = lambda c: run_classify_case(cfg, c, arms, args.dry_run, args.quiet)
    else:
        arms = [a.strip() for a in args.arms.split(",")] if args.arms else ["self", "tool"]
        results = args.out or results_path("fix", args.model)
        if args.repo:
            cases = [_adhoc_case(args.repo, args.sha or "HEAD")]
            print(f"ad-hoc case: {args.repo} @ {cases[0]['commit'][:10]} "
                  f"({', '.join(cases[0]['functions'])})")
        elif args.cases:
            print(f"loading curated cases from {args.cases} …")
            cases = load_case_list(args.cases)
            print(f"loaded {len(cases)} cases")
            for c in cases:
                print(f"  {c['url'].split('/')[-1]:14} {c['commit'][:10]}  "
                      f"{', '.join(c['functions'])}  ({c['changed_lines']} lines)")
        else:
            print(f"selecting {args.n} small vulnerability-fixing commits "
                  f"(<= {args.max_functions} functions, <= {args.max_lines} lines"
                  f"{f', skipping first {args.skip}' if args.skip else ''}) …")
            cases = select_fix_cases(args.n, skip=args.skip,
                                     max_functions=args.max_functions,
                                     max_lines=args.max_lines)
            print(f"selected {len(cases)} cases")
            for c in cases:
                print(f"  {c['url'].split('/')[-1]:14} {c['commit'][:10]}  "
                      f"{', '.join(c['functions'])}  ({c['changed_lines']} lines)")
        runner = lambda c: run_fix_case(cfg, c, arms, args.dry_run, args.quiet)

    cfg.results_file = results
    print(f"model: {args.model} @ {args.effort} | judge: {args.judge} | arms: "
          f"{', '.join(arms)} | hint: {args.hint} | budget: {args.budget or 'none'} "
          f"| results: {results}")
    if args.dry_run:
        dry = []
        for c in cases:
            dry.append(await runner(c))
        if args.task == "fix" and dry:
            _print_static([d for d in dry if d])
        print("dry-run complete (plumbing verified; no model calls)")
        return

    done = set()
    if os.path.exists(results):
        done = {json.loads(l)["commit"] for l in open(results)}
    with open(results, "a") as out:
        for i, c in enumerate(cases, 1):
            if c["commit"] in done:
                print(f"[{i}/{len(cases)}] {c['commit'][:10]} already done — skipped")
                continue
            print(f"\n[{i}/{len(cases)}] {c['url'].split('/')[-1]} "
                  f"{c['commit'][:10]} ...", flush=True)
            try:
                rec = await runner(c)
            except Exception as e:
                leaves = _leaf_errors(e)
                for leaf in leaves:
                    print(f"  error: {type(leaf).__name__}: {str(leaf)[:400]}")
                if any(type(x).__name__ in ("AuthenticationError", "SystemExit")
                       for x in leaves):
                    print("\nAuthentication failed — check the API key for this "
                          "provider (ANTHROPIC_API_KEY / OPENROUTER_API_KEY). Aborting.")
                    break
                continue
            if rec is None:
                continue
            out.write(json.dumps(rec) + "\n")
            out.flush()
            for arm in arms:
                a = rec.get(arm)
                if not a:
                    continue
                cost = f"  ${a['cost']:.3f}" if a.get("cost") is not None else ""
                if args.task == "classify":
                    print(f"  {arm:10} {str(a['pred']):8} "
                          f"{'OK' if a['correct'] else 'WRONG':5} "
                          f"{a['total']:>8,} tok  ({a['tool_calls']} tool calls){cost}")
                else:
                    print(f"  {arm:10} judge={a['judge']['fix_quality']:10} "
                          f"{a['total']:>8,} tok  ({a['tool_calls']} tool calls, "
                          f"{a['stop']}){cost}")
    cmd_report(argparse.Namespace(task=args.task, results=[results]))


# --------------------------------- report -----------------------------------

def _median(xs):
    xs = sorted(xs)
    return xs[len(xs) // 2] if xs else 0


def _print_static(recs):
    print("\nstatic context sizes, pre-commit version (chars; tokens ≈ chars/4):")
    print(f"{'repo':14} {'commit':11} {'files':>9} {'functions':>10} "
          f"{'tool ring-1':>12} {'nbhd':>8} {'ratio':>7}")
    ratios = []
    for r in recs:
        s = r["static"]
        ratio = s["tool_chars"] / s["file_chars"] if s["file_chars"] else float("nan")
        ratios.append(ratio)
        print(f"{r['url'].split('/')[-1]:14} {r['commit'][:10]:11} "
              f"{s['file_chars']:>9,} {s['fn_chars']:>10,} {s['tool_chars']:>12,} "
              f"{s.get('nbhd_chars', 0):>8,} {ratio:>7.2f}")
    if ratios:
        print(f"median tool/files ratio: {_median(ratios):.2f}")


def _glob_results(task):
    import glob
    pat = "agent_probe" if task == "classify" else "agent_fix"
    files = sorted(glob.glob(f"eval/results/{pat}*.jsonl"))
    return files


def cmd_report(args):
    paths = args.results or _glob_results(args.task)
    paths = [p for p in paths if os.path.exists(p)]
    if not paths:
        print(f"no results — run `run --task {args.task}` first")
        return
    if args.task == "fix":
        if len(paths) > 1:
            _report_fix_models(paths)
        for p in paths:
            _report_fix(p)
        return
    for p in paths:
        _report_classify(p)


def _report_fix_models(paths):
    """Cross-model summary: one line per (model, arm)."""
    print("\nFix task — summary across models (rows = results files):")
    print(f"{'model':42} {'hint':14} {'arm':9} {'n':>3} {'equiv':>6} {'>=part':>7} "
          f"{'rc ok':>6} {'mean tok':>9} {'final ctx':>10} {'calls':>6} {'$/case':>7}")
    for p in paths:
        recs = [json.loads(l) for l in open(p)]
        if not recs:
            continue
        model = recs[0].get("model", "anthropic:claude-opus-4-8")
        hint = recs[0].get("hint", "function+file")
        for arm in ("self", "tool", "semantic"):
            rs = [r[arm] for r in recs if arm in r]
            if not rs:
                continue
            sc = [a["judge"]["score"] for a in rs]
            toks = [a["total"] for a in rs]
            ctx = [a.get("final_ctx", 0) for a in rs]
            calls = [a.get("tool_calls", 0) for a in rs]
            costs = [a["cost"] for a in rs if a.get("cost") is not None]
            cost = f"{sum(costs) / len(costs):.3f}" if len(costs) == len(rs) else "n/a"
            rc = sum(1 for a in rs if a["judge"].get("root_cause_match") == "correct")
            hint_s = hint + ("+src" if recs[0].get("seed_source") else "")
            print(f"{model:42} {hint_s:14} {arm:9} {len(rs):>3} {sum(x == 2 for x in sc):>6} "
                  f"{sum(x >= 1 for x in sc):>7} {rc:>6} {sum(toks) / len(toks):>9,.0f} "
                  f"{sum(ctx) / len(ctx):>10,.0f} {sum(calls) / len(calls):>6.1f} {cost:>7}")


def _report_classify(results):
    recs = [json.loads(l) for l in open(results)]
    if not recs:
        print("no results yet")
        return
    arms = [a for a in ("no_tool", "self", "with_tool") if any(a in r for r in recs)]
    print(f"\nAgent exploration vs. one-shot — {results} "
          f"({MODEL} @ {EFFORT}, n={len(recs)})")
    print(f"{'arm':10} {'n':>3} {'acc':>6} {'mean tok':>9} {'median tok':>11} "
          f"{'final ctx':>10} {'calls':>6} {'no verdict':>11}")
    for arm in arms:
        rs = [r[arm] for r in recs if arm in r]
        # score from the stored prediction so old rows are re-scored honestly:
        # a missing verdict counts as wrong
        accs = [((a.get("pred") == "yes") == bool(r["label"])) and a.get("pred") is not None
                for r in recs if arm in r for a in [r[arm]]]
        toks = [a["total"] for a in rs]
        ctx = [a["final_ctx"] for a in rs if a.get("final_ctx")]
        calls = [a.get("tool_calls", 0) for a in rs]
        nov = sum(1 for a in rs if a.get("pred") is None)
        print(f"{arm:10} {len(rs):>3} {sum(accs) / len(accs):>6.3f} "
              f"{sum(toks) / len(toks):>9,.0f} {_median(toks):>11,} "
              f"{(f'{sum(ctx) / len(ctx):,.0f}' if ctx else 'n/a'):>10} "
              f"{sum(calls) / len(calls):>6.1f} {nov:>11}")
    if "no_tool" in arms:
        for arm in arms:
            if arm == "no_tool":
                continue
            pairs = [r for r in recs if arm in r and "no_tool" in r]
            ok = lambda a, r: a.get("pred") is not None and \
                (a["pred"] == "yes") == bool(r["label"])
            rescued = sum(1 for r in pairs if not ok(r["no_tool"], r) and ok(r[arm], r))
            broke = sum(1 for r in pairs if ok(r["no_tool"], r) and not ok(r[arm], r))
            print(f"\n{arm}: rescued {rescued} case(s) the one-shot got wrong; "
                  f"broke {broke}.")
    print("\nper case:")
    hdr = f"{'repo':14} {'commit':11} {'truth':6}" + "".join(
        f" {a:>10} {'tok':>8}" for a in arms)
    print(hdr)
    for r in recs:
        row = f"{r['url'].split('/')[-1]:14} {r['commit'][:10]:11} " \
              f"{('FIX' if r['label'] else 'not'):6}"
        for a in arms:
            if a in r:
                row += f" {str(r[a]['pred'] or '-'):>10} {r[a]['total']:>8,}"
            else:
                row += f" {'':>10} {'':>8}"
        print(row)


def _report_fix(results):
    recs = [json.loads(l) for l in open(results)]
    if not recs:
        print("no results yet")
        return
    arms = [a for a in ("self", "tool", "semantic") if any(a in r for r in recs)]
    model = recs[0].get("model", "anthropic:claude-opus-4-8")
    print(f"\nFix task — {results} ({model} @ {recs[0].get('effort', EFFORT)}, "
          f"hint {recs[0].get('hint', 'function+file')}, budget "
          f"{recs[0].get('budget') or 'none'}, judge {recs[0].get('judge', JUDGE_MODEL)}, "
          f"n={len(recs)})")
    print(f"{'arm':8} {'n':>3} {'equiv':>6} {'>=part':>7} {'rc ok':>6} {'score':>6} "
          f"{'mean tok':>9} {'median tok':>11} {'final ctx':>10} {'calls':>6} "
          f"{'no sub':>7}")
    for arm in arms:
        rs = [r[arm] for r in recs if arm in r]
        sc = [a["judge"]["score"] for a in rs]
        rc = sum(1 for a in rs if a["judge"].get("root_cause_match") == "correct")
        toks = [a["total"] for a in rs]
        ctx = [a.get("final_ctx", 0) for a in rs]
        calls = [a.get("tool_calls", 0) for a in rs]
        nosub = sum(1 for a in rs if not a.get("submission"))
        print(f"{arm:8} {len(rs):>3} {sum(s == 2 for s in sc):>6} "
              f"{sum(s >= 1 for s in sc):>7} {rc:>6} {sum(sc) / len(sc):>6.2f} "
              f"{sum(toks) / len(toks):>9,.0f} {_median(toks):>11,} "
              f"{sum(ctx) / len(ctx):>10,.0f} {sum(calls) / len(calls):>6.1f} {nosub:>7}")
    for other in ("tool", "semantic"):
        pairs = [r for r in recs if "self" in r and other in r]
        if not pairs:
            continue
        ratios = [r[other]["total"] / r["self"]["total"] for r in pairs
                  if r["self"]["total"]]
        cratios = [r[other]["final_ctx"] / r["self"]["final_ctx"] for r in pairs
                   if r["self"].get("final_ctx") and r[other].get("final_ctx")]
        line = (f"\npaired {other}/self ratio — total tokens: median {_median(ratios):.2f} "
                f"(mean {sum(ratios) / len(ratios):.2f})")
        if cratios:
            line += f"; final context: median {_median(cratios):.2f}"
        print(line)
        both_ok = sum(1 for r in pairs if r["self"]["judge"]["score"] >= 1
                      and r[other]["judge"]["score"] >= 1)
        only_other = sum(1 for r in pairs if r["self"]["judge"]["score"] == 0
                         and r[other]["judge"]["score"] >= 1)
        only_self = sum(1 for r in pairs if r["self"]["judge"]["score"] >= 1
                        and r[other]["judge"]["score"] == 0)
        print(f"root cause found by both: {both_ok}/{len(pairs)}; only {other}: "
              f"{only_other}; only self: {only_self}")
    print("\nper case:")
    print(f"{'repo':14} {'commit':11} {'lines':>5}" + "".join(
        f" {a + ' judge':>12} {'tok':>8} {'calls':>5}" for a in arms))
    for r in recs:
        row = f"{r['url'].split('/')[-1]:14} {r['commit'][:10]:11} {r['changed_lines']:>5}"
        for a in arms:
            if a in r:
                row += f" {r[a]['judge']['fix_quality']:>12} {r[a]['total']:>8,} " \
                       f"{r[a].get('tool_calls', 0):>5}"
            else:
                row += f" {'':>12} {'':>8} {'':>5}"
        print(row)
    _print_static(recs)


def cmd_models(args):
    rows = providers.list_openrouter_models(args.filter, args.max_in)
    print(f"{'model id':50} {'context':>9} {'$/M in':>7} {'$/M out':>8}  reasoning")
    for mid, ctx, pin, pout, reasoning in rows:
        print(f"{mid:50} {ctx or 0:>9,} {pin:>7.2f} {pout:>8.2f}  {'yes' if reasoning else '-'}")
    print(f"\n{len(rows)} models. Use as --model openrouter:<model id>")


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run", help="run the arms of a task on selected cases")
    r.add_argument("--task", choices=["classify", "fix"], default="classify")
    r.add_argument("--n", type=int, default=6, help="number of cases")
    r.add_argument("--skip", type=int, default=0,
                   help="skip the first N qualifying cases (to run the next batch)")
    r.add_argument("--arms", default=None,
                   help="comma-separated arms (classify: no_tool,self,with_tool; "
                        "fix: self,tool); default no_tool,with_tool / self,tool")
    r.add_argument("--dry-run", action="store_true",
                   help="select cases + check plumbing (+ static sizes), no model calls")
    r.add_argument("--include-cpp", action="store_true",
                   help="classify: also include C++ commits (default: C only)")
    r.add_argument("--max-functions", type=int, default=2,
                   help="fix: max changed functions of the real fix")
    r.add_argument("--max-lines", type=int, default=80,
                   help="fix: max changed lines of the real fix")
    r.add_argument("--quiet", action="store_true",
                   help="suppress live turn-by-turn logging (transcripts still saved)")
    r.add_argument("--model", default=MODEL,
                   help="<provider>:<model>, e.g. anthropic:claude-opus-4-8 or "
                        "openrouter:qwen/qwen3-coder-30b-a3b-instruct (see `models`)")
    r.add_argument("--effort", default=EFFORT,
                   choices=["low", "medium", "high", "xhigh", "max"])
    r.add_argument("--judge", default=JUDGE_MODEL,
                   help="fix: judge model (<provider>:<model>)")
    r.add_argument("--provider", default=None,
                   help="openrouter: pin providers (comma-separated, in order; "
                        "no fallbacks), e.g. --provider SiliconFlow")
    r.add_argument("--ignore-provider", default=None,
                   help="openrouter: never route to these providers (comma-separated)")
    r.add_argument("--hint", default="function", choices=["function", "function+file"],
                   help="fix: what the agent is told (default: function names only)")
    r.add_argument("--seed-source", action="store_true",
                   help="fix: give every arm the named function's verbatim source "
                        "up front, so the arms differ only in how they gather "
                        "its context (callees, callers, types)")
    r.add_argument("--budget", type=int, default=None,
                   help="total tokens per arm after which the submission is forced")
    r.add_argument("--max-iters", type=int, default=None,
                   help="override the turn limit (classify 16 / fix 24)")
    r.add_argument("--repo", default=None,
                   help="fix: run one ad-hoc case from this local repository")
    r.add_argument("--sha", default=None, help="fix: commit for --repo (default HEAD)")
    r.add_argument("--cases", default=None,
                   help="fix: curated case list file (`<repo url> <sha>` per line)")
    r.add_argument("--out", default=None,
                   help="results file (default: eval/results/agent_<task>_<model>.jsonl)")
    r.set_defaults(func=lambda a: asyncio.run(_run(a)))

    p = sub.add_parser("report", help="print the comparison tables")
    p.add_argument("--task", choices=["classify", "fix"], default="classify")
    p.add_argument("results", nargs="*", default=None,
                   help="results files (default: every agent_<task>*.jsonl)")
    p.set_defaults(func=cmd_report)

    m = sub.add_parser("models", help="list tool-capable OpenRouter models")
    m.add_argument("--filter", default=None, help="regex on the model id")
    m.add_argument("--max-in", type=float, default=None, help="max $/M input tokens")
    m.set_defaults(func=cmd_models)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
