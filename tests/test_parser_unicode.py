"""Function/macro names must survive non-ASCII bytes earlier in the file
(tree-sitter offsets are byte offsets; the parser used to slice the decoded str)."""
from pathlib import Path

from crossslice.intra.ts_utils.source_code_parser_c import SourceCodeParserC

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def test_names_after_non_ascii_header():
    parser = SourceCodeParserC(str(FIXTURES / "unicode_header.c"))
    names = {name: (start, end) for _node, name, start, end in parser.collect_function_definitions()}
    assert "pick" in names, names
    assert "add_numbers" in names, names
    assert "SQUARE" in names, names
    assert names["add_numbers"] == (5, 5)
