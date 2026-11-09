"""Zero-configuration behavior: the repository is found from the current
directory, commit mode needs git (and says so), code-context mode works on any
directory, and nothing is ever written into the analyzed checkout."""
import os
import shutil
import subprocess
import time
from pathlib import Path

import pytest

from crossslice.paths import NO_GIT, find_workspace, repo_cache

needs_gtags = pytest.mark.skipif(shutil.which("gtags") is None,
                                 reason="GNU Global (gtags) not installed")
EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "taskrunner"


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                            GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t"))


@pytest.fixture
def plain(tmp_path):
    """The taskrunner example as a plain directory (no git)."""
    dst = tmp_path / "taskrunner"
    shutil.copytree(EXAMPLE, dst, ignore=shutil.ignore_patterns(
        "GTAGS", "GRTAGS", "GPATH", ".cce_graph_*", "taskrunner", "*.o"))
    return dst


@pytest.fixture
def gitrepo(plain):
    """The example as a git repository with two commits (the second changes
    sched_submit), so commit mode has a parent to compare with."""
    _git(plain, "init", "-q", "-b", "main")
    _git(plain, "add", "-A")
    _git(plain, "commit", "-q", "-m", "initial")
    sched = plain / "src" / "sched.c"
    sched.write_text(sched.read_text().replace("int sched_submit(sched_t *s, task_t *t)\n{",
                                               "int sched_submit(sched_t *s, task_t *t)\n{\n"
                                               "    if (!s) return -1;", 1))
    _git(plain, "commit", "-q", "-am", "sched_submit: reject a NULL scheduler")
    return plain


def _status(repo):
    return subprocess.run(["git", "-C", str(repo), "status", "--porcelain", "--ignored"],
                          capture_output=True, text=True).stdout


# ---- workspace resolution ---------------------------------------------------

def test_workspace_from_subdirectory(gitrepo, monkeypatch):
    monkeypatch.chdir(gitrepo / "src")                     # implicit: the git top level
    ws = find_workspace()
    assert ws.is_git and Path(ws.root) == gitrepo and Path(ws.git_root) == gitrepo


def test_explicit_directory_is_the_root(gitrepo):
    ws = find_workspace(str(gitrepo / "src"))             # explicit: as given
    assert Path(ws.root) == gitrepo / "src" and Path(ws.git_root) == gitrepo


@needs_gtags
def test_subdirectory_at_a_revision(gitrepo):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(gitrepo / "src"), commit="HEAD~1") as g:
        assert len(g.commit) == 40                           # resolved, cache keyed by SHA
        assert Path(g.root).name == "src" and (Path(g.root) / "sched.c").exists()
        assert g.expand("sched_submit") is not None
    assert _status(gitrepo) == ""


def test_workspace_without_git(plain):
    ws = find_workspace(str(plain))
    assert not ws.is_git and Path(ws.root) == plain


def test_cache_is_outside_the_repository(plain):
    c = repo_cache(str(plain))
    assert c.startswith(os.environ["CROSSSLICE_CACHE_DIR"])
    assert c == repo_cache(str(plain))                     # stable
    assert (Path(c) / "repo.txt").read_text().strip() == os.path.realpath(plain)


# ---- nothing is written into the checkout --------------------------------------

@needs_gtags
def test_graph_leaves_the_checkout_untouched(gitrepo):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(gitrepo)) as g:
        assert g.expand("sched_submit") is not None
        cache = Path(g.cache_dir)
    with RepoGraph(str(gitrepo), commit="HEAD~1") as g:   # temporary worktree
        assert g.expand("sched_submit") is not None
    assert _status(gitrepo) == ""
    assert (cache / "gtags" / "worktree" / "GTAGS").exists()
    assert list(cache.glob("graph-*.db"))
    out = subprocess.run(["git", "-C", str(gitrepo), "worktree", "list"],
                         capture_output=True, text=True).stdout
    assert out.count("\n") == 1                            # worktree removed again


@needs_gtags
def test_external_index_is_updated_incrementally(plain):
    from crossslice.cross.gtags_handler import GtagsHandler
    db = plain.parent / "db"
    h = GtagsHandler(str(plain), dbpath=str(db))
    assert h.ensure_index()
    assert not (plain / "GTAGS").exists() and (db / "GTAGS").exists()
    assert h.find_function_definition("sched_submit")
    src = plain / "src" / "sched.c"
    src.write_text(src.read_text() + "\nint added_later(void) { return 1; }\n")
    later = time.time() + 5
    os.utime(src, (later, later))                          # gtags -i compares mtimes
    assert h.update()
    assert h.find_function_definition("added_later")


# ---- CLI ----------------------------------------------------------------------

@needs_gtags
def test_context_works_without_git(plain, capsys, monkeypatch):
    from crossslice.cli import main
    monkeypatch.chdir(plain)
    line = next(i for i, t in enumerate((plain / "src/sched.c").read_text().split("\n"), 1)
                if i > 40 and "queue_push(" in t)
    assert main(["context", f"src/sched.c:{line}"]) == 0
    cap = capsys.readouterr()
    assert cap.out.startswith("sched_submit —")
    assert NO_GIT in cap.err
    assert not (plain / "GTAGS").exists()


def test_enrich_without_git_explains(plain, capsys, monkeypatch):
    from crossslice.cli import main
    monkeypatch.chdir(plain)
    assert main(["enrich"]) == 2
    assert NO_GIT in capsys.readouterr().err


def test_enrich_bad_revision(gitrepo, capsys, monkeypatch):
    from crossslice.cli import main
    monkeypatch.chdir(gitrepo)
    assert main(["enrich", "no-such-rev"]) == 2
    assert "is not a commit" in capsys.readouterr().err


@needs_gtags
def test_expand_shapes(gitrepo, capsys, monkeypatch):
    from crossslice.cli import main
    monkeypatch.chdir(gitrepo / "src")                     # from a subdirectory
    assert main(["expand", "sched_submit"]) == 0
    out = capsys.readouterr().out
    assert out.startswith("sched_submit — src/sched.c:") and "callers" in out
    monkeypatch.chdir(gitrepo.parent)                      # older form: repo first
    assert main(["expand", str(gitrepo), "sched_submit"]) == 0
    assert capsys.readouterr().out.startswith("sched_submit —")
    assert main(["expand", "-C", str(gitrepo), "no_such_function_xyz"]) == 1


# ---- MCP sessions -----------------------------------------------------------

@needs_gtags
def test_mcp_working_tree_and_commit_versions(gitrepo):
    from crossslice.cross import mcp_server as m
    s = m.Session(str(gitrepo), str(gitrepo))
    m.SESSION, m.LOCK = s, None
    try:
        ctx, version = m._target(None)
        assert version == "work" and ctx.sha is None
        work = ctx.summary("sched_submit", "work")
        ctx, version = m._target("old")
        assert version == "old" and ctx.prev is not None
        old = ctx.summary("sched_submit", "old")
        assert len(work["returns"]) == len(old["returns"]) + 1   # the new early return
        root = s.commit_ctx("HEAD~1")                       # root commit: allowed, no old version
        assert root.is_root
        with pytest.raises(m.ToolError, match="root commit"):
            root.graph("old")
        with pytest.raises(m.ToolError, match="not a commit"):
            s.commit_ctx("nope")
    finally:
        s.close()


def test_mcp_without_git(plain):
    from crossslice.cross import mcp_server as m
    s = m.Session(str(plain), None)
    m.SESSION, m.LOCK = s, None
    try:
        assert m._target(None)[1] == "work"
        with pytest.raises(m.ToolError, match="not a git repository"):
            m._target("new")
    finally:
        s.close()


# ---- explorer commit list ------------------------------------------------------

@needs_gtags
def test_explorer_commit_list(gitrepo, plain):
    from crossslice.cross.graph import RepoGraph
    from crossslice.cross.graph_server import GraphService
    with RepoGraph(str(gitrepo)) as g:
        rows = GraphService(g, git_root=str(gitrepo)).commits()["commits"]
    assert [r["subject"] for r in rows] == ["sched_submit: reject a NULL scheduler", "initial"]


# ---- editor endpoints (VS Code extension) ---------------------------------------

@needs_gtags
def test_editor_endpoints(gitrepo):
    from crossslice.cross.graph import RepoGraph
    from crossslice.cross.graph_server import GraphService
    with RepoGraph(str(gitrepo)) as g:
        svc = GraphService(g, git_root=str(gitrepo))
        h = svc.health()
        assert h["ok"] and h["is_git"] and h["repo"] == str(gitrepo)
        fns = svc.functions("src/sched.c")["functions"]
        names = {f["name"]: f for f in fns}
        assert "sched_submit" in names and names["sched_submit"]["line"] < names["sched_submit"]["end_line"]
        line = names["sched_submit"]["line"] + 2
        r = svc.context("src/sched.c", line)                      # relative path
        assert r["text"].startswith("sched_submit —") and f"SLICE around line {line}" in r["text"]
        r2 = svc.context(str(gitrepo / "src" / "sched.c"), line, show_slice=False)   # absolute path
        assert r2["file"] == "src/sched.c" and "SLICE" not in r2["text"]
        with pytest.raises(ValueError, match="not inside a function"):
            svc.context("src/sched.c", 1)
        with pytest.raises(ValueError, match="outside"):
            svc.context("/etc/passwd", 1)
        with pytest.raises(ValueError, match="no such file"):
            svc.functions("nope.c")


# ---- tool discovery -------------------------------------------------------------

def test_find_gumtree_prefers_env_then_known_places(tmp_path, monkeypatch):
    from crossslice.paths import find_gumtree, _gumtree_version
    launcher = tmp_path / "gumtree-4.0.0-beta3" / "bin" / "gumtree"
    launcher.parent.mkdir(parents=True)
    launcher.write_text("#!/bin/sh\n")
    monkeypatch.setenv("GUMTREE_PATH", str(launcher))
    assert find_gumtree() == str(launcher)
    monkeypatch.setenv("GUMTREE_PATH", str(tmp_path / "missing"))      # dangling: ignored
    assert find_gumtree() != str(tmp_path / "missing")
    assert _gumtree_version("/opt/gumtree/gumtree-4.0.0-beta3/bin/gumtree") > \
        _gumtree_version("/opt/gumtree/gumtree-3.0.0/bin/gumtree")
