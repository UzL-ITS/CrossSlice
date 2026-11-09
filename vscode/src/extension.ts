/**
 * CrossSlice for VS Code.
 *
 * A thin client: it starts ONE backend per workspace folder — `crossslice explore`
 * on this machine, or the Docker image with the folder mounted — and talks to it
 * over HTTP on localhost. The explorer panel is a webview showing the backend's
 * web UI; locations clicked there open in the editor. "Context for symbol under
 * cursor" and "Commit context" ask the same backend and show the text as a
 * read-only document.
 */
import * as cp from 'child_process';
import * as crypto from 'crypto';
import * as fs from 'fs';
import * as http from 'http';
import * as net from 'net';
import * as path from 'path';
import * as vscode from 'vscode';

const SCHEME = 'crossslice';

interface Backend {
  proc: cp.ChildProcess;
  port: number;
  url: string; // reachable from the extension host
  mode: 'local' | 'docker';
  dockerCmd?: string;
  containerName?: string;
  folder: string; // the workspace folder being analyzed
}

let backend: Backend | undefined;
let starting: Promise<Backend> | undefined;
let status: vscode.StatusBarItem;
let log: vscode.OutputChannel;
let panel: vscode.WebviewPanel | undefined;
let panelBase: string | undefined;
const lensEmitter = new vscode.EventEmitter<void>();
const documents = new Map<string, string>();
const docEmitter = new vscode.EventEmitter<vscode.Uri>();

// ------------------------------------------------------------------ helpers

function setting<T>(key: string, fallback: T): T {
  return vscode.workspace.getConfiguration('crossslice').get<T>(key, fallback);
}

function splitCommand(cmd: string): string[] {
  return cmd.trim().split(/\s+/).filter(Boolean);
}

const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
const enc = encodeURIComponent;

/** Does `cmd args...` run and exit 0? (ENOENT, non-zero exit and timeouts are "no".) */
function runs(cmd: string, args: string[], timeoutMs = 15000): Promise<boolean> {
  return new Promise((resolve) => {
    let done = false;
    const finish = (ok: boolean) => {
      if (!done) {
        done = true;
        resolve(ok);
      }
    };
    try {
      const p = cp.spawn(cmd, args, { stdio: 'ignore' });
      const t = setTimeout(() => {
        p.kill();
        finish(false);
      }, timeoutMs);
      p.on('error', () => {
        clearTimeout(t);
        finish(false);
      });
      p.on('exit', (code) => {
        clearTimeout(t);
        finish(code === 0);
      });
    } catch {
      finish(false);
    }
  });
}

function freePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const srv = net.createServer();
    srv.once('error', reject);
    srv.listen(0, '127.0.0.1', () => {
      const addr = srv.address() as net.AddressInfo;
      srv.close(() => resolve(addr.port));
    });
  });
}

function getJson<T = any>(url: string, timeoutMs = 180000): Promise<T> {
  return new Promise((resolve, reject) => {
    const req = http.get(url, (res) => {
      const chunks: Buffer[] = [];
      res.on('data', (c) => chunks.push(c));
      res.on('end', () => {
        const body = Buffer.concat(chunks).toString('utf8');
        let data: any;
        try {
          data = JSON.parse(body);
        } catch {
          reject(new Error(`${res.statusCode}: ${body.slice(0, 200)}`));
          return;
        }
        if (data && data.error) reject(new Error(String(data.error)));
        else if ((res.statusCode ?? 500) >= 400) reject(new Error(`HTTP ${res.statusCode}`));
        else resolve(data as T);
      });
    });
    req.setTimeout(timeoutMs, () => req.destroy(new Error('the backend did not answer in time')));
    req.on('error', reject);
  });
}

function currentFolder(): string | undefined {
  const ed = vscode.window.activeTextEditor;
  if (ed) {
    const f = vscode.workspace.getWorkspaceFolder(ed.document.uri);
    if (f) return f.uri.fsPath;
  }
  return vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
}

/** A file's path relative to the analyzed folder, with forward slashes. */
function relPath(b: Backend, fsPath: string): string {
  const rel = path.relative(b.folder, fsPath);
  if (!rel || rel.startsWith('..') || path.isAbsolute(rel)) {
    throw new Error(`${fsPath} is outside the analyzed folder ${b.folder}. Stop the backend to switch folders.`);
  }
  return rel.split(path.sep).join('/');
}

function busy<T>(title: string, fn: () => Promise<T>): Promise<T> {
  return Promise.resolve(vscode.window.withProgress({ location: vscode.ProgressLocation.Window, title }, fn));
}

// ------------------------------------------------------------------ backend

async function containerCli(): Promise<string | undefined> {
  const configured = setting('dockerCommand', '');
  if (configured) return (await runs(configured, ['--version'])) ? configured : undefined;
  for (const c of ['docker', 'podman']) if (await runs(c, ['--version'])) return c;
  return undefined;
}

async function resolveMode(): Promise<{ mode: 'local' | 'docker'; dockerCmd?: string }> {
  const pref = setting<'auto' | 'local' | 'docker'>('backend', 'auto');
  const local = splitCommand(setting('localCommand', 'crossslice'));
  if (pref !== 'docker' && local.length) {
    if (await runs(local[0], [...local.slice(1), '--version'])) return { mode: 'local' };
    if (pref === 'local') {
      throw new Error(
        `'${local.join(' ')}' is not installed (setting crossslice.localCommand). ` +
          `Install it with 'uv tool install .' in the CrossSlice checkout, or set crossslice.backend to "docker".`,
      );
    }
  }
  const dockerCmd = await containerCli();
  if (dockerCmd) return { mode: 'docker', dockerCmd };
  throw new Error(
    pref === 'docker'
      ? 'Neither docker nor podman is available (setting crossslice.dockerCommand).'
      : `Neither '${local.join(' ')}' nor docker/podman is available. Install CrossSlice ('uv tool install .') or Docker.`,
  );
}

function buildCommand(
  mode: 'local' | 'docker',
  dockerCmd: string | undefined,
  folder: string,
  port: number,
): { cmd: string; args: string[]; containerName?: string } {
  if (mode === 'local') {
    const [cmd, ...pre] = splitCommand(setting('localCommand', 'crossslice'));
    return { cmd, args: [...pre, 'explore', '-C', folder, '--port', String(port), '--host', '127.0.0.1'] };
  }
  const containerName = 'crossslice-' + crypto.createHash('sha1').update(folder).digest('hex').slice(0, 10);
  const args = [...dockerBaseArgs(folder, { port, name: containerName }), setting('dockerImage', 'crossslice'), 'explore'];
  return { cmd: dockerCmd ?? 'docker', args, containerName };
}

function selinuxEnforcing(): boolean {
  try {
    return process.platform === 'linux' && fs.readFileSync('/sys/fs/selinux/enforce', 'utf8').trim() === '1';
  } catch {
    return false;
  }
}

/** `docker run` arguments shared by the explorer backend and the MCP server:
 *  the folder mounted at /repo (the working directory), the cache volume, the
 *  host user so nothing in the checkout becomes root-owned. */
function dockerBaseArgs(folder: string, opts: { port?: number; name?: string; interactive?: boolean }): string[] {
  const volume = setting('dockerCacheVolume', 'crossslice-cache');
  const args = ['run', '--rm'];
  if (opts.interactive) args.push('-i');
  if (opts.name) args.push('--name', opts.name);
  if (opts.port) args.push('-p', `127.0.0.1:${opts.port}:8000`);
  args.push('-v', `${folder}:/repo`, '-v', `${volume}:/cache`);
  if (process.platform !== 'win32' && process.getuid && process.getgid) {
    args.push('-u', `${process.getuid()}:${process.getgid()}`);
  }
  if (selinuxEnforcing()) args.push('--security-opt', 'label=disable'); // bind mount readable under SELinux
  args.push(...setting<string[]>('dockerExtraArgs', []));
  return args;
}

/** Environment overrides for a backend process (settings crossslice.env / gumtreePath). */
function envOverrides(): Record<string, string> {
  const out: Record<string, string> = {};
  for (const [k, v] of Object.entries(setting<Record<string, string>>('env', {}))) {
    out[k] = v.replace(/\$\{env:(\w+)\}/g, (_m, name) => process.env[name] ?? '');
  }
  const gumtree = setting('gumtreePath', '');
  if (gumtree) out.GUMTREE_PATH = gumtree;
  return out;
}

async function startBackend(): Promise<Backend> {
  const folder = currentFolder();
  if (!folder) throw new Error('Open a folder (a C repository) first.');
  const { mode, dockerCmd } = await resolveMode();
  const port = await freePort();
  const { cmd, args, containerName } = buildCommand(mode, dockerCmd, folder, port);
  log.appendLine(`[crossslice] $ ${cmd} ${args.join(' ')}`);
  updateStatus('starting');

  const env: NodeJS.ProcessEnv = { ...process.env, ...envOverrides() };
  const proc = cp.spawn(cmd, args, { cwd: folder, env });
  const tail: string[] = [];
  const onData = (d: Buffer) => {
    const t = d.toString();
    log.append(t);
    for (const l of t.split('\n')) {
      if (l.trim()) {
        tail.push(l.trim());
        if (tail.length > 6) tail.shift();
      }
    }
  };
  proc.stdout?.on('data', onData);
  proc.stderr?.on('data', onData);
  const b: Backend = { proc, port, url: `http://127.0.0.1:${port}`, mode, dockerCmd, containerName, folder };
  let exited = false;
  proc.on('error', (e) => {
    tail.push(e.message);
    exited = true;
  });
  proc.on('exit', (code, signal) => {
    exited = true;
    log.appendLine(`[crossslice] backend exited (${code ?? signal})`);
    if (backend === b) {
      backend = undefined;
      updateStatus('off');
      lensEmitter.fire();
    }
  });

  // Docker may have to pull the image on the first run
  const deadline = Date.now() + (mode === 'docker' ? 180000 : 60000);
  while (Date.now() < deadline && !exited) {
    try {
      const h = await getJson<{ ok: boolean }>(`${b.url}/api/health`, 2000);
      if (h.ok) {
        backend = b;
        updateStatus('on');
        lensEmitter.fire();
        log.appendLine(`[crossslice] ready at ${b.url} (${mode}) for ${folder}`);
        return b;
      }
    } catch {
      /* not up yet */
    }
    await sleep(300);
  }
  if (!exited) proc.kill('SIGTERM');
  updateStatus('off');
  throw new Error(`The CrossSlice backend (${mode}) did not start. ${tail.join(' | ')}`);
}

function ensureBackend(): Promise<Backend> {
  if (backend) return Promise.resolve(backend);
  if (!starting) {
    starting = busy('CrossSlice: starting the backend…', startBackend).finally(() => {
      starting = undefined;
    });
  }
  return starting;
}

async function stopBackend(): Promise<void> {
  const b = backend;
  if (!b) return;
  backend = undefined;
  updateStatus('off');
  lensEmitter.fire();
  if (b.mode === 'docker' && b.containerName && b.dockerCmd) {
    await runs(b.dockerCmd, ['stop', '-t', '5', b.containerName]);
  }
  if (b.proc.exitCode === null) b.proc.kill('SIGTERM');
  log.appendLine('[crossslice] backend stopped');
}

// ------------------------------------------------------------------ status bar

function updateStatus(state: 'off' | 'starting' | 'on') {
  if (state === 'on') {
    status.text = '$(graph) CrossSlice';
    status.tooltip = `CrossSlice backend (${backend?.mode}) at ${backend?.url}\n${backend?.folder}\nClick for actions`;
  } else if (state === 'starting') {
    status.text = '$(sync~spin) CrossSlice';
    status.tooltip = 'Starting the CrossSlice backend…';
  } else {
    status.text = '$(graph) CrossSlice: off';
    status.tooltip = 'CrossSlice backend not running. Click for actions';
  }
  status.show();
}

async function menu() {
  const items: (vscode.QuickPickItem & { cmd: string })[] = [
    { label: '$(graph) Open Explorer', description: 'call graph, details, Commit tab', cmd: 'crossslice.openExplorer' },
    { label: '$(symbol-method) Context for Symbol Under Cursor', description: 'summary, slice, callees, callers, types', cmd: 'crossslice.contextAtCursor' },
    { label: '$(git-commit) Commit Context', description: 'HEAD or any revision', cmd: 'crossslice.commitContext' },
    { label: '$(plug) Add MCP Server for Agents…', description: 'VS Code agent mode, Claude Code', cmd: 'crossslice.addMcp' },
    backend
      ? { label: '$(debug-stop) Stop Backend', description: `${backend.mode} at ${backend.url}`, cmd: 'crossslice.stop' }
      : { label: '$(debug-start) Start Backend', description: 'local crossslice or Docker (setting crossslice.backend)', cmd: 'crossslice.start' },
    { label: '$(output) Show Backend Log', cmd: 'crossslice.showLog' },
  ];
  const pick = await vscode.window.showQuickPick(items, { placeHolder: 'CrossSlice' });
  if (pick) await vscode.commands.executeCommand(pick.cmd);
}

// ------------------------------------------------------------------ documents

async function showDocument(name: string, text: string, language = 'plaintext') {
  const uri = vscode.Uri.from({ scheme: SCHEME, path: '/' + name });
  documents.set(uri.toString(), text);
  docEmitter.fire(uri);
  const doc = await vscode.workspace.openTextDocument(uri);
  if (doc.languageId !== language) await vscode.languages.setTextDocumentLanguage(doc, language);
  await vscode.window.showTextDocument(doc, { viewColumn: vscode.ViewColumn.Beside, preview: true });
}

// ------------------------------------------------------------------ commands

async function contextAtCursor(arg?: { uri: vscode.Uri; line: number }) {
  const ed = vscode.window.activeTextEditor;
  const uri = arg?.uri ?? ed?.document.uri;
  if (!uri || uri.scheme !== 'file') throw new Error('Open a C file first.');
  const line = arg?.line ?? (ed ? ed.selection.active.line + 1 : 1);
  const doc = vscode.workspace.textDocuments.find((d) => d.uri.toString() === uri.toString());
  if (doc?.isDirty) {
    const choice = await vscode.window.showWarningMessage(
      'CrossSlice analyzes the file on disk; this file has unsaved changes.', 'Save and continue', 'Continue');
    if (!choice) return;
    if (choice === 'Save and continue') await doc.save();
  }
  const b = await ensureBackend();
  const rel = relPath(b, uri.fsPath);
  const r = await busy(`CrossSlice: context for ${path.basename(rel)}:${line}…`, () =>
    getJson<{ text: string }>(`${b.url}/api/context?file=${enc(rel)}&line=${line}&slice=1`));
  await showDocument(`${path.basename(rel)}:${line} — context`, r.text);
}

async function showInExplorer(name?: string) {
  if (!name) {
    const ed = vscode.window.activeTextEditor;
    const range = ed && ed.document.getWordRangeAtPosition(ed.selection.active, /[A-Za-z_]\w*/);
    name = range ? ed!.document.getText(range) : undefined;
    if (!name) throw new Error('Put the cursor on a function or macro name first.');
  }
  await openExplorer(name);
}

interface CommitRow { sha: string; short: string; subject: string; author: string; when: string; merge: boolean }
interface CommitData {
  sha: string; parent: string; subject: string; author: string; when: string; files: string[];
  functions: string[]; text: string; seconds: number; note: string; cross_error: string;
}

async function commitContext(rev?: string) {
  const b = await ensureBackend();
  if (!rev) {
    const health = await getJson<{ is_git: boolean }>(`${b.url}/api/health`);
    if (!health.is_git) {
      throw new Error('This folder is not a git repository: commit context needs git. Code context works without it.');
    }
    const list = await getJson<{ commits: CommitRow[] }>(`${b.url}/api/commits?limit=30`);
    const items: vscode.QuickPickItem[] = [
      { label: 'HEAD', description: 'the last commit' },
      ...list.commits.map((c) => ({ label: c.short, description: c.subject, detail: `${c.author} · ${c.when}${c.merge ? ' · merge' : ''}` })),
      { label: '$(edit) Other revision…' },
    ];
    const pick = await vscode.window.showQuickPick(items, { placeHolder: 'Commit to analyze (commits that change .c/.h files)', matchOnDescription: true });
    if (!pick) return;
    rev = pick.label.startsWith('$(edit)')
      ? await vscode.window.showInputBox({ prompt: 'Revision: HEAD~2, a tag, a SHA' })
      : pick.label;
    if (!rev) return;
  }
  const r = await busy(`CrossSlice: analyzing ${rev}…`, () => getJson<CommitData>(`${b.url}/api/commit?rev=${enc(rev!)}`));
  const head = [
    r.subject,
    `${r.sha.slice(0, 12)} · ${r.author} · ${r.when} · parent ${r.parent.slice(0, 12)}`,
    `files: ${r.files.join(', ') || '-'}`,
    `changed functions: ${r.functions.join(', ') || '-'}`,
    r.note ? `note: ${r.note}` : undefined,
    r.cross_error ? `cross-function step failed (${r.cross_error}); intra-procedural result only` : undefined,
    '',
  ].filter((l) => l !== undefined);
  await showDocument(`commit ${r.sha.slice(0, 8)} — context`, head.join('\n') + '\n' + (r.text || '(this commit changes no .c or .h files)'), 'diff');
  const choice = await vscode.window.showInformationMessage(
    `CrossSlice: ${r.sha.slice(0, 8)} analyzed in ${r.seconds} s.`, 'Open in Explorer');
  if (choice) await openExplorer(undefined, r.sha);
}

// ------------------------------------------------------------------ MCP for agents

/** The command that starts `crossslice mcp` for `folder`, in the configured
 *  backend mode. `folderExpr` is what goes into the arguments (an absolute path,
 *  or `${workspaceFolder}` for .vscode/mcp.json). */
async function mcpCommand(folderExpr: string): Promise<{ command: string; args: string[]; mode: string }> {
  const { mode, dockerCmd } = await resolveMode();
  if (mode === 'local') {
    const [command, ...pre] = splitCommand(setting('localCommand', 'crossslice'));
    return { command, args: [...pre, 'mcp', '-C', folderExpr], mode };
  }
  return {
    command: dockerCmd ?? 'docker',
    args: [...dockerBaseArgs(folderExpr, { interactive: true }), setting('dockerImage', 'crossslice'), 'mcp'],
    mode,
  };
}

/** VS Code agent mode discovers the server through this provider: no file to write. */
function registerMcpProvider(context: vscode.ExtensionContext) {
  const changed = new vscode.EventEmitter<void>();
  context.subscriptions.push(
    changed,
    vscode.lm.registerMcpServerDefinitionProvider('crossslice.mcp', {
      onDidChangeMcpServerDefinitions: changed.event,
      provideMcpServerDefinitions: async () => {
        const defs: vscode.McpStdioServerDefinition[] = [];
        for (const f of vscode.workspace.workspaceFolders ?? []) {
          try {
            const { command, args } = await mcpCommand(f.uri.fsPath);
            const def = new vscode.McpStdioServerDefinition(`CrossSlice (${f.name})`, command, args, envOverrides(), '0.1.0');
            def.cwd = f.uri;
            defs.push(def);
          } catch (e: any) {
            log.appendLine(`[crossslice] MCP server not offered for ${f.name}: ${e?.message ?? e}`);
          }
        }
        return defs;
      },
      resolveMcpServerDefinition: (def) => def,
    }),
    vscode.workspace.onDidChangeWorkspaceFolders(() => changed.fire()),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('crossslice')) changed.fire();
    }),
  );
}

function mergeJsonFile(file: string, key: string, entry: unknown): void {
  let data: any = {};
  if (fs.existsSync(file)) {
    const text = fs.readFileSync(file, 'utf8');
    try {
      data = text.trim() ? JSON.parse(text) : {};
    } catch {
      throw new Error(`${file} is not valid JSON; add the server by hand or fix the file first.`);
    }
  }
  if (typeof data !== 'object' || data === null || Array.isArray(data)) data = {};
  data[key] = { ...(data[key] ?? {}), crossslice: entry };
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2) + '\n');
}

async function addMcpServer() {
  const folder = currentFolder();
  if (!folder) throw new Error('Open a folder (a C repository) first.');
  const pick = await vscode.window.showQuickPick(
    [
      { label: '$(vscode) VS Code agent mode', description: '.vscode/mcp.json', detail: 'Copilot Chat and other clients that read the workspace file. (This extension already offers the server to VS Code; the file pins the command and lets you edit it.)', id: 'vscode' },
      { label: '$(terminal) Claude Code', description: '.mcp.json', detail: 'Picked up when `claude` runs in this folder; it asks once before using a project server.', id: 'claude' },
      { label: '$(checklist) Both', description: '.vscode/mcp.json and .mcp.json', id: 'both' },
    ],
    { placeHolder: 'Where should the CrossSlice MCP server be registered?' },
  );
  if (!pick) return;
  const env = envOverrides();
  const written: string[] = [];
  if (pick.id !== 'claude') {
    const { command, args } = await mcpCommand('${workspaceFolder}');
    const file = path.join(folder, '.vscode', 'mcp.json');
    mergeJsonFile(file, 'servers', { type: 'stdio', command, args, ...(Object.keys(env).length ? { env } : {}) });
    written.push(file);
  }
  if (pick.id !== 'vscode') {
    const { command, args } = await mcpCommand(folder);
    const file = path.join(folder, '.mcp.json');
    mergeJsonFile(file, 'mcpServers', { command, args, ...(Object.keys(env).length ? { env } : {}) });
    written.push(file);
  }
  const { mode } = await mcpCommand(folder);
  const choice = await vscode.window.showInformationMessage(
    `CrossSlice MCP server (${mode} backend) registered in ${written.map((f) => path.relative(folder, f)).join(' and ')}. ` +
      (pick.id === 'vscode' ? 'Open the Chat view in agent mode and look for the crossslice tools.' :
        pick.id === 'claude' ? 'Start `claude` in this folder and approve the project server.' :
          'VS Code: Chat view in agent mode. Claude Code: start `claude` in this folder.'),
    ...written.map((f) => `Open ${path.basename(f)}`),
  );
  if (choice) {
    const file = written.find((f) => choice.endsWith(path.basename(f)));
    if (file) await vscode.window.showTextDocument(vscode.Uri.file(file));
  }
}

// ------------------------------------------------------------------ explorer panel

function webviewHtml(src: string, origin: string): string {
  const nonce = crypto.randomBytes(16).toString('hex');
  return `<!DOCTYPE html>
<html><head><meta charset="utf-8">
<meta http-equiv="Content-Security-Policy"
      content="default-src 'none'; frame-src ${origin}; script-src 'nonce-${nonce}'; style-src 'unsafe-inline';">
<style>html,body{height:100%;margin:0;overflow:hidden;background:#020617}iframe{border:0;width:100%;height:100%;display:block}</style>
</head><body>
<iframe id="f" src="${src}" allow="clipboard-write"></iframe>
<script nonce="${nonce}">
  const vscode = acquireVsCodeApi();
  const f = document.getElementById('f');
  let ready = false; const queue = [];
  window.addEventListener('message', (e) => {
    const m = e.data;
    if (!m || typeof m !== 'object' || typeof m.type !== 'string') return;
    if (e.source === f.contentWindow) { if (m.type.startsWith('crossslice:')) vscode.postMessage(m); }   // UI -> editor
    else if (ready) f.contentWindow.postMessage(m, '*'); else queue.push(m);                           // editor -> UI
  });
  f.addEventListener('load', () => { ready = true; for (const m of queue) f.contentWindow.postMessage(m, '*'); queue.length = 0; });
</script>
</body></html>`;
}

async function openExplorer(focus?: string, commit?: string) {
  const b = await ensureBackend();
  const external = await vscode.env.asExternalUri(vscode.Uri.parse(b.url));
  const base = external.toString().replace(/\/$/, '');
  const origin = `${external.scheme}://${external.authority}`;
  const src = `${base}/?host=vscode${commit ? `#commit=${enc(commit)}` : ''}`;
  if (!panel) {
    panel = vscode.window.createWebviewPanel('crossslice.explorer', 'CrossSlice', vscode.ViewColumn.Beside, {
      enableScripts: true,
      retainContextWhenHidden: true,
    });
    panel.onDidDispose(() => {
      panel = undefined;
      panelBase = undefined;
    });
    panel.webview.onDidReceiveMessage(onPanelMessage);
  }
  if (panelBase !== base) {
    panel.webview.html = webviewHtml(src, origin);
    panelBase = base;
  } else if (commit) {
    void panel.webview.postMessage({ type: 'crossslice:commit', rev: commit });
  }
  panel.reveal(vscode.ViewColumn.Beside, true);
  if (focus) void panel.webview.postMessage({ type: 'crossslice:expand', name: focus });
}

async function onPanelMessage(m: any) {
  if (!m || typeof m !== 'object' || !backend) return;
  if (m.type === 'crossslice:open' && m.file) {
    const file = path.join(backend.folder, String(m.file));
    const line = Math.max(1, Number(m.line) || 1);
    const doc = await vscode.workspace.openTextDocument(file);
    const pos = new vscode.Position(Math.min(line, doc.lineCount) - 1, 0);
    await vscode.window.showTextDocument(doc, {
      viewColumn: vscode.ViewColumn.One,
      selection: new vscode.Range(pos, pos),
      preserveFocus: false,
    });
  }
}

// ------------------------------------------------------------------ CodeLens

interface FunctionRow { name: string; line: number; end_line: number; kind: string }

class Lenses implements vscode.CodeLensProvider {
  onDidChangeCodeLenses = lensEmitter.event;
  private cache = new Map<string, { version: number; lenses: vscode.CodeLens[] }>();

  async provideCodeLenses(doc: vscode.TextDocument): Promise<vscode.CodeLens[]> {
    if (!setting('codeLens', true) || !backend || doc.uri.scheme !== 'file') return [];
    let rel: string;
    try {
      rel = relPath(backend, doc.uri.fsPath);
    } catch {
      return [];
    }
    const key = doc.uri.toString();
    const hit = this.cache.get(key);
    if (hit && hit.version === doc.version) return hit.lenses;
    try {
      const r = await getJson<{ functions: FunctionRow[] }>(`${backend.url}/api/functions?file=${enc(rel)}`, 10000);
      const lenses = r.functions.flatMap((f) => {
        const range = new vscode.Range(f.line - 1, 0, f.line - 1, 0);
        return [
          new vscode.CodeLens(range, { title: '$(graph) CrossSlice context', command: 'crossslice.contextAtCursor', arguments: [{ uri: doc.uri, line: f.line }] }),
          new vscode.CodeLens(range, { title: 'show in explorer', command: 'crossslice.showInExplorer', arguments: [f.name] }),
        ];
      });
      this.cache.set(key, { version: doc.version, lenses });
      return lenses;
    } catch {
      return [];
    }
  }
}

// ------------------------------------------------------------------ activation

export function activate(context: vscode.ExtensionContext) {
  log = vscode.window.createOutputChannel('CrossSlice');
  status = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Left, 50);
  status.command = 'crossslice.menu';
  updateStatus('off');

  const register = (id: string, fn: (...args: any[]) => Promise<void> | void) =>
    vscode.commands.registerCommand(id, async (...args: any[]) => {
      try {
        await fn(...args);
      } catch (e: any) {
        const msg = e?.message ?? String(e);
        log.appendLine(`[crossslice] ${msg}`);
        const choice = await vscode.window.showErrorMessage(`CrossSlice: ${msg}`, 'Show Log');
        if (choice) log.show();
      }
    });

  context.subscriptions.push(
    log,
    status,
    register('crossslice.menu', menu),
    register('crossslice.openExplorer', () => openExplorer()),
    register('crossslice.contextAtCursor', contextAtCursor),
    register('crossslice.showInExplorer', showInExplorer),
    register('crossslice.commitContext', commitContext),
    register('crossslice.addMcp', addMcpServer),
    register('crossslice.start', async () => {
      const b = await ensureBackend();
      void vscode.window.showInformationMessage(`CrossSlice backend running (${b.mode}) at ${b.url}`);
    }),
    register('crossslice.stop', stopBackend),
    register('crossslice.showLog', () => log.show()),
    vscode.workspace.registerTextDocumentContentProvider(SCHEME, {
      onDidChange: docEmitter.event,
      provideTextDocumentContent: (uri) => documents.get(uri.toString()) ?? '',
    }),
    vscode.languages.registerCodeLensProvider({ language: 'c', scheme: 'file' }, new Lenses()),
    vscode.workspace.onDidChangeConfiguration((e) => {
      if (e.affectsConfiguration('crossslice.codeLens')) lensEmitter.fire();
    }),
    vscode.workspace.onDidChangeWorkspaceFolders(() => void stopBackend()),
  );
  registerMcpProvider(context);
}

export function deactivate() {
  const b = backend;
  backend = undefined;
  if (!b) return;
  if (b.mode === 'docker' && b.containerName && b.dockerCmd) {
    cp.spawnSync(b.dockerCmd, ['stop', '-t', '5', b.containerName], { stdio: 'ignore' });
  }
  if (b.proc.exitCode === null) b.proc.kill('SIGTERM');
}
