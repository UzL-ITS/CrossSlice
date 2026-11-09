"""A name must map to ONE node however it is reached (resolved from a call site
with clangd, or looked up bare), and the caller list must report how many
reference sites exist. Reproduces the zlib `zmemcpy` case: a macro in the
header and a fallback function in a .c file share the name."""
import shutil
import textwrap

import pytest

from crossslice.cross.graph import RepoGraph

pytestmark = pytest.mark.skipif(shutil.which("gtags") is None, reason="GNU Global (gtags) not installed")


def _write(repo, rel, text):
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(textwrap.dedent(text))


@pytest.fixture
def repo(tmp_path):
    _write(tmp_path, "util.h", """
        #ifndef UTIL_H
        #define UTIL_H
        #include <string.h>
        #ifdef HAVE_MEMCPY
        #  define zcopy memcpy
        #else
        void zcopy(void *dst, const void *src, unsigned n);
        #endif
        #endif
        """)
    _write(tmp_path, "util.c", """
        #include "util.h"
        void zcopy(void *dst, const void *src, unsigned n) {
            unsigned i;
            char *d = dst;
            const char *s = src;
            for (i = 0; i < n; i++) d[i] = s[i];
        }
        """)
    _write(tmp_path, "a.c", """
        #include "util.h"
        int fa(char *out, const char *in) { zcopy(out, in, 4); return 0; }
        """)
    _write(tmp_path, "b.c", """
        #include "util.h"
        int fb(char *out, const char *in) { zcopy(out, in, 2); return 1; }
        int fc(char *out, const char *in) { zcopy(out, in, 8); zcopy(out + 8, in, 8); return 2; }
        """)
    return tmp_path


def _count(g, name):
    return g.db.execute("SELECT COUNT(*) FROM nodes WHERE name=?", (name,)).fetchone()[0]


def test_same_node_from_call_site_and_bare_name(repo):
    with RepoGraph(str(repo)) as g:
        assert g.expand("fa") is not None                      # reaches zcopy from a call site
        assert _count(g, "zcopy") == 1
        node_id = g.expand("zcopy")                             # bare-name expansion: no new node
        assert _count(g, "zcopy") == 1
        nb = g.neighborhood("zcopy")
        assert nb["node"]["id"] == node_id
        assert {c["name"] for c in nb["callers"]} == {"fa", "fb", "fc"}
        assert nb["node"]["callers_total"] >= 3                 # reference sites known
        assert nb["node"]["alternatives"], "macro vs. function: the other definition is recorded"
        # expanding by node id keeps identity too
        assert g.expand("zcopy", node_id=node_id) == node_id
        assert _count(g, "zcopy") == 1


def test_user_can_pick_the_other_definition(repo):
    with RepoGraph(str(repo)) as g:
        g.expand("fa")
        nb = g.neighborhood("zcopy")
        alt = nb["node"]["alternatives"][0]
        other = g.expand_definition("zcopy", alt["file"], alt["line"],
                                    "macro" if alt["is_macro"] else "function")
        assert other is not None and other != nb["node"]["id"]
        assert _count(g, "zcopy") == 2                          # explicit pick: a second node
