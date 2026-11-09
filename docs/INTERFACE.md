# Interface for agents and clients

CrossSlice offers two programmatic interfaces, both served from the repository
graph (`crossslice/cross/graph.py`):

- the **MCP server** (`crossslice/cross/mcp_server.py`), typed tools over stdio
  JSON-RPC for clients of the Model Context Protocol;
- the **HTTP server** (`crossslice/cross/graph_server.py`), a JSON API behind
  the explorer.

Both return compact representations instead of files: a function arrives as
its def-use slice or as a one-line read/write summary.

## MCP server

The server works on the repository it is started in and has two modes.

- **Working tree** (default). The symbol tools answer for the files on disk
  (`version="work"`). The commit tools take a revision (`rev`, default HEAD),
  and the symbol tools can address that commit's parent (`version="old"`) and
  the commit itself (`version="new"`), so a function can be compared before
  and after a change.
- **Commit scope** (`--commit REV`). The server is about one commit;
  `version` defaults to `"new"` and `rev` to that commit.

Outside a git repository only `version="work"` is available, and the commit
tools return an error that says so.

### Starting and registering

```bash
crossslice mcp                       # working tree of the repository in the current directory
crossslice mcp -C REPO --commit REV
claude mcp add crossslice -- crossslice mcp     # Claude Code, from inside the repository
```

Any MCP client with a stdio transport can start the command. The VS Code
extension registers the server with VS Code's agent mode and can write
`.vscode/mcp.json` or `.mcp.json`. Without `uv tool install`, register `uv run
--project /path/to/crossslice crossslice mcp`.

The server needs the same external tools as the command line. The first tool
call for a version builds that version's symbol index; later calls use the
cache in `~/.cache/crossslice/`. SIGTERM and SIGINT stop the server and remove
its temporary worktrees.

### Channel isolation

The server serves MCP over private copies of its original stdin and stdout and
then points fd 0 at `/dev/null` and fd 1 at stderr. Output of every child
process (gtags, global, git, GumTree, clangd, gcc) and every print from any
thread therefore goes to stderr, never to the protocol channel.

### Tools

Commit tools take `rev` (any git revision; default the server's `--commit`,
else HEAD). Symbol tools take `version` (`"work"`, `"old"` or `"new"`; default
`"new"` under `--commit`, else `"work"`) and `rev`. Results are one text
content block with JSON or plain text, clipped to 20,000 characters. User
errors such as an unknown revision, a root commit or a missing git repository
come back as `{"error": "..."}`.

| Tool | Input | Returns |
|---|---|---|
| `get_commit_overview` | `rev?` | `{commit, parent, changed_files, changed_functions}` |
| `get_raw_diff` | `rev?` | unified diff (`-U3`) |
| `get_intra_diff` | `rev?` | the change merged with its intra-procedural def-use slice |
| `list_changed_functions` | `rev?` | `[name, …]` |
| `resolve_symbol` | `name`, `version?` | `{resolved, file, line, kind, signature, resolution_method, ambiguous}`; with several definitions also `definitions` and `alternatives` |
| `get_sliced_body` | `name`, `version?` | one summary line (reads, writes, returns) and the body sliced to the statements connected to parameters and return values; `...` marks omitted statements |
| `get_summary` | `name`, `version?` | `{params_read, params_written, params_rebound, returns}`; `params_written` lists `p*` for every parameter whose object is written, directly, through an alias, a library call, an out-argument or a called macro; `params_rebound` are by-value parameters reassigned locally |
| `get_callers` | `name`, `version?`, `limit?` (default 50) | `{callers: [{caller, file, line}]}` |
| `expand_function` | `name`, `version?`, `levels?` (1 to 3) | `{node, callees, callers}` with the call lines of every edge; `levels > 1` adds `rings` with at most 10 nodes per neighbor and 60 per ring |
| `get_function_source` | `name`, `version?` | the definition verbatim with line numbers, headed by `name (kind, version) — file:start-end` |
| `get_neighborhood` | `name`, `version?` | in one call: location and summary of the function, an `AMBIGUOUS` line when the name has several definitions, callees as one-line summaries (functions, then macros, then names without a definition in the repository), callers with their call-site lines, and the definitions of the struct, union, enum and `_t` types the function names |
| `get_context_at` | `file`, `line`, `version?` | the function containing the line with its summary, the def-use slice around the line (`>` marks it), callees, callers and types |
| `get_type_definition` | `name`, `version?` | a struct, union, enum, typedef, macro or global definition with file and line span |

**Version lock.** `--lock-version old|new` together with `--commit` restricts
the server to one version of the commit. The commit tools then return an
error and every symbol tool answers for the locked version regardless of the
`version` or `rev` passed.

**Ambiguous names.** When several definitions share a name and no call site is
available for clangd, the reported one is ranked: functions over macros,
macros over alias macros (`#define get_bits bits_read_nz`), real code over
stubs (`#define av_log(a, ...) while(0)`), and ordinary paths over test and
generator paths. Which `#if` branch a build selects is not known without a
build, so `resolve_symbol` returns `ambiguous: true` with the alternatives,
`get_neighborhood` prints an `AMBIGUOUS` line, and `get_context_at(file,
line)` addresses one definition.

**Sliced bodies.** `get_sliced_body` and the slice of `get_context_at` keep
the statements connected to the parameters and return values, or to the seed
line, then add the reaching definitions of the variables they use and the
control-flow headers that enclose them. The reaching definitions are the
nearest unconditional assignment or declaration and the conditional
assignments between it and the use.

**Macros in summaries.** A summary looks one level into called macros: a macro
that writes through one of its arguments or through a variable of the caller
counts as a write to the corresponding parameter. Macro bodies are not
expanded further. When a macro has several definitions in one file (`#if X
... #else ... #endif`), the later one is reported and the callee line says
`(1 of N definitions)`.

**Resolution provenance.** `resolution_method` on `resolve_symbol` and on
graph nodes is `gtags_unique` (one verified definition in the index),
`gtags+ts` (several candidates, one verified by tree-sitter), `lsp` (decided
by clangd) or `priority_fallback` (ranked choice after clangd gave no
answer). Treat `priority_fallback` as lower confidence.

**Response sizes.** `get_summary` returns tens of tokens; `resolve_symbol`,
`get_callers` and `expand_function` return node lists without bodies;
`get_sliced_body` returns the slice, which is a fraction of the function;
every response is clipped at 20,000 characters.

**Log.** Every tool call is logged to the server's stderr as `[mcp] <tool>(<args>)
ok <seconds>s <chars> chars`, or with `ERROR` and a traceback.

**Failures.** Tools do not raise across the wire. Unresolved symbols come back
as `{"resolved": false, ...}` or `{"error": "..."}` inside a normal result;
only an internal exception sets `isError: true`. A symbol without a definition
in the repository, such as a libc function, is reported as not resolved.

**Typical sequences.** To review a commit: `get_commit_overview`, then
`get_intra_diff`, then `get_sliced_body` or `get_summary` on the callees and
`get_callers` on the changed functions. To compare a function before and after
a change: `get_summary(name, "old")` and `get_summary(name, "new")`. To trace
impact: `get_callers` upward and `expand_function` downward, with
`get_summary` on the neighbors and `get_sliced_body` where detail is needed.

The server exposes these primitives rather than a finished commit context, so
that an agent retrieves only what it needs. The command line produces the
complete commit context with `crossslice enrich`.

## HTTP server

```bash
crossslice explore [-C REPO] [--rev REV] [--focus FUNCTION] [--levels N] [--port N] [--open]
```

Without `--port` the server takes 8000 or the next free port and prints the
URL. The explorer is served at `/`.

| Method and path | Body or query | Returns |
|---|---|---|
| `GET /api/state` | — | the materialized graph `{nodes, edges, focus, stats}` |
| `POST /api/expand` | `{id}`, or `{name}`, or `{name, file, line, kind}`, plus `levels` | the graph after expanding that node, with `focus_id` |
| `GET /api/search?q=NAME` | — | definition candidates for NAME |
| `GET /api/node?id=ID` or `?name=NAME` | — | node detail: sliced `body`, `summary`, location, provenance, `alternatives`, caller totals |
| `POST /api/update` | — | incremental refresh after the repository changed |
| `GET /api/commits?limit=N` | — | recent commits that change C files: `{commits: [{sha, short, subject, author, when, merge}]}` |
| `GET /api/commit?rev=REV` | — | commit context of REV, cached per SHA: `{sha, parent, subject, files, functions, text, sections, diff, seconds, note, cross_error}` |

Errors are `{"error": "..."}` with status 400 for user errors and 500
otherwise. Nodes are `{id, name, file, line, state, kind, resolution_method}`
and edges `{src, dst, line}`. The JSON shapes match the MCP tool outputs.

## Stability

The schemas returned by the MCP `tools/list` call and the HTTP shapes above
are the interface contract. The 20,000-character clip and the `levels` cap
keep every response bounded.
