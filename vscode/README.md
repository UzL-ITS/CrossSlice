# CrossSlice for VS Code

Commit and code context for C projects, inside the editor: the def-use slice
around a line, the called functions sliced to what matters, the callers with
their call sites, and the macros involved. Backed by the CrossSlice analysis
server, which the extension starts for the open folder.

## Commands

| Command | What it does |
|---|---|
| **CrossSlice: Open Explorer** | the interactive call graph in a panel: click a function for its sliced body and summary, double-click to expand; the **Commit** tab shows the context of recent commits. Locations open in the editor. |
| **CrossSlice: Context for Symbol Under Cursor** | the function at the cursor: read/write summary, def-use slice around that line, callees, callers, types. Also in the editor context menu and as a CodeLens above every function. |
| **CrossSlice: Show Symbol Under Cursor in Explorer** | expands that function in the explorer panel |
| **CrossSlice: Commit Context** | pick a recent commit or type a revision; the enriched context opens as a document |
| **CrossSlice: Start / Stop Backend**, **Show Backend Log** | the analysis server (status bar item `CrossSlice`) |

## Backend

The extension starts one backend per workspace folder and stops it when the
window closes (`crossslice.backend`):

- `auto` (default): the `crossslice` command when it is installed, else Docker.
- `local`: `crossslice explore` on this machine. Install it with
  `uv tool install .` in the CrossSlice checkout, or set
  `crossslice.localCommand` to `uv run --project /path/to/crossslice crossslice`.
  Needs git, GNU Global, Java and GumTree (`crossslice check`). GumTree is found
  through `GUMTREE_PATH`, `gumtree` on PATH, or a release unpacked under
  `/opt/gumtree` or `~/gumtree`; `crossslice.gumtreePath` names it explicitly,
  and `crossslice.env` adds environment variables for the backend process.
- `docker`: the CrossSlice image with the folder mounted at `/repo` and a named
  volume for the caches. Nothing else to install. The image is
  `crossslice.dockerImage` (`docker build -t crossslice .` in the checkout, or
  the published image once available). `podman` is used when `docker` is absent.

With Remote-SSH or Codespaces the backend runs where the files are; the panel
reaches it through VS Code's port forwarding.

## Install

From a `.vsix` file: *Extensions: Install from VSIX…* in the command palette,
or `code --install-extension crossslice-0.1.0.vsix`.

From source:

```bash
cd vscode && npm install && npm run package   # produces crossslice-0.1.0.vsix
```

Or open `vscode/` in VS Code and press F5 for an Extension Development Host.

## Agents (MCP)

The same analysis is available to coding agents as an MCP server. The
extension offers it to VS Code's agent mode automatically (it appears under
*MCP: List Servers* as "CrossSlice (folder)"), started with the same backend
mode as the explorer. **CrossSlice: Add MCP Server for Agents…** writes the
configuration for other clients: `.vscode/mcp.json` (VS Code) and `.mcp.json`
(Claude Code, picked up when `claude` runs in the folder).
