"""End-to-end GumTree matching tests (need a working GumTree binary at
GUMTREE_PATH). The pipeline replicated here mirrors crossslice/intra/gen_dataflow.py:
create_ast_json -> gumtree textdiff -> NodeMatcher.match_stmts ->
propagate_via_part_of -> run_through_stmts (see helpers.run_matching)."""
import os

import pytest

from helpers import find_stmt, run_matching

from crossslice.paths import find_gumtree

GUMTREE = find_gumtree() or ""
pytestmark = pytest.mark.skipif(
    not os.path.exists(GUMTREE), reason=f"GumTree binary not found at {GUMTREE!r}"
)


def statuses(stmts):
    return {s.get("expression"): s.get("change_status") for s in stmts}


def test_insert_marks_new_statement_inserted():
    old, new = run_matching("pair_insert_old", "pair_insert_new")

    inserted = find_stmt(new, "x = x + 1;")
    assert inserted["change_status"] == "inserted"
    assert not inserted.get("match_id")

    # unchanged statements are matched, with reciprocal match ids
    old_decl = find_stmt(old, "int x = a;")
    new_decl = find_stmt(new, "int x = a;")
    assert old_decl["change_status"] == "matched"
    assert new_decl["change_status"] == "matched"
    assert old_decl["match_id"] == new_decl["id"]
    assert new_decl["match_id"] == old_decl["id"]

    assert find_stmt(old, "return x;")["change_status"] == "matched"
    assert find_stmt(new, "return x;")["change_status"] == "matched"
    # nothing in the old version is deleted/changed
    assert set(statuses(old).values()) == {"matched"}


def test_delete_marks_old_statement_deleted():
    # reverse direction of the insert pair
    old, new = run_matching("pair_insert_new", "pair_insert_old")

    deleted = find_stmt(old, "x = x + 1;")
    assert deleted["change_status"] == "deleted"
    assert not deleted.get("match_id")

    assert find_stmt(old, "int x = a;")["change_status"] == "matched"
    assert find_stmt(new, "int x = a;")["change_status"] == "matched"
    assert set(statuses(new).values()) == {"matched"}


def test_modify_resolves_to_changed_after_merge():
    from crossslice.intra.merge import merge_statements

    old, new = run_matching("pair_modify_old", "pair_modify_new")

    # the modified declarations are matched to each other
    old_decl = find_stmt(old, "int x = a;")
    new_decl = find_stmt(new, "int x = a + 42;")
    assert old_decl["match_id"] == new_decl["id"]

    merged, _ = merge_statements(old, new)
    changed = find_stmt(merged, "int x = a + 42;")
    assert changed["change_status"] == "changed"
    assert changed["old_expression"] == "int x = a;"
    assert changed["new_expression"] == "int x = a + 42;"

    # the untouched statements survive as matched
    assert find_stmt(merged, "int y = b;")["change_status"] == "matched"
    assert find_stmt(merged, "return x + y;")["change_status"] == "matched"


def test_move_marks_statements_moved_on_both_sides():
    old, new = run_matching("pair_move_old", "pair_move_new")

    for stmts in (old, new):
        assert find_stmt(stmts, "int x = a;")["change_status"] == "moved"
        assert find_stmt(stmts, "use(x);")["change_status"] == "moved"
        assert find_stmt(stmts, "int y = b;")["change_status"] == "matched"
        assert find_stmt(stmts, "use(y);")["change_status"] == "matched"

    # reciprocal match ids for a moved pair
    assert find_stmt(old, "use(x);")["match_id"] == find_stmt(new, "use(x);")["id"]
    assert find_stmt(new, "use(x);")["match_id"] == find_stmt(old, "use(x);")["id"]


def test_move_produces_ghosts_in_merge():
    from crossslice.intra.merge import merge_statements

    old, new = run_matching("pair_move_old", "pair_move_new")
    merged, _ = merge_statements(old, new)

    by_status = {}
    for s in merged:
        by_status.setdefault(s.get("change_status"), []).append(s)

    ghosts = by_status.get("moved_from", [])
    moved = by_status.get("moved", [])
    assert {g["expression"] for g in ghosts} == {"int x = a;", "use(x);"}
    assert {m["expression"] for m in moved} == {"int x = a;", "use(x);"}
    assert all(g["id"].startswith("ghost_") for g in ghosts)

    # ghost of use(x) sits at its OLD position: after `int y = b;`,
    # before `use(y);`; the moved statement itself is at the NEW position (end)
    order = [s["expression"] for s in merged]
    ghost_use_idx = next(
        i for i, s in enumerate(merged)
        if s["expression"] == "use(x);" and s.get("change_status") == "moved_from"
    )
    assert order.index("int y = b;") < ghost_use_idx < order.index("use(y);")
    moved_use_idx = next(
        i for i, s in enumerate(merged)
        if s["expression"] == "use(x);" and s.get("change_status") == "moved"
    )
    assert moved_use_idx > order.index("use(y);")


def test_collapsed_block_keeps_the_statement_gumtree_matched_as_a_whole():
    """zlib a4e4521e: `if (a) { a = 0; if (g() == -1) return r; }` becomes
    `if (b && g() == -1) return r;`. GumTree maps the outer if to the new if
    and deletes the inner one, but sub-expression matches tie the inner if to
    the new if as well. The matcher used to pick the survivor from a set of
    uuids (so the result changed from run to run); it keeps the pair GumTree
    matched as whole statements. The unmatched old inner if is old code: the
    merge reports it deleted, not "changed" (which the formatter prints as new)."""
    from crossslice.intra.merge import merge_statements

    for _ in range(3):  # fresh uuids each time: the candidates come in another order
        old, new = run_matching("pair_collapse_old", "pair_collapse_new")
        outer = find_stmt(old, "if(state->seek){ state->seek = 0; "
                               "if(gz_zero(state, state->skip)== -1)return state->err; }")
        inner = find_stmt(old, "if(gz_zero(state, state->skip)== -1)return state->err;")
        new_if = find_stmt(new, "if(state->skip && gz_zero(state)== -1)return state->err;")
        assert new_if["match_id"] == outer["id"]
        assert outer["match_id"] == new_if["id"]
        assert not inner.get("match_id")

        merged, _ = merge_statements(old, new)
        status = {s["expression"]: s["change_status"] for s in merged}
        assert status[new_if["expression"]] == "changed"
        assert status[inner["expression"]] == "deleted"
        assert status["state->seek = 0;"] == "deleted"
