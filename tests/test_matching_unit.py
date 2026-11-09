"""Unit tests for the parts of crossslice/intra/matching.py that decide
between several candidate matches. They do not need GumTree."""
from crossslice.intra.matching import NodeMatcher, Statement, find_most_specific_stmts


def _stmt(sid, start, end, typ="if_statement", expr="", match_id=None):
    s = {"id": sid, "type": typ, "expression": expr, "start": list(start), "end": list(end),
         "left_side": [], "right_side": [], "calls_info": [], "parts": [], "additional_info": []}
    if match_id:
        s["match_id"] = match_id
    return s


def _matcher(old, new):
    return NodeMatcher([], [], {}, {}, {}, {}, "/", "/",
                       {"old": {"statements": old}, "new": {"statements": new}})


def test_conflict_keeps_the_pair_gumtree_matched_as_whole_statements():
    outer = _stmt("outer", (2, 4), (6, 5), expr="if(a){ a = 0; if(g(s)== -1)return r; }", match_id="new")
    inner = _stmt("inner", (4, 8), (5, 21), expr="if(g(s)== -1)return r;", match_id="new")
    new_if = _stmt("new", (2, 4), (3, 17), expr="if(s && g(s)== -1)return r;", match_id="inner")
    m = _matcher([outer, inner], [new_if])
    # the inner if is the more similar expression, but GumTree matched the outer one as a node
    m.pair_evidence = {("outer", "new"): 2, ("new", "outer"): 2, ("inner", "new"): 0, ("new", "inner"): 0}
    m._postprocess_matches()
    assert new_if["match_id"] == "outer"
    assert outer["match_id"] == "new"
    assert inner["match_id"] is None


def test_conflict_without_evidence_prefers_similarity_then_source_order():
    for _ in range(5):  # the candidate set iterates in hash order; the choice must not
        a = _stmt("a", (1, 4), (1, 10), typ="expression_statement", expr="x = 1;", match_id="n")
        b = _stmt("b", (5, 4), (5, 10), typ="expression_statement", expr="x = 1;", match_id="n")
        n = _stmt("n", (1, 4), (1, 10), typ="expression_statement", expr="x = 1;", match_id="b")
        m = _matcher([a, b], [n])
        m._postprocess_matches()
        assert n["match_id"] == "a"  # equal similarity: the earliest statement
        assert b["match_id"] is None

        a = _stmt("a", (1, 4), (1, 10), typ="expression_statement", expr="x = 1;", match_id="n")
        b = _stmt("b", (5, 4), (5, 14), typ="expression_statement", expr="x = 1 + y;", match_id="n")
        n = _stmt("n", (1, 4), (1, 14), typ="expression_statement", expr="x = 1 + y;", match_id="a")
        m = _matcher([a, b], [n])
        m._postprocess_matches()
        assert n["match_id"] == "b"  # the more similar expression, although it comes later
        assert a["match_id"] is None


def test_match_evidence_scores_whole_statement_matches():
    s1 = Statement({"id": "s1", "start": [2, 4], "end": [6, 5]})
    s2 = Statement({"id": "s2", "start": [4, 8], "end": [5, 21]})
    d1 = Statement({"id": "d1", "start": [2, 4], "end": [3, 17]})
    m = _matcher([], [])
    m.statement_store["old"] = [s1, s2]
    m.statement_store["new"] = [d1]
    # the statements themselves
    m._note_match_evidence("old", ["s1"], (2, 4), (6, 5), "new", ["d1"], (2, 4), (3, 17))
    # a sub-expression inside s2 matched to one inside d1
    m._note_match_evidence("old", ["s2"], (4, 12), (4, 25), "new", ["d1"], (2, 13), (2, 26))
    assert m.pair_evidence[("s1", "d1")] == 2 and m.pair_evidence[("d1", "s1")] == 2
    assert m.pair_evidence[("s2", "d1")] == 0
    # a later, weaker match does not lower the score
    m._note_match_evidence("old", ["s1"], (2, 8), (2, 12), "new", ["d1"], (2, 8), (2, 12))
    assert m.pair_evidence[("s1", "d1")] == 2


def test_range_lookup_returns_statements_in_source_order():
    stmts = [Statement({"id": f"s{i}", "start": [i, 4], "end": [i, 10]}) for i in range(1, 6)]
    for _ in range(5):  # Statement objects hash by address: a set of them has no fixed order
        assert find_most_specific_stmts(stmts, (1, 4), (5, 10)) == ["s1", "s2", "s3", "s4", "s5"]
