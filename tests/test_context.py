"""`crossslice context FILE:LINE`: the function containing a line, its
neighborhood, and the def-use slice around that line (shared helper used by
the CLI, the MCP server and the editor integration)."""
import shutil
from pathlib import Path

import pytest

from crossslice.cross.graph import RepoGraph
from crossslice.cross.context import locate, neighborhood_text, context_at

pytestmark = pytest.mark.skipif(shutil.which("gtags") is None, reason="GNU Global (gtags) not installed")
EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "taskrunner"


@pytest.fixture
def repo(tmp_path):
    dst = tmp_path / "taskrunner"
    shutil.copytree(EXAMPLE, dst, ignore=shutil.ignore_patterns(
        "GTAGS", "GRTAGS", "GPATH", ".cce_graph_*", "taskrunner", "*.o"))
    return dst


def _line_of(repo, rel, needle, after=0):
    for i, text in enumerate((repo / rel).read_text().split("\n"), 1):
        if i > after and needle in text:
            return i
    raise AssertionError(f"{needle!r} not found in {rel}")


def test_locate_and_neighborhood_with_slice(repo):
    line = _line_of(repo, "src/sched.c", "queue_push(", after=40)   # inside sched_submit
    with RepoGraph(str(repo)) as g:
        loc = locate(g, "src/sched.c", line)
        assert loc["name"] == "sched_submit"
        text = neighborhood_text(g, location=loc, point_line=line, show_slice=True)
    assert text.startswith("sched_submit — src/sched.c:")
    assert "reads: s, t" in text
    assert f"SLICE around line {line}" in text and "\n>" in text       # seed marked
    assert "CALLEES" in text and "queue_push (src/queue.c:" in text
    assert "LOG_ERROR [macro]" in text and "validate_task (src/sched.c:" in text
    assert "CALLERS" in text and "main (src/main.c:" in text


def test_line_outside_any_function(repo):
    with RepoGraph(str(repo)) as g:
        assert locate(g, "src/sched.c", 1) is None                      # file header
        res = context_at(g, "src/sched.c", 1)
    assert isinstance(res, dict) and "not inside a function" in res["error"]


def test_cli_context(repo, capsys):
    from crossslice.cli import main
    line = _line_of(repo, "src/sched.c", "queue_push(", after=40)
    rc = main(["context", f"{repo}/src/sched.c:{line}", "--repo", str(repo), "--slice"])
    out = capsys.readouterr().out
    assert rc == 0
    assert out.startswith("sched_submit —") and "CALLERS" in out
    rc = main(["context", f"{repo}/src/sched.c:1", "--repo", str(repo)])
    assert rc == 1


def test_existing_compile_db_in_hidden_directory_is_ignored(tmp_path):
    from crossslice.cross.py_clangd_bridge import CompileDBBuilder
    (tmp_path / ".py_clangd_bridge").mkdir()
    (tmp_path / ".py_clangd_bridge" / "compile_commands.json").write_text("[]")
    builder = CompileDBBuilder(tmp_path, tmp_path / "work")
    assert builder._find_existing_db() is None
    (tmp_path / "build").mkdir()
    (tmp_path / "build" / "compile_commands.json").write_text("[]")
    assert builder._find_existing_db() == (tmp_path / "build" / "compile_commands.json").resolve()
