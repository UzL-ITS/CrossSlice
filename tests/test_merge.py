"""Tests for crossslice/intra/merge.merge_statements using synthetic statements shaped
like the analyzer/matcher output."""
from crossslice.intra.merge import merge_statements


def mk(sid, expr, line, typ="expression_statement", scope_level=0,
       match_id=None, change_status=None):
    s = {
        "id": sid,
        "type": typ,
        "expression": expr,
        "start": [line, 4],
        "end": [line, 4 + len(expr)],
        "scope_id": 1,
        "scope_depth": 1,
        "scope_level": scope_level,
        "left_side": [],
        "right_side": [],
        "calls_info": [],
        "parts": [],
        "additional_info": [],
    }
    if match_id is not None:
        s["match_id"] = match_id
    if change_status is not None:
        s["change_status"] = change_status
    return s


def pair(old_sid, new_sid, old_expr, new_expr, old_line, new_line, status="matched",
         old_scope=0, new_scope=0):
    old = mk(old_sid, old_expr, old_line, match_id=new_sid, change_status=status,
             scope_level=old_scope)
    new = mk(new_sid, new_expr, new_line, match_id=old_sid, change_status=status,
             scope_level=new_scope)
    return old, new


def exprs_and_statuses(merged):
    return [(s["expression"], s.get("change_status")) for s in merged]


def test_matched_pair_emission():
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 1;", 1, 1)
    merged, _ = merge_statements([a_old], [a_new])
    assert len(merged) == 1
    assert merged[0]["id"] == "nA"
    assert merged[0]["change_status"] == "matched"


def test_changed_pair_keeps_old_and_new_expressions():
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 2;", 1, 1)
    merged, _ = merge_statements([a_old], [a_new])
    assert len(merged) == 1
    m = merged[0]
    assert m["change_status"] == "changed"
    assert m["old_expression"] == "a = 1;"
    assert m["new_expression"] == "a = 2;"
    assert m["old_statement"]["id"] == "oA"
    assert m["new_statement"]["id"] == "nA"


def test_inserted_statement_placed_in_new_order():
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 1;", 1, 1)
    b_old, b_new = pair("oB", "nB", "b = 2;", "b = 2;", 2, 3)
    d_new = mk("nD", "d = 9;", 2)  # new-only, between A and B in the new file

    merged, _ = merge_statements([a_old, b_old], [a_new, d_new, b_new])
    assert exprs_and_statuses(merged) == [
        ("a = 1;", "matched"),
        ("d = 9;", "inserted"),
        ("b = 2;", "matched"),
    ]


def test_deleted_statement_placed_near_old_neighbors():
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 1;", 1, 1)
    b_old, b_new = pair("oB", "nB", "b = 2;", "b = 2;", 3, 2)
    x_old = mk("oX", "x = 5;", 2)  # old-only, between A and B in the old file

    merged, _ = merge_statements([a_old, x_old, b_old], [a_new, b_new])
    assert exprs_and_statuses(merged) == [
        ("a = 1;", "matched"),
        ("x = 5;", "deleted"),
        ("b = 2;", "matched"),
    ]


def test_moved_statement_emits_ghost_at_old_position():
    # old order: A, M, B  --  new order: A, B, M (M moved to the end).
    # The matcher stamps 'moved' + match ids on both sides of the moved pair.
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 1;", 1, 1)
    m_old, m_new = pair("oM", "nM", "m = 7;", "m = 7;", 2, 3, status="moved")
    b_old, b_new = pair("oB", "nB", "b = 2;", "b = 2;", 3, 2)

    merged, _ = merge_statements([a_old, m_old, b_old], [a_new, b_new, m_new])

    assert exprs_and_statuses(merged) == [
        ("a = 1;", "matched"),
        ("m = 7;", "moved_from"),   # ghost at the OLD position
        ("b = 2;", "matched"),
        ("m = 7;", "moved"),        # actual statement at the NEW position
    ]

    ghost = merged[1]
    assert ghost["id"] == "ghost_oM"
    assert ghost["is_ghost_deleted"] is True
    assert "match_id" not in ghost

    moved = merged[3]
    assert moved["id"] == "nM"
    assert moved["old_statement"]["id"] == "oM"
    assert moved["new_statement"]["id"] == "nM"


def test_scope_level_change_detected_as_move():
    # Matched pair with identical expression but different scope_level is
    # treated as moved by detect_order_changes (needs >= 2 match pairs).
    a_old, a_new = pair("oA", "nA", "a = 1;", "a = 1;", 1, 1)
    m_old, m_new = pair("oM", "nM", "m = 7;", "m = 7;", 2, 3,
                        old_scope=0, new_scope=1)

    merged, _ = merge_statements([a_old, m_old], [a_new, m_new])
    by_id = {s["id"]: s for s in merged}
    assert by_id["nM"]["change_status"] == "moved"
    assert "ghost_oM" in by_id
    assert by_id["ghost_oM"]["change_status"] == "moved_from"


def test_empty_old_side_marks_everything_inserted():
    n = mk("n1", "a = 1;", 1)
    merged, _ = merge_statements([], [n])
    assert merged[0]["change_status"] == "inserted"
    assert merged[0]["relevant_to_dataflow"] is True


def test_empty_new_side_marks_everything_deleted():
    o = mk("o1", "a = 1;", 1)
    merged, _ = merge_statements([o], [])
    assert merged[0]["change_status"] == "deleted"
    assert merged[0]["relevant_to_dataflow"] is True


def test_unmatched_statements_take_the_status_of_their_side():
    # GumTree marked both as changed, but the matcher dropped the pair (or never
    # made one): the old statement is old code and the new one is new code.
    old = mk("oA", "if (a) { b(); }", 1, typ="if_statement", change_status="changed")
    new = mk("nA", "if (a && b()) c();", 1, typ="if_statement", change_status="changed")
    merged, _ = merge_statements([old], [new])
    assert sorted(exprs_and_statuses(merged)) == [("if (a && b()) c();", "inserted"),
                                                  ("if (a) { b(); }", "deleted")]

    old = mk("oB", "x = 1;", 2, change_status="moved")
    new = mk("nB", "x = 2;", 2, change_status="moved")
    merged, _ = merge_statements([old], [new])
    assert sorted(exprs_and_statuses(merged)) == [("x = 1;", "deleted"), ("x = 2;", "inserted")]
