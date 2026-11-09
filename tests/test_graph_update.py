"""RepoGraph.update() must make the persistent graph answer like a rebuilt
one after the repository changed: removed calls and callers disappear, new
callers appear, moved definitions are found again, and an edit in the same
second as the previous index write is not missed (gtags -i compares mtimes
with one-second granularity)."""
import os
import shutil

import pytest

from crossslice.cross.graph import RepoGraph

pytestmark = pytest.mark.skipif(shutil.which("gtags") is None, reason="GNU Global (gtags) not installed")

V1 = {
    "a.c": "int b(int x);\nint c(int x);\nint a(int x)\n{\n    return b(x) + c(x);\n}\n",
    "b.c": "int helper(int x) { return x; }\nint b(int x) { return helper(x) + 1; }\nint c(int x) { return x + 2; }\nint d(int x) { return b(x); }\n",
}
# a no longer calls c; d no longer calls b; e is a new caller of b; b moved down two lines
# (its old line is now inside c: analysing there would make c's body b's)
V2 = {
    "a.c": "int b(int x);\nint c(int x);\nint a(int x)\n{\n    return b(x);\n}\n",
    "b.c": "int helper(int x) { return x; }\nint c(int x) { return x + 2; }\nint d(int x) { return x; }\nint b(int x) { return helper(x) + 1; }\nint e(int x) { return b(x); }\n",
}


def _write(repo, files):
    for name, text in files.items():
        (repo / name).write_text(text)


def _answers(g, names):
    out = {}
    for n in names:
        g.expand(n, levels=1)
        h = g.neighborhood(n)
        out[n] = (sorted({(c["name"], c["call_line"]) for c in h["callees"]}),
                  sorted({(c["name"], c["call_line"]) for c in h["callers"]}))
    return out


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _write(r, V1)
    return r


def test_update_matches_a_rebuild(repo, tmp_path):
    names = ["a", "b"]
    with RepoGraph(str(repo), db_path=str(tmp_path / "inc.db"), cache_dir=str(tmp_path / "inc")) as g:
        before = _answers(g, names)
        _write(repo, V2)                                   # same second as the index write
        info = g.update()
        after = _answers(g, names)
        n_b = g.db.execute("SELECT COUNT(*) FROM nodes WHERE name='b'").fetchone()[0]
    with RepoGraph(str(repo), db_path=str(tmp_path / "reb.db"), cache_dir=str(tmp_path / "reb")) as g2:
        rebuilt = _answers(g2, names)
    assert before["a"][0] == [("b", 4), ("c", 4)] and [n for n, _ in before["b"][1]] == ["a", "d"]
    assert info["stale_nodes"] >= 1
    assert after == rebuilt
    assert after["a"][0] == [("b", 4)]                     # removed call gone
    assert [n for n, _ in after["b"][1]] == ["a", "e"]     # removed caller gone, new caller found
    assert [n for n, _ in after["b"][0]] == ["helper"]     # b analysed at its new line, not c's body
    assert n_b == 1                                        # one node per name after the move


def test_update_without_change_keeps_everything(repo, tmp_path):
    with RepoGraph(str(repo), db_path=str(tmp_path / "g.db"), cache_dir=str(tmp_path / "c")) as g:
        before = _answers(g, ["a", "b"])
        nodes_before = g.stats()["nodes"]
        info = g.update()
        assert info["stale_nodes"] == 0
        assert _answers(g, ["a", "b"]) == before
        assert g.stats()["nodes"] == nodes_before


def test_index_catches_same_second_change_in_untouched_file(repo, tmp_path):
    """A file the graph has no node in changes in the same second as the index
    was written: `gtags -i` would miss it (mtime granularity); the manifest
    must not."""
    (repo / "d.c").write_text("int b(int x);\nint d(int x) { return x; }\n")
    with RepoGraph(str(repo), db_path=str(tmp_path / "g.db"), cache_dir=str(tmp_path / "c")) as g:
        g.expand("b", direction="down")                        # index written now; d.c gets no node
        (repo / "d.c").write_text("int b(int x);\nint d(int x) { return b(x); }\n")
        g.update()
        g.expand("b", direction="up")
        callers = {c["name"] for c in g.neighborhood("b")["callers"]}
    assert "d" in callers


def test_twin_names_mean_what_the_cascade_picks(tmp_path):
    """`foo` is a library function and also a static wrapper in a test file.
    When the wrapper's node exists first (reached through a caller lookup),
    a lookup of `foo` must still mean the library definition."""
    repo = tmp_path / "repo"
    (repo / "tests").mkdir(parents=True)
    (repo / "lib.c").write_text("int helper(int x) { return x; }\nint foo(int x) { return helper(x); }\n")
    (repo / "tests" / "foo_wrap.c").write_text("int baz(int x);\nstatic int foo(int x) { return baz(x); }\n")
    (repo / "tests" / "t.c").write_text("int baz(int x) { return x; }\nint qux(int x) { return foo(x); }\n")
    with RepoGraph(str(repo), db_path=str(tmp_path / "g.db"), cache_dir=str(tmp_path / "c")) as g:
        g.expand("baz", direction="up")                        # creates the wrapper's node first
        g.expand("qux", direction="down")                      # and the library foo through the callee path
        assert g.db.execute("SELECT COUNT(*) FROM nodes WHERE name='foo'").fetchone()[0] == 2
        g.expand("foo")
        callees = {c["name"] for c in g.neighborhood("foo")["callees"]}
    assert callees == {"helper"}


def test_moved_function_reached_through_a_caller_keeps_one_node(repo, tmp_path):
    """After b moved, resolving it again through a's callee edge must merge
    into b's stale node instead of leaving two nodes for the name."""
    with RepoGraph(str(repo), db_path=str(tmp_path / "g.db"), cache_dir=str(tmp_path / "c")) as g:
        g.expand("a"); g.expand("b")
        _write(repo, V2)
        g.update()
        g.expand("a")                                          # callee path first
        assert g.db.execute("SELECT COUNT(*) FROM nodes WHERE name='b'").fetchone()[0] == 1
        g.expand("b")
        assert [n for n, _ in sorted({(c["name"], c["call_line"]) for c in g.neighborhood("b")["callers"]})] == ["a", "e"]
        assert g.db.execute("SELECT COUNT(*) FROM nodes WHERE name='b'").fetchone()[0] == 1
