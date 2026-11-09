"""Tests for the statement-level def/use engine (crossslice/intra/general_code_analyzer.py)."""
from helpers import analyze, find_stmt, names, path_names, var_ids

from crossslice.intra.general_code_analyzer import ScopeManager


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
def test_parameters_registered():
    res = analyze("simple")
    assert [(p["name"], p["arg_pos"]) for p in res["parameters"]] == [("a", 0), ("b", 1)]

    fn_def = res["statements"][0]
    assert fn_def["type"] == "function_definition"
    params = {p["name"]: p["var_id"] for p in fn_def["parameters"]}
    assert set(params) == {"a", "b"}

    # a use of parameter `a` in the body resolves to the same var_id
    decl = find_stmt(res["statements"], "int x = a + 1;")
    assert var_ids(decl["right_side"], "a") == {params["a"]}


# ---------------------------------------------------------------------------
# Simple assignment / compound assignment / declaration
# ---------------------------------------------------------------------------
def test_simple_assignment_lhs_def_rhs_use():
    stmts = analyze("simple")["statements"]
    s = find_stmt(stmts, "x = b;")
    assert names(s["left_side"]) == ["x"]
    assert names(s["right_side"]) == ["b"]


def test_compound_assignment_is_def_and_use():
    stmts = analyze("simple")["statements"]
    s = find_stmt(stmts, "x += a;")
    assert names(s["left_side"]) == ["x"]
    assert sorted(names(s["right_side"])) == ["a", "x"]
    # def and use of x refer to the same variable
    assert var_ids(s["left_side"], "x") == var_ids(s["right_side"], "x")


def test_declaration_with_initializer():
    stmts = analyze("simple")["statements"]
    s = find_stmt(stmts, "int x = a + 1;")
    assert names(s["left_side"]) == ["x"]
    assert names(s["right_side"]) == ["a"]


def test_var_id_stable_across_statements():
    stmts = analyze("simple")["statements"]
    x_ids = set()
    for expr in ["int x = a + 1;", "x = b;", "x += a;"]:
        x_ids |= var_ids(find_stmt(stmts, expr)["left_side"], "x")
    x_ids |= var_ids(find_stmt(stmts, "return x;")["right_side"], "x")
    assert len(x_ids) == 1


def test_return_statement_children_are_uses():
    stmts = analyze("simple")["statements"]
    s = find_stmt(stmts, "return x;")
    assert s["left_side"] == []
    assert names(s["right_side"]) == ["x"]


# ---------------------------------------------------------------------------
# Calls
# ---------------------------------------------------------------------------
def test_call_records_callee_and_args_as_uses():
    stmts = analyze("calls")["statements"]
    s = find_stmt(stmts, "y = compute(a, 5);")
    assert names(s["left_side"]) == ["y"]

    by_name = {e["name"]: e for e in s["right_side"] if e["id_type"] != "access_path_part"}
    assert set(by_name) == {"compute", "a"}
    assert by_name["compute"]["id_type"] == "function_call"
    assert by_name["a"]["id_type"] == "variable"


def test_calls_info_structure():
    stmts = analyze("calls")["statements"]
    s = find_stmt(stmts, "y = compute(a, 5);")
    assert len(s["calls_info"]) == 1
    call = s["calls_info"][0]
    assert call["function_name"] == "compute"
    assert [(a["name"], a["arg_pos"]) for a in call["arguments"]] == [("a", 0), ("5", 1)]


def test_input_function_writes_its_buffer_argument():
    # fgets writes through its first argument: the buffer's contents (`buf[]`)
    # are defined, the pointer and the other arguments are read. (The scalar
    # engine defined every identifier argument of scanf/fgets/gets instead.)
    stmts = analyze("calls")["statements"]
    s = find_stmt(stmts, "fgets(buf, n, stdin);")
    assert names(s["left_side"]) == []
    assert path_names(s["left_side"]) == ["buf[]"]
    assert sorted(names(s["right_side"])) == ["buf", "fgets", "n", "stdin"]
    assert s["right_side"][0]["id_type"] == "function_call"


def test_scanf_address_of_arg_is_a_def():
    # scanf("%d", &a) writes a: the field-sensitive engine records a plain
    # definition of `a` (the scalar engine demoted it to a use).
    stmts = analyze("calls")["statements"]
    s = find_stmt(stmts, 'scanf("%d", &a);')
    assert names(s["left_side"]) == ["a"]
    assert s["left_side"][0]["id_type"] == "variable"
    assert names(s["right_side"]) == ["scanf"]
    call = s["calls_info"][0]
    assert call["function_name"] == "scanf"
    assert [(a["name"], a["arg_pos"]) for a in call["arguments"]] == [('"%d"', 0), ("&a", 1)]


# ---------------------------------------------------------------------------
# Pointer / field access on the LHS
# ---------------------------------------------------------------------------
def test_field_write_base_identifier_is_use_not_def():
    # The base pointer of a field write is read, not defined; what is defined
    # is the access path `s->field` (see test_access_paths.py).
    stmts = analyze("fields")["statements"]
    s = find_stmt(stmts, "s->field = x;")
    assert names(s["left_side"]) == []
    assert path_names(s["left_side"]) == ["s->field"]
    assert sorted(names(s["right_side"])) == ["s", "x"]


def test_pointer_deref_write_base_is_use():
    stmts = analyze("fields")["statements"]
    s = find_stmt(stmts, "*s->arr = x;")
    assert names(s["left_side"]) == []
    assert path_names(s["left_side"]) == ["s->arr[]"]
    assert sorted(names(s["right_side"])) == ["s", "x"]


# ---------------------------------------------------------------------------
# Shadowing
# ---------------------------------------------------------------------------
def test_shadowed_variable_gets_distinct_var_id():
    stmts = analyze("shadow")["statements"]
    outer_id = var_ids(find_stmt(stmts, "int x = 1;")["left_side"], "x")
    inner_id = var_ids(find_stmt(stmts, "int x = 2;")["left_side"], "x")
    assert outer_id != inner_id

    # statement inside the block writes the inner x
    assert var_ids(find_stmt(stmts, "x = a;")["left_side"], "x") == inner_id
    # statement after the block writes the outer x
    assert var_ids(find_stmt(stmts, "x = 3;")["left_side"], "x") == outer_id
    assert var_ids(find_stmt(stmts, "return x;")["right_side"], "x") == outer_id


def test_resolve_any_prefers_innermost_scope():
    # Regression test: resolve_any used to index scopes_by_node_id (keyed by
    # AST node id) with a scope_id, which broke the depth preference.
    sm = ScopeManager()
    sm.enter_scope(100)
    outer = sm.declare("t", 1)
    sm.enter_scope(200)
    inner = sm.declare("t", 2)
    sm.exit_scope()
    sm.exit_scope()

    resolved = sm.resolve_any("t")
    assert resolved.id == inner.id
    assert resolved.id != outer.id


# ---------------------------------------------------------------------------
# Control-flow decomposition into parts
# ---------------------------------------------------------------------------
def test_if_statement_parts_and_part_of_links():
    stmts = analyze("control_flow")["statements"]
    if_stmt = next(s for s in stmts if s["type"] == "if_statement")

    # statement-level def/use of the if only covers the condition
    assert if_stmt["left_side"] == []
    assert sorted(names(if_stmt["right_side"])) == ["a", "b"]

    parts = {p["part_nname"]: p for p in if_stmt["parts"]}
    assert set(parts) == {"condition", "consequence", "alternative"}

    cond = parts["condition"]
    assert sorted(names(cond["right_side"])) == ["a", "b"]
    assert cond["left_side"] == []
    assert cond["statement_ids"] == []

    then_stmt = find_stmt(stmts, "r = a;")
    else_stmt = find_stmt(stmts, "r = b;")
    assert parts["consequence"]["statement_ids"] == [then_stmt["id"]]
    assert parts["alternative"]["statement_ids"] == [else_stmt["id"]]

    # per-part def/use of the consequence body
    assert names(parts["consequence"]["left_side"]) == ["r"]
    assert names(parts["consequence"]["right_side"]) == ["a"]

    # inner statements carry the reciprocal part_of link
    assert {"part_of": parts["consequence"]["id"]} in then_stmt["additional_info"]
    assert {"part_of": parts["alternative"]["id"]} in else_stmt["additional_info"]


def test_for_statement_parts_and_loop_variable():
    stmts = analyze("for_loop")["statements"]
    for_stmt = next(s for s in stmts if s["type"] == "for_statement")
    parts = {p["part_nname"]: p for p in for_stmt["parts"]}
    assert set(parts) == {"initializer", "condition", "update", "body"}

    # initializer declares i (def), condition uses i and n, update i++ is def+use
    assert names(parts["initializer"]["left_side"]) == ["i"]
    assert sorted(names(parts["condition"]["right_side"])) == ["i", "n"]
    assert names(parts["update"]["left_side"]) == ["i"]
    assert names(parts["update"]["right_side"]) == ["i"]

    # the loop variable is one and the same variable everywhere
    i_ids = (
        var_ids(parts["initializer"]["left_side"], "i")
        | var_ids(parts["condition"]["right_side"], "i")
        | var_ids(parts["update"]["left_side"], "i")
    )
    body_stmt = find_stmt(stmts, "sum = sum + i;")
    i_ids |= var_ids(body_stmt["right_side"], "i")
    assert len(i_ids) == 1

    # body statement is attached to the body part
    assert parts["body"]["statement_ids"] == [body_stmt["id"]]
    assert {"part_of": parts["body"]["id"]} in body_stmt["additional_info"]


def test_while_statement_parts():
    stmts = analyze("control_flow")["statements"]
    while_stmt = next(s for s in stmts if s["type"] == "while_statement")
    assert names(while_stmt["right_side"]) == ["r"]

    parts = {p["part_nname"]: p for p in while_stmt["parts"]}
    assert set(parts) == {"condition", "body"}

    body_stmt = find_stmt(stmts, "r = r - 1;")
    assert parts["body"]["statement_ids"] == [body_stmt["id"]]
    assert {"part_of": parts["body"]["id"]} in body_stmt["additional_info"]

    # condition/body var resolution uses the same variable as the outer decl
    decl_r = var_ids(find_stmt(stmts, "int r = 0;")["left_side"], "r")
    assert var_ids(parts["condition"]["right_side"], "r") == decl_r
    assert var_ids(while_stmt["right_side"], "r") == decl_r
