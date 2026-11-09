"""Tests for crossslice/intra/relevant_dataflow.find_relevant_dataflow on statements
produced by the real engine, with change_status stamped manually."""
from helpers import analyze, find_stmt, mark_changed, relevant_exprs

from crossslice.intra.relevant_dataflow import find_relevant_dataflow


def test_level1_only_changed_statements_relevant():
    stmts = analyze("slicer_levels")["statements"]
    mark_changed(stmts, "int r = y + y;")
    find_relevant_dataflow(stmts, level=1)
    assert relevant_exprs(stmts) == {"int r = y + y;"}


def test_level2_backward_and_forward_slice():
    stmts = analyze("slicer_levels")["statements"]
    mark_changed(stmts, "int r = y + y;")
    find_relevant_dataflow(stmts, level=2)
    # One slicing round. NOTE: a single backward pass is transitive along
    # source order (the needed-set grows while scanning back), so both
    # `int y = x;` AND `int x = a;` are pulled in at level 2.
    assert relevant_exprs(stmts) == {"int r = y + y;", "int y = x;", "int x = a;"}
    # `int p = x;` is only reachable by slicing forward from a statement that
    # was itself discovered backward -> needs another round (level "all").
    assert not find_stmt(stmts, "int p = x;")["relevant_to_dataflow"]


def test_level_all_reaches_fixpoint():
    stmts = analyze("slicer_levels")["statements"]
    mark_changed(stmts, "int r = y + y;")
    find_relevant_dataflow(stmts, level="all")
    assert relevant_exprs(stmts) == {
        "int r = y + y;",
        "int y = x;",
        "int x = a;",
        "int p = x;",
    }


def test_unchanged_function_has_no_relevant_statements():
    stmts = analyze("slicer_levels")["statements"]
    find_relevant_dataflow(stmts, level="all")
    assert relevant_exprs(stmts) == set()


def test_control_flow_parent_becomes_relevant():
    stmts = analyze("control_flow")["statements"]
    mark_changed(stmts, "r = a;")
    find_relevant_dataflow(stmts, level=1)

    if_stmt = next(s for s in stmts if s["type"] == "if_statement")
    assert if_stmt["relevant_to_dataflow"], (
        "if-statement must become relevant when a statement in its body is"
    )
    # ... but the propagation must not leak to unrelated siblings/children
    assert not find_stmt(stmts, "r = b;")["relevant_to_dataflow"]
    while_stmt = next(s for s in stmts if s["type"] == "while_statement")
    assert not while_stmt["relevant_to_dataflow"]
    assert not find_stmt(stmts, "return r;")["relevant_to_dataflow"]


def test_nested_control_flow_propagation_is_transitive():
    stmts = analyze("nested_cf")["statements"]
    mark_changed(stmts, "s = s + a;")
    find_relevant_dataflow(stmts, level=1)

    if_stmt = next(s for s in stmts if s["type"] == "if_statement")
    while_stmt = next(s for s in stmts if s["type"] == "while_statement")
    assert if_stmt["relevant_to_dataflow"]
    assert while_stmt["relevant_to_dataflow"], "propagation must climb through nested levels"
    # siblings inside the while body stay irrelevant
    assert not find_stmt(stmts, "n = n - 1;")["relevant_to_dataflow"]
    assert not find_stmt(stmts, "int s = 0;")["relevant_to_dataflow"]
    assert not find_stmt(stmts, "return s;")["relevant_to_dataflow"]


def test_matched_statements_are_not_seeds():
    stmts = analyze("slicer_levels")["statements"]
    for s in stmts:
        s["change_status"] = "matched"
    find_relevant_dataflow(stmts, level="all")
    assert relevant_exprs(stmts) == set()


def test_scope_awareness_sibling_scopes_not_conflated():
    stmts = analyze("slicer_scope")["statements"]
    mark_changed(stmts, "a = t;")
    find_relevant_dataflow(stmts, level=2)

    # the `t` defined in the FIRST block flows into the seed
    assert find_stmt(stmts, "int t = a;")["relevant_to_dataflow"]
    # the same-named `t` in the sibling block must NOT be pulled in
    assert not find_stmt(stmts, "int t = 5;")["relevant_to_dataflow"]
    assert not find_stmt(stmts, "int u = t;")["relevant_to_dataflow"]
