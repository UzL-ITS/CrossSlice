"""Environment bootstrap for the eval scripts: read `.env` at the repository
root (KEY=VALUE lines; never overrides variables already set in the shell) and
default GUMTREE_PATH to the standard install location when it is unset."""

import os

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_GUMTREE_DEFAULT = "/opt/gumtree/gumtree-4.0.0-beta3/bin/gumtree"


def load():
    env_file = os.path.join(_ROOT, ".env")
    if os.path.exists(env_file):
        for line in open(env_file):
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k, v = k.strip(), v.strip().strip('"').strip("'")
            if k.startswith("export "):
                k = k[7:].strip()
            os.environ.setdefault(k, v)
    if "GUMTREE_PATH" not in os.environ and os.path.exists(_GUMTREE_DEFAULT):
        os.environ["GUMTREE_PATH"] = _GUMTREE_DEFAULT
    if not os.path.exists(os.environ.get("GUMTREE_PATH", "")):
        raise SystemExit(
            "GUMTREE_PATH is not set (or points nowhere). Export it, e.g.\n"
            f"  export GUMTREE_PATH={_GUMTREE_DEFAULT}\n"
            "or add that line to .env at the repository root.")


load()
