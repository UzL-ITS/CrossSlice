"""Trailing macro tokens in an argument list (php-5.6 `TSRMLS_CC`) are not arguments."""
from tree_sitter import Language, Parser
import tree_sitter_c as tsc

from crossslice.intra.general_code_analyzer import is_valid_argument_node


def _args(src: bytes):
    tree = Parser(Language(tsc.language())).parse(src)
    found = []

    def walk(n):
        if n.type == "call_expression":
            al = n.child_by_field_name("arguments")
            found.append([a.text.decode() for a in al.named_children if is_valid_argument_node(a)])
        for c in n.children:
            walk(c)
    walk(tree.root_node)
    return found


def test_trailing_macro_token_is_not_an_argument():
    assert _args(b"int f(void) { return phar_free_alias(*fd_ptr, alias, alias_len TSRMLS_CC); }") == \
        [["*fd_ptr", "alias", "alias_len"]]


def test_ordinary_arguments_and_comments():
    assert _args(b"int f(void) { return g(a, /* c */ b, h(1, 2)); }") == [["a", "b", "h(1, 2)"], ["1", "2"]]


def test_calls_info_skips_error_children():
    # fixture tsrmls.c: php-5.6 style trailing TSRMLS_CC tokens
    from helpers import analyze, find_stmt
    stmts = analyze("tsrmls")["statements"]
    s = find_stmt(stmts, "int rc = phar_free_alias(*fd_ptr, alias, alias_len TSRMLS_CC);")
    call = [c for c in s["calls_info"] if c["function_name"] == "phar_free_alias"][0]
    assert [a["name"] for a in call["arguments"]] == ["*fd_ptr", "alias", "alias_len"]
    assert [a["arg_pos"] for a in call["arguments"]] == [0, 1, 2]
