#!/usr/bin/env bash
# Build examples/kvstore-evolution/kvstore: a git repository with two commits.
#
#   HEAD~1  "kvstore: initial implementation"    <- contains a buffer overflow
#   HEAD    "kv_put: reject oversized keys ..."  <- the security fix
#
# Run the enrichment pipeline on the fix commit afterwards, e.g.:
#   uv run python -m eval.make_example examples/kvstore-evolution/kvstore HEAD
set -euo pipefail
cd "$(dirname "$0")"

rm -rf kvstore
mkdir kvstore
git -C kvstore init -q -b main
git -C kvstore config user.name "Example Author"
git -C kvstore config user.email "author@example.com"

cp old/* kvstore/
git -C kvstore add -A
git -C kvstore commit -q -m "kvstore: initial implementation

A small open-addressing hash map with a line-based CLI.
Keys live in fixed-size buffers inside the entry table."

cp new/* kvstore/
git -C kvstore add -A
git -C kvstore commit -q -m "kv_put: reject oversized keys instead of overflowing the entry buffer

kv_put copied the caller-supplied key into the fixed-size
kv_entry.key buffer with strcpy. Any key of KV_MAX_KEY_LEN or more
bytes (the CLI accepts up to 255) overflowed the entry and corrupted
the neighbouring slots of the table.

Validate the length up front, return the new KV_ERR_KEYLEN error,
and use an exact-size memcpy for the copy."

echo "kvstore/ created:"
git -C kvstore log --oneline
