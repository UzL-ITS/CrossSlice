# Example projects

Two small C projects for trying CrossSlice. Both build with `make` and run.

| project | content | used for |
|---|---|---|
| `taskrunner/` | a small priority task scheduler with retry | code context: `expand`, `context`, the explorer, the MCP server |
| `kvstore-evolution/` | a hash-map key-value store as a git repository with two commits, a buffer overflow and its fix | commit context and analysis of past revisions |

The commands below run from the CrossSlice checkout. `-C DIR` names the
example to analyze. The commit pipeline needs GumTree; `crossslice check`
verifies the setup.

## taskrunner

`taskrunner/` is not a git repository, so it is named with `-C`.

```bash
crossslice expand sched_submit -C examples/taskrunner
```

Expected output:

```
sched_submit — src/sched.c:44 [gtags_unique] (0.04s)
  reads: s, t; writes: -
  callees (4):
    -> LOG_ERROR (include/log.h:10, summarized)
    -> validate_task (src/sched.c:6, summarized)
    -> queue_push (src/queue.c:17, summarized)
    -> LOG_INFO (include/log.h:8, summarized)
  callers (2):
    <- main (src/main.c:24, call at line 34)
    <- main (src/main.c:24, call at line 35)
```

`gtags_unique` is the resolution tier, `LOG_ERROR` and `LOG_INFO` are
function-like macros resolved to their definitions, `validate_task` is a
static function, and `main` appears once per call site.

```bash
T=examples/taskrunner
crossslice expand sched_drain -C $T --levels 2 --dot /tmp/graph.dot   # two rings, Graphviz output
crossslice expand queue_push -C $T --direction up                     # callers only
crossslice expand task_execute -C $T                                  # calls t->fn(...) through a pointer: no edge is reported
crossslice context $T/src/sched.c:50 -C $T --slice                    # the function at a line, with the slice around it
crossslice explore -C $T --focus sched_submit --open                  # the explorer
```

## kvstore-evolution

`old/` and `new/` are the two versions of the project. `init.sh` creates
`kvstore/`, a git repository with the two versions as commits:

```bash
bash examples/kvstore-evolution/init.sh
# kvstore/ created:
#   <sha> kv_put: reject oversized keys instead of overflowing the entry buffer
#   <sha> kvstore: initial implementation
```

In the first version `kv_put` copies the key with `strcpy` into the fixed-size
buffer `kv_entry.key`. The second commit adds a length check, the error code
`KV_ERR_KEYLEN` in `kv.h`, and a bounded `memcpy`.

```bash
cd examples/kvstore-evolution/kvstore
crossslice enrich                          # commit context of HEAD
crossslice enrich --no-cross               # intra-procedural slice only
git diff HEAD~1 HEAD                       # the raw diff, for comparison
crossslice explore --open                  # the same context in the commit tab
```

The output shows the def-use slice of `kv_put` around the change, the
definitions of `KV_MAX_KEY_LEN` and `KV_ERR_KEYLEN`, the callee `find_slot`
sliced to the call with its read/write summary, and the callers `kv_grow` and
`main` with their call sites.

Past revisions:

```bash
crossslice expand kv_put --rev HEAD~1     # the version with the overflow
crossslice expand kv_put --rev HEAD       # the fixed version
```

Each revision gets its own cached graph in `~/.cache/crossslice/`. The
analysis of a past revision runs in a temporary worktree.

For an agent:

```bash
cd examples/kvstore-evolution/kvstore
claude mcp add crossslice -- crossslice mcp
```

## Cleaning up

`make clean` in an example removes the compiled binaries, `bash
examples/kvstore-evolution/init.sh` recreates `kvstore/`, and `rm -rf
~/.cache/crossslice` removes all caches. CrossSlice writes nothing into the
examples themselves.
