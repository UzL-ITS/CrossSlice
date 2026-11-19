# Usage

CrossSlice computes the code context of a commit, a function or a line of a C
project: the def-use slice around a change, the called functions sliced to the
call, the callers with their call sites, and the macros involved. This guide
covers the command line, the explorer, the VS Code extension, the MCP server,
batch processing, the Python API and Docker.

## Setup

```bash
uv tool install .                    # installs the `crossslice` command
sudo bash scripts/setup_tools.sh     # external tools on RHEL/CentOS 9; see README for other systems
crossslice check                     # verifies git, GNU Global, clangd, Java and GumTree
```

GumTree is found in `/opt/gumtree` or `~/gumtree`; elsewhere set `GUMTREE_PATH`
to its `bin/gumtree`.

## Conventions

- Every command analyzes the git repository that contains the current
  directory. `-C DIR` analyzes another directory, exactly as given.
- `--rev REV` analyzes a past revision. The revision is checked out into a
  temporary worktree that is removed afterwards.
- Outside a git repository the code-context commands work and the commit
  commands report that they need git.
- Indexes and graph stores are written to `~/.cache/crossslice/<repo>-<hash>/`
  (`--cache-dir DIR` or `CROSSSLICE_CACHE_DIR`). Nothing is written into the
  analyzed checkout.
- `CROSSSLICE_DEFUSE=scalar` switches the def/use analysis from access paths
  to plain identifiers. It exists for comparison runs only.

## Commit context

```bash
crossslice enrich                          # HEAD against its first parent
crossslice enrich REV                      # any revision
crossslice enrich REV --parent REV2        # another base revision
crossslice enrich REV --no-cross           # intra-procedural slice only
crossslice enrich REV -o context.txt -v    # write to a file, verbose
```

The output lists, per changed function, the changed lines merged with the
statements they depend on, then the called functions sliced to the call with
a `[reads: …; writes: …]` summary, the macro definitions the change uses, and
the callers with the call site marked `>`. If the cross-function step fails,
the intra-procedural result is still printed and the error goes to stderr.

## Code context

```bash
crossslice context FILE:LINE               # the function containing the line, summary, callees, callers, types
crossslice context FILE:LINE --slice       # adds the def-use slice around the line
crossslice context FILE:LINE --rev v1.2.12 # at a past revision
crossslice expand FUNCTION                 # callees and callers with summaries
crossslice expand FUNCTION --levels 2      # two rings
crossslice expand FUNCTION --direction up  # callers only
crossslice expand FUNCTION --dot graph.dot # Graphviz output
```

## Explorer

```bash
crossslice explore --open                  # http://127.0.0.1:8000/, or the next free port
crossslice explore --focus FUNCTION        # start with one function expanded
crossslice explore --rev REV               # a past revision
```

- Search a function or macro by name. `/` focuses the search box, Enter
  selects the first hit.
- Click a node to open its detail panel: sliced or full body, read/write
  summary, signature, resolution tier, callees and callers.
- Double-click a node, or press *Expand neighborhood*, to add one ring of
  callers and callees. The depth selector adds two rings at once.
- Mouse wheel zooms, dragging the background pans, dragging a node moves it,
  *fit* or `f` frames the graph. Dashed nodes are summarized, solid blue nodes
  are analyzed, amber nodes are macros.
- `↻ update` refreshes the graph after the repository changed.
- The *Commit* tab shows the commit context of recent commits or of a typed
  revision. Changed functions, callees and callers link into the graph, and
  *Copy as text* copies the whole context.
- Keys: `/` search, `e` expand the selected node, `f` fit, `c` commit tab,
  `Esc` close the panel on top, `?` help.

## VS Code

The extension in `vscode/` provides the explorer in a panel, *Context for
Symbol Under Cursor* in the editor context menu and as a CodeLens above each
C function, and *Commit Context* for a chosen revision. It starts the backend
for the open folder with the local `crossslice` command or, if none is
installed, with the Docker image (setting `crossslice.backend`, default
`auto`). On SELinux hosts it adds the required mount option itself.

```bash
cd vscode && npm install && npm run package      # crossslice-0.1.0.vsix
code --install-extension crossslice-0.1.0.vsix
```

## MCP server

```bash
cd /path/to/repo
claude mcp add crossslice -- crossslice mcp
```

VS Code's agent mode reads `.vscode/mcp.json`; the extension offers the server
there by itself and *CrossSlice: Add MCP Server for Agents…* writes the file.
By hand:

```json
{
  "servers": {
    "crossslice": {
      "type": "stdio",
      "command": "crossslice",
      "args": ["mcp", "-C", "${workspaceFolder}"]
    }
  }
}
```

The symbol tools answer for the files on disk by default (`version="work"`).
The commit tools take a revision (`rev`, default HEAD), and the symbol tools
can address its parent and the commit itself (`version="old"` and `"new"`).
`crossslice mcp --commit REV` scopes the whole server to one commit. Without
`uv tool install`, register `uv run --project /path/to/crossslice crossslice
mcp`. The tools and their outputs are described in
[docs/INTERFACE.md](docs/INTERFACE.md).

## Batch processing

```bash
crossslice dataset commits.jsonl --repos-dir ./repos --out-dir ./outputs
```

Each line of the input names a commit (`project_url`, `commit_id`).
Repositories are cloned on demand, and the output is one `<repo>_<sha>.txt`
per commit.

## Python

```python
from crossslice import RepoGraph, enrich_commit

g = RepoGraph("/path/to/repo")            # or RepoGraph(repo, commit="REV")
g.expand("mp_decode_layer3", levels=1)
hood = g.neighborhood("mp_decode_layer3")
g.update()
g.close()

res = enrich_commit("/path/to/repo", "HEAD", cross=True)
res.text, res.changed_files, res.functions, res.cross_stats, res.seconds
```

Nodes carry the statement-level IR and the read/write summary that the commit
pipeline uses.

## Docker

The image contains git, GNU Global, clangd, gcc, Java and GumTree. Docker and
Podman both work.

```bash
docker build -t crossslice .
docker run --rm -p 127.0.0.1:8000:8000 crossslice        # the explorer on the bundled example
```

For your own checkout, mount it at `/repo`, keep the caches in a named volume
and run as your user so that files created in the mount belong to you:

```bash
cd /path/to/repo
alias crossslice='docker run --rm -i -u "$(id -u):$(id -g)" -v "$PWD:/repo" -v crossslice-cache:/cache crossslice'
crossslice check
crossslice enrich REV
crossslice context src/file.c:120 --slice
crossslice mcp                                           # MCP server over stdio
docker run --rm -p 127.0.0.1:8000:8000 -u "$(id -u):$(id -g)" -v "$PWD:/repo" \
    -v crossslice-cache:/cache crossslice explore         # http://127.0.0.1:8000
```

For a coding agent: `claude mcp add crossslice -- docker run --rm -i -u "$(id -u):$(id -g)" -v "$PWD:/repo" -v crossslice-cache:/cache crossslice mcp`.

On SELinux hosts (Fedora, RHEL) add `--security-opt label=disable` to the
`docker run` commands. `docker volume rm crossslice-cache` removes the caches
and `docker rmi crossslice` the image.

## Troubleshooting

| Symptom | What to do |
|---|---|
| `GumTree binary not found` | unpack the release into `/opt/gumtree` or `~/gumtree`, or set `GUMTREE_PATH` to its `bin/gumtree`; `crossslice check` shows what is found |
| `not a git repository: commit mode unavailable` | run inside a git checkout or pass `-C REPO`; `context`, `expand` and `explore` work without git |
| `git worktree add` hangs, or `/tmp/cce_wt_*` directories remain | a previous run was killed with SIGKILL; run `git -C REPO worktree prune && rm -rf /tmp/cce_wt_*` |
| gtags or clangd missing | `scripts/setup_tools.sh`, your package manager, or the Docker image |
| the first query on a large repository takes seconds | the symbol index is built once per repository and revision; later queries use the cache |
| port 8000 is taken | `explore` takes the next free port and prints the URL; `--port N` fixes one |
| a symbol does not resolve | it has no definition in the repository, for example a libc function; `resolve_symbol` and `/api/search` report the reason |

## Limitations

C only. Calls through function pointers are not followed. Macros are shown
with their definitions, not expanded.
