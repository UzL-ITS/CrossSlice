# kvstore @ 353554d523f6

Repository: kvstore
Commit: `353554d523f64f166407451b12309609efb00946`
Parent: `b4b2e72b0752a152acc6615ba1c912f5915c0cd7`

Commit message:

```
kv_put: reject oversized keys instead of overflowing the entry buffer

kv_put copied the caller-supplied key into the fixed-size
kv_entry.key buffer with strcpy. Any key of KV_MAX_KEY_LEN or more
bytes (the CLI accepts up to 255) overflowed the entry and corrupted
the neighbouring slots of the table.

Validate the length up front, return the new KV_ERR_KEYLEN error,
and use an exact-size memcpy for the copy.
```

## Context size comparison

| representation | characters | vs full functions |
|---|---:|---:|
| raw git diff (-U3) | 965 | 0.44x |
| full changed functions (old+new) | 2,190 | 1.00x |
| intra-procedural enriched | 1,725 | 0.79x |
| + cross-function ring 1 | 3,108 | 1.42x |
| + ring 2 summaries | 3,256 | 1.49x |

## Cascade statistics

```json
{
  "old": {
    "gtags_unique": 3,
    "gtags+ts": 0,
    "lsp": 0,
    "priority_fallback": 0,
    "unresolved": 0,
    "stdlib_skipped": 2
  },
  "new": {
    "gtags_unique": 6,
    "gtags+ts": 0,
    "lsp": 0,
    "priority_fallback": 0,
    "unresolved": 0,
    "stdlib_skipped": 3
  }
}
```

Files: `raw_diff_u3.txt`, `enriched_intra.txt`, `enriched_inter1.txt`, `enriched_inter2.txt`.
