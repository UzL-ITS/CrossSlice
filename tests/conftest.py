"""Shared test setup. The GumTree-based matching tests need GumTree 4.0.0-beta3:
set GUMTREE_PATH (or put `gumtree` on PATH). Without it they are skipped."""
import os
import shutil

from crossslice.paths import find_gumtree

GUMTREE_AVAILABLE = find_gumtree() is not None

import pytest


@pytest.fixture(autouse=True, scope="session")
def _isolated_cache(tmp_path_factory):
    """Keep the tests' graph stores and indexes out of the user's ~/.cache."""
    old = os.environ.get("CROSSSLICE_CACHE_DIR")
    os.environ["CROSSSLICE_CACHE_DIR"] = str(tmp_path_factory.mktemp("crossslice-cache"))
    yield
    if old is None:
        os.environ.pop("CROSSSLICE_CACHE_DIR", None)
    else:
        os.environ["CROSSSLICE_CACHE_DIR"] = old
