"""Tests for crossslice/intra/pre_merge.run_through_stmts on real analyzer output."""
from helpers import analyze, find_stmt, mark_changed

from crossslice.intra.pre_merge import run_through_stmts


def get_info(stmt, key):
    for info in stmt.get("additional_info", []):
        if isinstance(info, dict) and info.get("info") == key:
            return info
    return None


def test_contained_statements_recorded():
    stmts = analyze("control_flow")["statements"]
    out = run_through_stmts(stmts)

    if_stmt = next(s for s in out if s["type"] == "if_statement")
    contained = get_info(if_stmt, "contained_statements")
    then_id = find_stmt(out, "r = a;")["id"]
    else_id = find_stmt(out, "r = b;")["id"]
    assert contained is not None
    assert set(contained["stmt_ids"]) == {then_id, else_id}


def test_inner_change_reports_containing_part():
    # Regression test: find_containing_part used to look up the part name under
    # 'part_name' while the analyzer emits 'part_nname', so in_part was always None.
    stmts = analyze("control_flow")["statements"]
    mark_changed(stmts, "r = a;")
    out = run_through_stmts(stmts)

    if_stmt = next(s for s in out if s["type"] == "if_statement")
    inner = get_info(if_stmt, "inner_changes")
    assert inner is not None
    changes = {c["expression"]: c for c in inner["changes"]}
    assert set(changes) == {"r = a;"}
    assert changes["r = a;"]["change_type"] == "changed"
    assert changes["r = a;"]["in_part"] == "consequence"


def test_control_flow_statement_does_not_inherit_inner_status():
    stmts = analyze("control_flow")["statements"]
    mark_changed(stmts, "r = a;")
    out = run_through_stmts(stmts)
    if_stmt = next(s for s in out if s["type"] == "if_statement")
    # control-flow nodes must not have their own change_status bumped
    assert if_stmt.get("change_status") is None
