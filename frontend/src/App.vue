<script setup>
import { computed, onBeforeUnmount, onMounted, provide, ref, watch } from 'vue'
import { api } from './api'
import GraphView from './components/GraphView.vue'
import DetailPanel from './components/DetailPanel.vue'
import SearchBox from './components/SearchBox.vue'
import CommitPanel from './components/CommitPanel.vue'
import HelpOverlay from './components/HelpOverlay.vue'

const graph = ref({ nodes: [], edges: [], stats: null, focus: null })
const detail = ref(null)
const selected = ref(null)
const levels = ref(1)
const busy = ref(0)
const busyLabel = ref('')
const helpOpen = ref(false)
const graphView = ref(null)
const searchBox = ref(null)

// deep links: #focus=NAME expands a function; #commit or #commit=REV opens the Commit tab
const hash = decodeURIComponent(window.location.hash || '')
const commitOpen = ref(hash.startsWith('#commit'))
const commitRev = ref(hash.startsWith('#commit=') ? hash.slice('#commit='.length) : '')
const focusName = hash.startsWith('#focus=') ? hash.slice('#focus='.length) : ''

const isGit = computed(() => graph.value.meta?.is_git !== false)

const toast = ref(null) // { text, kind: 'error' | 'info' }
let toastTimer = null
function showToast(text, kind = 'error') {
  toast.value = { text: String(text), kind }
  clearTimeout(toastTimer)
  toastTimer = setTimeout(() => (toast.value = null), kind === 'error' ? 6000 : 2000)
}
function showError(err) {
  showToast(err?.message || err, 'error')
}

// Inside the VS Code extension the UI runs in a webview iframe (?host=vscode):
// locations are sent to the editor; in a browser they are copied as file:line.
const embedded = new URLSearchParams(window.location.search).get('host') === 'vscode'
async function openLocation(file, line) {
  if (embedded) {
    window.parent.postMessage({ type: 'crossslice:open', file, line: line || 1 }, '*')
    return
  }
  try {
    await navigator.clipboard.writeText(`${file}:${line || 1}`)
    showToast(`Copied ${file}:${line || 1}`, 'info')
  } catch (err) {
    showError(err)
  }
}
provide('openLocation', openLocation)
provide('embedded', embedded)

async function run(fn, label = '') {
  busy.value++
  if (label) busyLabel.value = label
  try {
    return await fn()
  } catch (err) {
    showError(err)
  } finally {
    busy.value--
    if (!busy.value) busyLabel.value = ''
  }
}

async function refresh() {
  const s = await run(api.state, 'loading')
  if (s) graph.value = s
}

function nodeName(id) {
  return graph.value.nodes.find((n) => n.id === id)?.name
}

async function select(id) {
  selected.value = id
  const d = await run(() => api.node({ id }), `loading ${nodeName(id) || 'details'}`)
  if (d) detail.value = d
}

// target: a node id (number), a bare name (string), or { name, file, line, kind }
async function expand(target, lv) {
  const body =
    typeof target === 'number' ? { id: target } : typeof target === 'string' ? { name: target } : { ...target }
  body.levels = lv ?? levels.value
  const label = typeof target === 'number' ? nodeName(target) : target?.name || target
  const s = await run(() => api.expand(body), `expanding ${label || 'node'}`)
  if (s) {
    graph.value = s
    if (s.focus_id != null) await select(s.focus_id)
  }
}

async function updateGraph() {
  const s = await run(api.update, 'updating')
  if (s) {
    graph.value = s
    if (selected.value) await select(selected.value)
  }
}

const stats = computed(() => {
  const st = graph.value.stats
  if (!st) return ''
  const n = Object.values(st.nodes || {}).reduce((a, b) => a + b, 0)
  if (!n) return ''
  return `${n} node${n === 1 ? '' : 's'} · ${st.edges} edge${st.edges === 1 ? '' : 's'}`
})

function closeTopmost() {
  if (helpOpen.value) helpOpen.value = false
  else if (detail.value) {
    detail.value = null
    selected.value = null
  } else if (commitOpen.value) commitOpen.value = false
}

function onKey(e) {
  const t = e.target
  const typing =
    t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'SELECT' || t.isContentEditable)
  if (e.key === 'Escape') {
    if (typing) t.blur()
    else closeTopmost()
    return
  }
  if (typing || e.ctrlKey || e.metaKey || e.altKey) return
  if (e.key === '/') {
    e.preventDefault()
    searchBox.value?.focus()
  } else if (e.key === '?') {
    e.preventDefault()
    helpOpen.value = !helpOpen.value
  } else if (e.key === 'f') graphView.value?.fit()
  else if (e.key === 'e' && selected.value != null) expand(selected.value)
  else if (e.key === 'c' && isGit.value) commitOpen.value = !commitOpen.value
}

// the graph area changes width when the Commit tab opens or closes: re-frame it
watch(commitOpen, () => setTimeout(() => graphView.value?.fit(), 350))

// messages from the host (the VS Code extension): expand a function, show a commit
function onMessage(e) {
  const m = e.data
  if (!m || typeof m !== 'object') return
  if (m.type === 'crossslice:expand' && m.name) expand(m.name)
  else if (m.type === 'crossslice:commit') {
    commitOpen.value = true
    commitRev.value = m.rev || 'HEAD'
  }
}

onMounted(async () => {
  window.addEventListener('keydown', onKey)
  window.addEventListener('message', onMessage)
  await refresh()
  if (focusName) await expand(focusName)
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKey)
  window.removeEventListener('message', onMessage)
})
</script>

<template>
  <div class="flex h-full flex-col bg-slate-950 text-slate-200">
    <!-- top bar -->
    <header
      class="z-20 flex h-14 shrink-0 items-center gap-4 border-b border-slate-800 bg-slate-900/80 px-4 backdrop-blur"
    >
      <div class="flex items-baseline gap-2">
        <h1 class="text-sm font-semibold tracking-wide text-slate-100">CrossSlice</h1>
        <span v-if="graph.meta?.repo" class="hidden font-mono text-xs text-slate-400 md:inline">
          {{ graph.meta.repo }}<template v-if="graph.meta.commit">@{{ graph.meta.commit.slice(0, 10) }}</template>
        </span>
      </div>

      <div class="flex rounded-md border border-slate-700 bg-slate-800 p-0.5 text-xs">
        <button
          class="rounded px-2.5 py-1 transition"
          :class="!commitOpen ? 'bg-slate-600 text-white' : 'text-slate-400 hover:text-slate-200'"
          title="Call graph only"
          @click="commitOpen = false"
        >
          Graph
        </button>
        <button
          class="rounded px-2.5 py-1 transition"
          :class="commitOpen ? 'bg-slate-600 text-white' : 'text-slate-400 hover:text-slate-200'"
          :title="isGit ? 'Commit context of recent commits (c)' : 'Not a git repository'"
          @click="commitOpen = true"
        >
          Commit
        </button>
      </div>

      <SearchBox ref="searchBox" class="max-w-md flex-1" @pick="(hit) => expand(hit)" />

      <label class="flex items-center gap-1.5 text-xs text-slate-400" title="Rings to expand per double-click">
        depth
        <select
          v-model.number="levels"
          class="rounded-md border border-slate-700 bg-slate-800 px-1.5 py-1 text-xs text-slate-200 focus:outline-none"
        >
          <option :value="1">1</option>
          <option :value="2">2</option>
        </select>
      </label>

      <button
        class="rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1.5 text-xs text-slate-300 transition hover:border-slate-500 hover:text-white"
        title="Re-sync with the repository after you pull or edit (incremental)"
        @click="updateGraph"
      >
        ↻ update
      </button>

      <button
        class="rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1.5 text-xs text-slate-300 transition hover:border-slate-500 hover:text-white"
        title="Help and keyboard shortcuts (?)"
        @click="helpOpen = !helpOpen"
      >
        ?
      </button>

      <div class="flex min-w-5 items-center gap-2 text-xs text-slate-400">
        <svg v-if="busy" class="h-4 w-4 shrink-0 animate-spin text-sky-400" viewBox="0 0 24 24" fill="none">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-90" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
        <span v-if="busy" class="hidden truncate lg:inline">{{ busyLabel }}…</span>
      </div>
    </header>

    <!-- main area -->
    <div class="relative flex min-h-0 flex-1">
      <CommitPanel
        v-if="commitOpen"
        :is-git="isGit"
        :initial-rev="commitRev"
        @close="commitOpen = false"
        @focus="(target) => expand(target)"
        @error="showError"
      />

      <GraphView
        ref="graphView"
        class="min-w-0 flex-1"
        :nodes="graph.nodes"
        :edges="graph.edges"
        :selected="selected"
        @select="select"
        @expand="(id) => expand(id)"
      />

      <DetailPanel
        v-if="detail"
        :detail="detail"
        :nodes="graph.nodes"
        :edges="graph.edges"
        @close="detail = null; selected = null"
        @select="select"
        @expand="(target) => expand(target)"
      />

      <!-- empty state / onboarding -->
      <div
        v-if="!graph.nodes.length && !busy"
        class="pointer-events-none absolute inset-0 flex items-center justify-center"
      >
        <div class="max-w-md rounded-xl border border-slate-800 bg-slate-900/90 px-8 py-6">
          <p class="text-sm font-medium text-slate-100">Start with a function.</p>
          <ol class="mt-3 list-decimal space-y-2 pl-5 text-xs text-slate-400">
            <li>Press <kbd>/</kbd>, type a function or macro name and press Enter.</li>
            <li>Click a node for its sliced body, read/write summary, callers and callees.</li>
            <li>Double-click a node (or press <kbd>e</kbd>) to expand one more ring of the call graph.</li>
            <li v-if="isGit">The <span class="text-slate-200">Commit</span> tab shows what a commit changes and what that code depends on.</li>
          </ol>
          <p class="mt-3 text-[11px] text-slate-500">Press <kbd>?</kbd> for all shortcuts.</p>
        </div>
      </div>
    </div>

    <!-- footer: legend, counts, hints -->
    <footer
      class="flex h-8 shrink-0 items-center gap-4 border-t border-slate-800 bg-slate-900/80 px-4 text-[11px] text-slate-400"
    >
      <span class="flex items-center gap-1.5" title="Analyzed: sliced body and summary available">
        <span class="inline-block h-2.5 w-5 rounded-full border-2 border-sky-400 bg-slate-800"></span>analyzed
      </span>
      <span class="flex items-center gap-1.5" title="Summarized: known, not expanded yet (double-click)">
        <span class="inline-block h-2.5 w-5 rounded-full border-2 border-dashed border-slate-500 bg-slate-800"></span>summarized
      </span>
      <span class="flex items-center gap-1.5">
        <span class="inline-block h-2.5 w-5 rounded-full border-2 border-amber-400 bg-slate-800"></span>macro
      </span>
      <span class="text-slate-600">·</span>
      <span class="font-mono">{{ stats || 'empty graph' }}</span>
      <span class="ml-auto hidden text-slate-500 md:inline">
        click = details · double-click = expand · wheel = zoom · <kbd>?</kbd> shortcuts
      </span>
    </footer>

    <HelpOverlay v-if="helpOpen" :is-git="isGit" @close="helpOpen = false" />

    <!-- toast -->
    <transition
      enter-active-class="transition duration-150"
      enter-from-class="translate-y-2 opacity-0"
      leave-active-class="transition duration-300"
      leave-to-class="opacity-0"
    >
      <div
        v-if="toast"
        class="absolute bottom-12 left-1/2 z-50 -translate-x-1/2 rounded-lg border px-4 py-2 text-xs shadow-lg"
        :class="toast.kind === 'error' ? 'border-rose-800 bg-rose-950/95 text-rose-200' : 'border-emerald-800 bg-emerald-950/95 text-emerald-200'"
      >
        {{ toast.text }}
      </div>
    </transition>
  </div>
</template>
