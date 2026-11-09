"""Where CrossSlice finds the repository and where it keeps its caches.

Every front end (CLI, explorer, MCP server, editor) resolves its target the
same way. A directory named explicitly (`-C DIR`, a positional REPO) is the
analysis root as given, so `crossslice explore examples/taskrunner` analyzes
just that example even inside a larger repository. Without one, the root is
the git top level containing the current directory, else the current
directory. Commit mode needs git and always works on the whole repository
(`git_root`); code-context mode works on any directory of C sources.

Caches (graph stores, GNU Global indexes, clangd's compile database) live
outside the checkout, so the tool never writes into the user's repository:

    $CROSSSLICE_CACHE_DIR            (if set), else
    $XDG_CACHE_HOME/crossslice       (if set), else
    ~/.cache/crossslice
        <repo-name>-<hash of its absolute path>/
            graph-worktree.db        graph of the working tree
            graph-<sha12>.db         graph of one commit
            gtags/worktree/          GNU Global index of the working tree
            gtags/<sha>/             GNU Global index of one commit (reused)
            clangd/                  synthesized compile_commands.json
            repo.txt                 which checkout this folder belongs to
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
from dataclasses import dataclass
from typing import Optional

NO_GIT = ("not a git repository: commit mode unavailable, code-context mode works "
          "(context, expand, explore)")


def cache_root(cache_dir: Optional[str] = None) -> str:
    base = (cache_dir or os.environ.get("CROSSSLICE_CACHE_DIR")
            or os.path.join(os.environ.get("XDG_CACHE_HOME") or "~/.cache", "crossslice"))
    return os.path.abspath(os.path.expanduser(base))


def repo_cache(repo_path: str, cache_dir: Optional[str] = None) -> str:
    """The cache folder of one checkout (created on first use)."""
    repo = os.path.realpath(repo_path)
    key = hashlib.sha1(repo.encode("utf-8")).hexdigest()[:12]
    name = re.sub(r"[^A-Za-z0-9._-]", "_", os.path.basename(repo) or "root")
    path = os.path.join(cache_root(cache_dir), f"{name}-{key}")
    os.makedirs(path, exist_ok=True)
    marker = os.path.join(path, "repo.txt")
    if not os.path.exists(marker):
        try:
            with open(marker, "w", encoding="utf-8") as f:
                f.write(repo + "\n")
        except OSError:
            pass
    return path


def git_toplevel(path: str) -> Optional[str]:
    try:
        out = subprocess.check_output(["git", "-C", path, "rev-parse", "--show-toplevel"],
                                      stderr=subprocess.DEVNULL, text=True).strip()
        return out or None
    except (subprocess.CalledProcessError, FileNotFoundError, NotADirectoryError):
        return None


def has_commits(root: str) -> bool:
    return subprocess.run(["git", "-C", root, "rev-parse", "--verify", "-q", "HEAD"],
                          capture_output=True).returncode == 0


@dataclass
class Workspace:
    root: str                 # analysis root (graph, index, context)
    git_root: Optional[str]   # top level of the enclosing git repository, if any

    @property
    def is_git(self) -> bool:
        return self.git_root is not None

    def require_git(self) -> None:
        """Raise a user-facing error when commit mode is not available here."""
        if not self.is_git:
            raise NotAGitRepository(f"{self.root}: {NO_GIT}")


class NotAGitRepository(RuntimeError):
    pass


class MissingTool(FileNotFoundError):
    """An external tool CrossSlice needs is not installed; the message says which
    one and how to get it. Every front end turns it into a one-line answer."""


def find_workspace(path: Optional[str] = None) -> Workspace:
    """Resolve the analysis root: `path` itself when given, else the git top
    level containing the current directory, else the current directory."""
    start = os.path.abspath(os.path.expanduser(path or os.getcwd()))
    if not os.path.isdir(start):
        raise FileNotFoundError(f"{path}: no such directory")
    top = git_toplevel(start)
    top = os.path.realpath(top) if top else None
    if path:
        return Workspace(start, top)
    return Workspace(top or start, top)


# ---- external tools -----------------------------------------------------------

_GUMTREE_GLOBS = (
    "{cache}/gumtree/gumtree-*/bin/gumtree",          # crossslice check --install (planned)
    "/opt/gumtree/gumtree-*/bin/gumtree", "/opt/gumtree-*/bin/gumtree", "/opt/gumtree/bin/gumtree",
    "/usr/local/gumtree/gumtree-*/bin/gumtree", "/usr/local/gumtree-*/bin/gumtree",
    "~/gumtree/gumtree-*/bin/gumtree", "~/gumtree-*/bin/gumtree",
    "~/.local/gumtree*/bin/gumtree", "~/.local/opt/gumtree*/bin/gumtree", "~/opt/gumtree*/bin/gumtree",
    "/Applications/gumtree*/bin/gumtree",
)


def _gumtree_version(path: str) -> tuple:
    m = re.search(r"gumtree-(\d+)\.(\d+)\.(\d+)(?:-beta(\d+))?", path)
    return tuple(int(x) for x in m.groups(default="0")) if m else (0, 0, 0, 0)


def find_gumtree() -> Optional[str]:
    """The GumTree launcher: $GUMTREE_PATH, `gumtree` on PATH, or a release unpacked
    in a usual place (/opt/gumtree, ~/gumtree, the CrossSlice cache); newest wins."""
    import glob
    import shutil
    env = os.environ.get("GUMTREE_PATH")
    if env and os.path.isfile(env):
        return env
    on_path = shutil.which("gumtree")
    if on_path:
        return on_path
    hits = []
    for pat in _GUMTREE_GLOBS:
        pat = os.path.expanduser(pat.format(cache=cache_root()))
        hits.extend(p for p in glob.glob(pat) if os.path.isfile(p))
    return max(hits, key=_gumtree_version) if hits else None


# ---- shared command-line handling -------------------------------------------

def add_repo_args(ap, positional: bool = True, rev: bool = True) -> None:
    """The options every analysis command shares."""
    if positional:
        ap.add_argument("repo", nargs="?", default=None,
                        help="repository directory (default: the current directory)")
    ap.add_argument("-C", "--repo", dest="repo_opt", metavar="DIR", default=None,
                    help="repository directory (default: the current directory)")
    if rev:
        ap.add_argument("--rev", "--commit", dest="rev", metavar="REV", default=None,
                        help="analyze this git revision (in a temporary worktree) "
                             "instead of the files on disk")
    ap.add_argument("--cache-dir", metavar="DIR", default=None,
                    help="cache root (default: $CROSSSLICE_CACHE_DIR, else "
                         "~/.cache/crossslice); nothing is written into the repository")


def workspace_from_args(args, prog: str, repo: Optional[str] = None):
    """(Workspace, full SHA or None) for parsed `add_repo_args` options.
    Exits with a one-line message on a bad directory or revision."""
    import sys
    try:
        ws = find_workspace(getattr(args, "repo_opt", None) or repo
                            or getattr(args, "repo", None))
    except FileNotFoundError as e:
        print(f"{prog}: {e}", file=sys.stderr)
        raise SystemExit(2)
    rev = getattr(args, "rev", None)
    if not ws.is_git:
        if rev:
            print(f"{prog}: {ws.root}: {NO_GIT}; --rev needs git", file=sys.stderr)
            raise SystemExit(2)
        print(f"note: {ws.root}: {NO_GIT}", file=sys.stderr)
        return ws, None
    if not rev:
        return ws, None
    out = subprocess.run(["git", "-C", ws.root, "rev-parse", "--verify", "-q",
                          f"{rev}^{{commit}}"], capture_output=True, text=True)
    if out.returncode != 0 or not out.stdout.strip():
        print(f"{prog}: {rev!r} is not a commit in {ws.root}", file=sys.stderr)
        raise SystemExit(2)
    return ws, out.stdout.strip()
