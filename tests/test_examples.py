"""Cross-function behavior on the bundled examples: static and macro resolution,
callers with their call sites, expansion levels and directions, the documented
function-pointer limitation, the kvstore fix end to end (needs GumTree), the MCP
tools, "did you mean" suggestions, and the one-line answer for a missing tool."""
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from crossslice.paths import MissingTool, find_gumtree

needs_gtags = pytest.mark.skipif(shutil.which("gtags") is None,
                                 reason="GNU Global (gtags) not installed")
needs_gumtree = pytest.mark.skipif(find_gumtree() is None, reason="GumTree not installed")
EXAMPLES = Path(__file__).resolve().parent.parent / "examples"
IGNORE = shutil.ignore_patterns("GTAGS", "GRTAGS", "GPATH", ".cce_graph_*", "taskrunner", "*.o")


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True,
                   env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t",
                            GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t"))


@pytest.fixture
def taskrunner(tmp_path):
    dst = tmp_path / "taskrunner"
    shutil.copytree(EXAMPLES / "taskrunner", dst, ignore=IGNORE)
    return dst


@pytest.fixture
def kvstore(tmp_path):
    """The kvstore history as init.sh builds it: the vulnerable snapshot, then the fix."""
    repo = tmp_path / "kvstore"
    shutil.copytree(EXAMPLES / "kvstore-evolution" / "old", repo)
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kvstore: initial implementation")
    for f in repo.iterdir():
        if f.name != ".git":
            f.unlink() if f.is_file() else shutil.rmtree(f)
    shutil.copytree(EXAMPLES / "kvstore-evolution" / "new", repo, dirs_exist_ok=True)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "kv_put: reject oversized keys instead of overflowing the entry buffer")
    return repo


# ---- resolution and expansion ---------------------------------------------------

@needs_gtags
def test_static_and_macro_callees_resolve(taskrunner):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner)) as g:
        assert g.expand("sched_submit") is not None
        hood = g.neighborhood("sched_submit")
    node = hood["node"]
    assert node["file"] == "src/sched.c" and node["resolution_method"] == "gtags_unique"
    assert set(node["summary"]["params_read"]) == {"s", "t"}
    callees = {c["name"]: c for c in hood["callees"]}
    assert {"LOG_ERROR", "validate_task", "queue_push", "LOG_INFO"} <= set(callees)
    assert callees["LOG_ERROR"]["kind"] == "macro" and callees["LOG_ERROR"]["file"] == "include/log.h"
    assert callees["validate_task"]["kind"] == "function"          # static helper in the same file
    assert callees["queue_push"]["file"] == "src/queue.c"


@needs_gtags
def test_callers_carry_every_call_site(taskrunner):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner)) as g:
        g.expand("sched_submit")
        callers = g.neighborhood("sched_submit")["callers"]
    assert {c["name"] for c in callers} == {"main"}
    assert len({c["call_line"] for c in callers}) == 2            # main submits twice


@needs_gtags
def test_expand_levels_and_direction(taskrunner, tmp_path):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner), db_path=str(tmp_path / "one.db")) as g:
        g.expand("sched_drain", levels=1)
        one = sum(g.stats()["nodes"].values())
    with RepoGraph(str(taskrunner), db_path=str(tmp_path / "two.db")) as g:
        g.expand("sched_drain", levels=2)
        two = sum(g.stats()["nodes"].values())
    assert two > one
    with RepoGraph(str(taskrunner), db_path=str(tmp_path / "up.db")) as g:
        g.expand("queue_push", direction="up")
        hood = g.neighborhood("queue_push")
    assert "sched_submit" in {c["name"] for c in hood["callers"]}
    assert hood["callees"] == []                                      # up only


@needs_gtags
def test_function_pointer_calls_are_not_followed(taskrunner):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner)) as g:
        g.expand("task_execute")
        names = {c["name"] for c in g.neighborhood("task_execute")["callees"]}
    assert not names & {"work_ok", "work_flaky"}                      # documented limitation


# ---- the kvstore fix, end to end ------------------------------------------------------

@needs_gumtree
@needs_gtags
def test_kvstore_fix_enrichment(kvstore):
    from crossslice.commit import enrich_commit, split_sections
    res = enrich_commit(str(kvstore), "HEAD")
    assert res.functions == ["kv_put"] and set(res.changed_files) == {"kv.c", "kv.h"}
    assert not res.cross_error and not res.note
    assert "+ if (key_len >= KV_MAX_KEY_LEN)" in res.text
    assert "- strcpy(e->key, key);" in res.text
    sections = split_sections(res.text)
    by_kind = {}
    for s in sections:
        by_kind.setdefault(s["kind"], []).append(s.get("name") or s.get("title"))
    assert "find_slot" in by_kind["callee"]
    assert "KV_MAX_KEY_LEN" in by_kind["macro"] and "KV_ERR_KEYLEN" in by_kind["macro"]
    assert set(by_kind["caller"]) == {"kv_grow", "main"}
    assert res.cross_stats["new"]["gtags_unique"] >= 1
    intra = enrich_commit(str(kvstore), "HEAD", cross=False)
    assert "Cross-function context" not in intra.text and "+ if (key_len" in intra.text
    # matcher regressions (Oct 28): an update action names the OLD node, so the
    # unchanged `return KV_ERR_NOMEM;` must not be reported as added; the header's
    # global context must show only the one added #define
    assert "+ return KV_ERR_NOMEM;" not in intra.text and "KV_ERR_NOMEM" not in intra.text
    header = intra.text.split("Context for merged statement of old file: kv.h")[1]
    assert [l for l in header.split("\n") if l.startswith("+")] == ["+ #define KV_ERR_KEYLEN -3"]
    assert not [l for l in header.split("\n") if l.startswith("-")]
    root = enrich_commit(str(kvstore), "HEAD~1", cross=False)       # root commit: everything added
    assert root.note.startswith("root commit") and "+ int kv_put(" in root.text and "main" in root.functions


# ---- MCP tools ------------------------------------------------------------------

@pytest.fixture
def mcp_session(kvstore):
    from crossslice.cross import mcp_server as m
    m.SESSION, m.LOCK = m.Session(str(kvstore), str(kvstore)), None
    yield m
    m.SESSION.close()
    m.SESSION = None


@needs_gtags
def test_mcp_symbol_tools(mcp_session):
    m = mcp_session
    hood = m.get_neighborhood("kv_put")
    assert hood.startswith("kv_put —") and "find_slot" in hood and "CALLERS" in hood
    ctx = m.get_context_at("kv.c", 70)
    assert ctx.startswith("kv_put —") and "SLICE around line 70" in ctx
    old = json.loads(m.get_summary("kv_put", version="old"))
    new = json.loads(m.get_summary("kv_put", version="new"))
    assert "return KV_ERR_KEYLEN;" in new["returns"] and "return KV_ERR_KEYLEN;" not in old["returns"]
    assert "char key[KV_MAX_KEY_LEN]" in m.get_type_definition("kv_entry")
    body = m.get_sliced_body("kv_put")
    assert body.startswith("kv_put (work version)") and "memcpy" in body
    missing = json.loads(m.resolve_symbol("kv_putt"))
    assert missing["resolved"] is False and "kv_put" in missing["did_you_mean"]


@needs_gumtree
@needs_gtags
def test_mcp_commit_tools(mcp_session):
    m = mcp_session
    overview = json.loads(m.get_commit_overview())
    assert overview["changed_functions"] == ["kv_put"] and len(overview["parent"]) == 40
    assert m.list_changed_functions() == json.dumps(["kv_put"], indent=2)
    intra = m.get_intra_diff()
    assert "+ if (key_len >= KV_MAX_KEY_LEN)" in intra
    assert "diff --git" in m.get_raw_diff()
    root = json.loads(m.get_commit_overview(rev="HEAD~1"))   # root commit: everything is new
    assert root["parent"] is None and "root commit" in root["note"]
    assert "kv_put" in root["changed_functions"] and "main" in root["changed_functions"]
    assert "root commit" in json.loads(m.get_summary("kv_put", version="old", rev="HEAD~1"))["error"]
    assert "+ int kv_put(" in m.get_intra_diff(rev="HEAD~1")


@needs_gtags
def test_modref_summaries_see_pointer_writes(mcp_session):
    """Writes through out-parameters, increments of fields, library writers and
    local aliases of a parameter (e = &s->entries[i]; e->v = ..) count as writes."""
    m = mcp_session
    def summary(fn):
        return json.loads(m.get_summary(fn))
    assert summary("kv_get")["params_written"] == ["out_value*"]      # *out_value = ..
    assert summary("kv_put")["params_written"] == ["s*"]              # s->count++, memcpy(e->key..), e->in_use = 1
    assert summary("xstrdup")["params_read"] == ["s"]                 # `char *f(const char *s)`: pointer return type
    assert summary("find_slot")["params_written"] == []               # reads only
    assert summary("kv_grow")["params_written"] == ["s*"]


@needs_gtags
def test_expand_levels_and_one_based_lines(mcp_session):
    m = mcp_session
    one = json.loads(m.expand_function("kv_put", levels=1))
    assert one["node"]["line"] == 63 and "rings" not in one
    callees = {c["name"]: c for c in one["callees"]}
    assert callees["find_slot"]["line"] == 18 and callees["find_slot"]["call_lines"] == [73]
    assert one["node"]["ambiguous" if "ambiguous" in one["node"] else "name"] in (False, "kv_put")
    two = json.loads(m.expand_function("kv_put", levels=2))            # compact JSON, string rings
    assert [r["level"] for r in two["rings"]] == [1, 2]
    ring2 = two["rings"][1]["nodes"]
    assert any(n.startswith("hash_key kv.c:7 <- find_slot") for n in ring2)   # callee of find_slot
    assert any(n.startswith("kv_get kv.c:88 -> find_slot") for n in ring2)    # caller of find_slot
    assert two["rings"][1]["count"] == len(ring2)
    body = m.get_sliced_body("kv_get")
    assert body.count("*out_value = NULL;") == 1 and "if(idx < 0 || !s->entries[idx].in_use) {" in body
    assert body.count("{") == body.count("}")                         # every block is closed
    slot = m.get_sliced_body("find_slot").split("\n")
    assert slot[slot.index("   return -1;") - 1] == "   }"            # the loop closes before the return
    destroy = m.get_sliced_body("kv_destroy").split("\n")
    i = destroy.index("   for(i = 0; i < s->cap; i++)")
    assert destroy[i + 1].startswith("     if(") and destroy[i + 2].startswith("       free(")   # nested indentation
    put = m.get_sliced_body("kv_put").split("\n")
    i = put.index("   } else {")                                      # the else branch has its own header
    assert put[i - 1].strip() == "s->count++;" and put[i + 1].strip() == "free(e->value);"
    import re
    ctx = m.get_context_at("main.c", 23)                             # inside the "get" branch
    assert '   } else if(sscanf(line, "get %255s", key)== 1) {' in ctx    # chains stay on one line
    ctx = m.get_context_at("main.c", 17)                             # printf("error") in a brace-less else
    assert re.search(r"^\s+else$", ctx, re.M) and "} else" not in ctx    # brace-less else: no brace


# ---- friendly failures ------------------------------------------------------------------

@needs_gtags
def test_did_you_mean(taskrunner):
    from crossslice.cross.graph import RepoGraph
    from crossslice.cross.graph_server import GraphService
    with RepoGraph(str(taskrunner)) as g:
        g._ensure_gtags()
        assert "sched_submit" in g.gtags.suggest("sched_submt")
        assert "queue_push" in g.gtags.suggest("push")
        svc = GraphService(g)
        miss = svc.search("sched_submt")
        assert miss["hits"] == [] and "sched_submit" in miss["suggestions"]
        hit = svc.search("sched_submit")
        assert hit["hits"][0]["file"] == "src/sched.c" and hit["suggestions"] == []
        with pytest.raises(ValueError, match="Did you mean: .*sched_submit"):
            svc.expand("sched_submt")


def test_missing_global_is_one_clear_line(taskrunner, capsys, monkeypatch):
    from crossslice.cli import main
    from crossslice.cross.gtags_handler import GtagsHandler
    monkeypatch.setenv("PATH", str(taskrunner))                      # no gtags, no global, no git
    with pytest.raises(MissingTool, match="GNU Global"):
        GtagsHandler(str(taskrunner)).generate_gtags()
    assert main(["expand", "main", "-C", str(taskrunner)]) == 1
    err = capsys.readouterr().err
    assert "GNU Global is not installed" in err and "crossslice check" in err


# ---- cache lifetime ------------------------------------------------------------

@needs_gtags
def test_store_rebuilt_when_the_analysis_changes(taskrunner, tmp_path):
    """Summaries and slices are cached per node; a store built by an older
    analysis must not serve them after the analysis changed."""
    import sqlite3
    from crossslice.cross.graph import ANALYSIS_VERSION, RepoGraph
    db = tmp_path / "g.db"
    with RepoGraph(str(taskrunner), db_path=str(db)) as g:
        g.expand("sched_submit")
        assert sum(g.stats()["nodes"].values()) > 0
    c = sqlite3.connect(db)
    c.execute("UPDATE meta SET value='2000-01-01.0' WHERE key='analysis_version'")
    c.commit(); c.close()
    with RepoGraph(str(taskrunner), db_path=str(db)) as g:
        assert sum(g.stats()["nodes"].values()) == 0                   # rebuilt from scratch
        assert g.db.execute("SELECT value FROM meta WHERE key='analysis_version'").fetchone()[0] == ANALYSIS_VERSION
        g.expand("sched_submit")
        assert sum(g.stats()["nodes"].values()) > 0


@needs_gtags
def test_caller_nodes_carry_real_signatures(taskrunner):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner)) as g:
        g.expand("sched_submit")
        callers = {c["name"]: c for c in g.neighborhood("sched_submit")["callers"]}
    assert callers["main"]["signature"].startswith("int main(")          # not the bare name


@needs_gtags
def test_callees_deduped_with_every_call_site(taskrunner):
    """main submits two tasks: one callee entry, two call lines (was: two entries)."""
    from crossslice.cross import mcp_server as m
    m.SESSION, m.LOCK = m.Session(str(taskrunner), None), None
    try:
        r = json.loads(m.expand_function("main"))
        names = [c["name"] for c in r["callees"]]
        assert len(names) == len(set(names))
        assert {c["name"]: c["call_lines"] for c in r["callees"]}["sched_submit"] == [34, 35]
        res = json.loads(m.resolve_symbol("sched_submit"))
        assert res["ambiguous"] is False and res["signature"].startswith("int sched_submit(")
        assert not res["signature"].endswith("{")
        body = m.get_sliced_body("sched_submit")
        assert body.split("\n")[1].startswith("int sched_submit(sched_t *s, task_t *t) {")
    finally:
        m.SESSION.close()
        m.SESSION = None


def test_leading_global_options(taskrunner, capsys, monkeypatch):
    from crossslice.cli import main
    if shutil.which("gtags") is None:
        pytest.skip("GNU Global (gtags) not installed")
    assert main(["--cache-dir", str(taskrunner.parent / "c"), "-C", str(taskrunner), "expand", "sched_submit"]) == 0
    assert capsys.readouterr().out.startswith("sched_submit —")


@needs_gtags
def test_suggestions_without_two_letter_noise(taskrunner):
    from crossslice.cross.graph import RepoGraph
    with RepoGraph(str(taskrunner)) as g:
        g._ensure_gtags()
        for s in g.gtags.suggest("memcpy"):
            assert len(s) >= 3


@needs_gtags
def test_pointing_at_a_control_statement_seeds_its_branches(mcp_session):
    """get_context_at on an `if` line: both branches are in the slice, with the
    else header, not just the condition."""
    m = mcp_session
    ctx = m.get_context_at("kv.c", 77)                                # `if (!e->in_use) {` in kv_put
    sl = ctx[ctx.index("SLICE"):ctx.index("CALLEES")]
    assert ">" in sl and "memcpy(e->key, key, key_len + 1);" in sl
    assert "} else {" in sl and "free(e->value);" in sl
