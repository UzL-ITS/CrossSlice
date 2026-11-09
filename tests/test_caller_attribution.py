"""Callers whose enclosing function tree-sitter cannot name: macro-defined
headers (`PHP_METHOD(Phar, mount) { … }` is a top-level compound statement to
tree-sitter), functions wrapped into ERROR nodes by embedded-GLSL macros, and
a function merged with its neighbour by a parse error. `resolve.enclosing_header`
attributes them by the nearest column-0 header line, `create_ast_json_region`
slices them as a synthetic function with the file's line numbers."""
import shutil
import textwrap

import pytest

from crossslice.cross.resolve import enclosing_header, header_name
from crossslice.intra.general_code_analyzer import create_ast_json_region

needs_gtags = pytest.mark.skipif(shutil.which("gtags") is None, reason="GNU Global (gtags) not installed")

SRC = textwrap.dedent('''\
    #include "phar.h"

    int phar_split_fname(const char *s);

    /* {{{ proto Phar::mount() */
    PHP_METHOD(Phar, mount)
    {
    \tchar *fname = NULL;
    \tif (phar_split_fname(fname) == 0) {
    \t\tRETURN_TRUE;
    \t}
    \tphar_split_fname(fname);
    }
    /* }}} */

    static int helper(int x) /* {{{ */
    {
    \treturn phar_split_fname("x") + x;
    }

    PHP_FUNCTION(phar_is_file) /* {{{ */
    {
    \tphar_split_fname("y");
    }
    /* }}} */

    static const struct cb table[] = {
    \t{ "split", phar_split_fname },
    };

    int phar_split_fname(const char *s)
    {
    \treturn s[0];
    }
    ''')

# an unbalanced `{` inside a macro argument (FFmpeg's embedded GLSL) makes
# tree-sitter swallow the following function into the first one
GLSL = textwrap.dedent('''\
    static int init_gblur_pipeline(void)
    {
        GLSLC(0, layout(push_constant, std430) uniform pushConstants {   );
        GLSLC(0, };                                                       );
        return 0;
    }

    static int init_filter(void)
    {
        return ff_vk_shader_init(1);
    }

    int ff_vk_shader_init(int x)
    {
        return x;
    }
    ''')


def _line_of(text, needle):
    return next(i for i, l in enumerate(text.split("\n")) if needle in l)


def test_header_name_forms():
    assert header_name("PHP_METHOD(Phar, mount)") == "PHP_METHOD(Phar, mount)"
    assert header_name("PHP_METHOD(Phar,mount) /* {{{ */") == "PHP_METHOD(Phar, mount)"
    assert header_name("static PHP_FUNCTION(phar_is_file)") == "PHP_FUNCTION(phar_is_file)"
    assert header_name("ZEND_ATTRIBUTE_NONNULL_ARGS(1, 4) int phar_zip_flush(phar_archive_data *phar) /* {{{ */") == "phar_zip_flush"
    assert header_name("static av_cold int init_filter(AVFilterContext *avctx)") == "init_filter"
    assert header_name("SwsPass *ff_sws_graph_add_pass(SwsGraph *graph, enum AVPixelFormat fmt,") == "ff_sws_graph_add_pass"
    assert header_name("init_filter(AVFilterContext *avctx)") == "init_filter"       # return type on the line above
    assert header_name("static const AVOption opts[] = { OFFSET(x), 0 },") == ""
    assert header_name("if (x) {") == ""
    assert header_name("out: free(x);") == ""
    assert header_name("typedef int (*fn_t)(int);") == ""


def test_enclosing_header_macro_body_and_file_scope():
    lines = SRC.split("\n")
    at = lambda needle: _line_of(SRC, needle)
    assert enclosing_header(lines, at("== 0) {"))[1:] == ("PHP_METHOD(Phar, mount)", "PHP_METHOD(Phar, mount)")
    assert enclosing_header(lines, at("\tphar_split_fname(fname);"))[1] == "PHP_METHOD(Phar, mount)"
    _, name, head = enclosing_header(lines, at('return phar_split_fname("x")'))
    assert (name, head) == ("helper", "static int helper(int x)")
    assert enclosing_header(lines, at("int phar_split_fname(const char *s);")) is None    # prototype at file scope
    assert enclosing_header(lines, at('{ "split", phar_split_fname },')) is None           # initialiser at file scope
    assert enclosing_header(lines, at("return s[0];"))[1] == "phar_split_fname"


def test_region_slice_keeps_file_line_numbers(tmp_path):
    f = tmp_path / "phar_object.c"
    f.write_text(SRC)
    start = _line_of(SRC, "PHP_METHOD(Phar, mount)")
    data = create_ast_json_region(str(f), start)
    stmts = data["statements"]
    exprs = " | ".join(s.get("expression", "") for s in stmts)
    assert "phar_split_fname(fname)" in exprs and "RETURN_TRUE" in exprs
    rows = [s["start"][0] for s in stmts[1:]]
    assert rows and min(rows) > start and max(rows) <= _line_of(SRC, "/* }}} */")
    assert create_ast_json_region(str(f), _line_of(SRC, "int phar_split_fname(const char *s);")) is None


@needs_gtags
def test_graph_callers_in_macro_defined_and_merged_functions(tmp_path):
    from crossslice.cross.graph import RepoGraph
    repo = tmp_path / "repo"
    (repo / "ext").mkdir(parents=True)
    (repo / "ext" / "phar_object.c").write_text(SRC)
    (repo / "ext" / "phar.h").write_text("#define PHP_METHOD(c, m) void zim_##c##_##m(void)\n#define RETURN_TRUE return\n")
    (repo / "ext" / "vf_gblur_vulkan.c").write_text(GLSL)
    with RepoGraph(str(repo)) as g:
        g.expand("phar_split_fname", direction="up")
        callers = {c["name"]: c for c in g.neighborhood("phar_split_fname")["callers"]}
        g.expand("ff_vk_shader_init", direction="up")
        vk = {c["name"]: c for c in g.neighborhood("ff_vk_shader_init")["callers"]}
    assert set(callers) == {"PHP_METHOD(Phar, mount)", "helper", "PHP_FUNCTION(phar_is_file)"}   # not the prototype, not the table
    assert callers["PHP_METHOD(Phar, mount)"]["signature"] == "PHP_METHOD(Phar, mount)"
    assert len({c for c in callers["PHP_METHOD(Phar, mount)"].get("call_lines", [callers["PHP_METHOD(Phar, mount)"].get("call_line")])}) >= 1
    assert set(vk) == {"init_filter"}                                       # not init_gblur_pipeline (merged by the GLSL macro)
