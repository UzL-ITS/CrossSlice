"""Test helpers: analyzer wrappers and a minimal replica of the gen_dataflow
matching pipeline (create_ast_json -> GumTree diff -> NodeMatcher ->
propagate_via_part_of -> run_through_stmts), as run by crossslice/intra/gen_dataflow.py.
"""
import copy
import os
from pathlib import Path

from crossslice.intra.general_code_analyzer import create_ast_json

FIXTURES = Path(__file__).resolve().parent / "fixtures"

_AST_CACHE = {}


def analyze(fixture_name, line=2):
    """Run the def/use engine on tests/fixtures/<fixture_name>.c and return a
    deep copy of the result (cached), so tests can freely mutate statements."""
    key = (fixture_name, line)
    if key not in _AST_CACHE:
        _AST_CACHE[key] = create_ast_json(str(FIXTURES / f"{fixture_name}.c"), line)
    return copy.deepcopy(_AST_CACHE[key])


def find_stmt(statements, expression):
    """Return the unique statement with the given (cleaned) expression."""
    hits = [s for s in statements if s.get("expression") == expression]
    assert len(hits) == 1, f"expected exactly one stmt {expression!r}, got {len(hits)}"
    return hits[0]


_SCALAR_TYPES = ("variable", "function_call")


def names(entries):
    """Names of the scalar entries (variables and callees), in order; the
    access-path entries the field-sensitive engine adds are listed by
    path_names()."""
    return [e["name"] for e in entries if e.get("id_type", "variable") in _SCALAR_TYPES]


def path_names(entries, parts=False):
    """Names of the access-path entries (`s->gb.x`, `len[]`); with parts=True
    also the part tokens (`s{*}`)."""
    kinds = ("access_path", "access_path_part") if parts else ("access_path",)
    return [e["name"] for e in entries if e.get("id_type") in kinds]


def analyze_function(fixture_name, function_name):
    """analyze() for the function called `function_name` in the fixture."""
    text = (FIXTURES / f"{fixture_name}.c").read_text()
    for i, line in enumerate(text.splitlines(), 1):
        if line.startswith(function_name + "(") or (" " + function_name + "(") in line and not line.startswith(" "):
            return analyze(fixture_name, i)
    raise AssertionError(f"no function {function_name} in {fixture_name}.c")


def var_ids(entries, name=None):
    return {e["var_id"] for e in entries if name is None or e["name"] == name}


def mark_changed(statements, expression, status="changed"):
    find_stmt(statements, expression)["change_status"] = status
    return statements


def relevant_exprs(statements):
    return {s.get("expression") for s in statements if s.get("relevant_to_dataflow")}


# ---------------------------------------------------------------------------
# Minimal end-to-end matching pipeline (mirrors crossslice/intra/gen_dataflow.py)
# ---------------------------------------------------------------------------
def run_matching(old_fixture, new_fixture, line=1):
    """Return (old_statements, new_statements) with change_status stamped, by
    running the same steps gen_dataflow.gen_dataflow runs for one function."""
    import shutil
    import pytest
    from crossslice.paths import find_gumtree
    _gt = find_gumtree()
    if not (_gt and os.path.exists(_gt)):
        pytest.skip("GumTree not available: unzip it into /opt/gumtree or set GUMTREE_PATH "
                    "(see scripts/setup_tools.sh)")
    from crossslice.intra.gumtree_handler import (
        create_gumtree_diff,
        map_changes_to_lines,
        map_matches_to_lines,
    )
    from crossslice.intra.matching import NodeMatcher
    from crossslice.intra.gen_dataflow import propagate_via_part_of
    from crossslice.intra.pre_merge import run_through_stmts

    old_path = str(FIXTURES / f"{old_fixture}.c")
    new_path = str(FIXTURES / f"{new_fixture}.c")
    old_ast = create_ast_json(old_path, line)
    new_ast = create_ast_json(new_path, line)
    with open(old_path) as f:
        old_code = f.read()
    with open(new_path) as f:
        new_code = f.read()

    gum_changes, gum_matches, offs_a, offs_b = create_gumtree_diff(
        old_path, new_path, old_code, new_code
    )
    assert gum_matches, "GumTree produced no matches - is GUMTREE_PATH correct?"
    changes_mapping = map_changes_to_lines(gum_changes, offs_a, offs_b, gum_matches)
    matches_mapping = map_matches_to_lines(gum_matches, offs_a, offs_b)

    # Identity line lookups covering the whole file (like __global_context__,
    # but for a single function that spans the file).
    def lookup(path, code, kind):
        n_lines = len(code.splitlines())
        return {
            i: {"initial_line": i, "file": path.lstrip("/"), "type": kind, "function": "f"}
            for i in range(n_lines + 1)
        }

    old_lookup = lookup(old_path, old_code, "old")
    new_lookup = lookup(new_path, new_code, "new")

    old_rel = os.path.relpath(old_path, "/")
    new_rel = os.path.relpath(new_path, "/")
    old_key, new_key = "old_ast", "new_ast"
    old_ast_mapping = {old_rel: [(0, max(old_lookup), old_key)]}
    new_ast_mapping = {new_rel: [(0, max(new_lookup), new_key)]}
    objs = {old_key: old_ast, new_key: new_ast}

    matcher = NodeMatcher(
        matches_mapping, changes_mapping, old_lookup, new_lookup,
        old_ast_mapping, new_ast_mapping, "/", "/", objs,
    )
    objs = matcher.match_stmts()

    old_stmts = run_through_stmts(propagate_via_part_of(objs[old_key]["statements"]))
    new_stmts = run_through_stmts(propagate_via_part_of(objs[new_key]["statements"]))
    return old_stmts, new_stmts
