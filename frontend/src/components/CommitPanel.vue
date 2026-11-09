<script setup>
import { computed, inject, onMounted, ref, watch } from 'vue'
import { api } from '../api'
import CodeBlock from './CodeBlock.vue'

const props = defineProps({
  isGit: { type: Boolean, default: true },
  initialRev: { type: String, default: '' }, // e.g. from the #commit=REV deep link
})
const emit = defineEmits(['close', 'focus', 'error'])
const openLocation = inject('openLocation', () => {})
const embedded = inject('embedded', false)
const locTitle = embedded ? 'Open in editor' : 'Copy file:line'

const commits = ref([])
const rev = ref('')
const revInput = ref('')
const data = ref(null)
const loading = ref(false)
const showDiff = ref(false)
const copied = ref(false)
const open = ref({ change: true, callee: true, macro: false, caller: true, ring2: false })

async function loadCommits() {
  if (!props.isGit) return
  try {
    const r = await api.commits(40)
    commits.value = r.commits
    if (!rev.value && props.initialRev) pick(props.initialRev)
    else if (!rev.value && r.commits.length) pick(r.commits[0].sha)
  } catch (err) {
    emit('error', err)
  }
}

async function pick(r) {
  if (!r) return
  rev.value = r
  loading.value = true
  data.value = null
  showDiff.value = false
  try {
    data.value = await api.commit(r)
    revInput.value = ''
  } catch (err) {
    emit('error', err)
  } finally {
    loading.value = false
  }
}

const groups = computed(() => {
  const s = data.value?.sections || []
  return {
    change: s.filter((x) => x.kind === 'change'),
    callee: s.filter((x) => x.kind === 'callee'),
    macro: s.filter((x) => x.kind === 'macro'),
    caller: s.filter((x) => x.kind === 'caller'),
    ring2: s.filter((x) => x.kind === 'ring2'),
  }
})

const GROUPS = [
  { key: 'change', title: 'Change and its def-use slice', hint: 'the diff merged with every statement that defines or uses a variable the change touches' },
  { key: 'callee', title: 'Called functions', hint: 'callees of the changed code, sliced to what the call sites pass in' },
  { key: 'macro', title: 'Macros', hint: 'macros the changed code uses, as their #define' },
  { key: 'caller', title: 'Callers of changed functions', hint: '> marks the call site' },
  { key: 'ring2', title: 'Second-level summaries', hint: 'what the callees call, as one-line summaries' },
]

async function copyText() {
  try {
    await navigator.clipboard.writeText(data.value?.text || '')
    copied.value = true
    setTimeout(() => (copied.value = false), 1500)
  } catch (err) {
    emit('error', err)
  }
}

function focusSection(s) {
  if (s.kind === 'callee' || s.kind === 'macro')
    emit('focus', { name: s.name, file: s.file, line: s.line, kind: s.kind === 'macro' ? 'macro' : 'function' })
  else if (s.kind === 'caller') emit('focus', s.name)
}

watch(() => props.isGit, loadCommits)
watch(() => props.initialRev, (r) => r && r !== rev.value && pick(r))
onMounted(loadCommits)
</script>

<template>
  <aside class="z-10 flex w-[30rem] shrink-0 flex-col overflow-hidden border-r border-slate-800 bg-slate-900">
    <!-- header: commit picker -->
    <div class="border-b border-slate-800 p-3">
      <div class="flex items-center justify-between">
        <h2 class="text-xs font-semibold tracking-wider text-slate-400 uppercase">Commit context</h2>
        <button
          class="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-200"
          title="Close (Esc)"
          @click="emit('close')"
        >
          <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6.3 6.3a1 1 0 011.4 0L10 8.6l2.3-2.3a1 1 0 111.4 1.4L11.4 10l2.3 2.3a1 1 0 01-1.4 1.4L10 11.4l-2.3 2.3a1 1 0 01-1.4-1.4L8.6 10 6.3 7.7a1 1 0 010-1.4z" />
          </svg>
        </button>
      </div>

      <div v-if="!isGit" class="mt-3 rounded-md border border-amber-900 bg-amber-950/50 p-3 text-xs text-amber-200">
        This directory is not a git repository, so there are no commits to show. The graph,
        search and code context work as usual.
      </div>

      <template v-else>
        <select
          class="mt-2 w-full rounded-md border border-slate-700 bg-slate-800 px-2 py-1.5 text-xs text-slate-200 focus:border-sky-600 focus:outline-none"
          :value="rev"
          :disabled="loading"
          @change="pick($event.target.value)"
        >
          <option v-if="rev && !commits.find((c) => c.sha === rev)" :value="rev">{{ rev }}</option>
          <option v-for="c in commits" :key="c.sha" :value="c.sha">
            {{ c.short }} · {{ c.subject.slice(0, 60) }}{{ c.merge ? ' (merge)' : '' }} · {{ c.when }}
          </option>
        </select>
        <form class="mt-2 flex gap-2" @submit.prevent="pick(revInput.trim())">
          <input
            v-model="revInput"
            placeholder="any revision: HEAD~3, v1.2.13, a1b2c3d"
            class="min-w-0 flex-1 rounded-md border border-slate-700 bg-slate-800 px-2 py-1 font-mono text-xs text-slate-200 placeholder:text-slate-500 focus:border-sky-600 focus:outline-none"
          />
          <button
            class="rounded-md border border-slate-700 bg-slate-800 px-2.5 py-1 text-xs text-slate-300 hover:border-slate-500 hover:text-white disabled:opacity-40"
            :disabled="loading || !revInput.trim()"
          >
            Analyze
          </button>
        </form>
        <p v-if="!commits.length && !loading" class="mt-2 text-[11px] text-slate-500">
          No commits that change .c or .h files yet.
        </p>
      </template>
    </div>

    <!-- body -->
    <div class="min-h-0 flex-1 space-y-4 overflow-y-auto p-3">
      <div v-if="loading" class="flex items-start gap-3 rounded-md border border-slate-800 bg-slate-950 p-4">
        <svg class="mt-0.5 h-4 w-4 shrink-0 animate-spin text-sky-400" viewBox="0 0 24 24" fill="none">
          <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
          <path class="opacity-90" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
        </svg>
        <div class="text-xs text-slate-400">
          <p class="text-slate-300">Analyzing {{ rev.slice(0, 12) }} …</p>
          <p class="mt-1">
            AST diff, def-use slice, then callees, callers and macros in both versions. Seconds on
            small projects, up to a minute on large ones; the result is cached.
          </p>
        </div>
      </div>

      <template v-if="data && !loading">
        <!-- commit header -->
        <div>
          <p class="text-sm font-medium text-slate-100">{{ data.subject }}</p>
          <p class="mt-1 font-mono text-[11px] text-slate-500">
            {{ data.sha.slice(0, 12) }} · {{ data.author }} · {{ data.when }} · parent
            {{ data.parent.slice(0, 12) }}
          </p>
          <div class="mt-2 flex flex-wrap items-center gap-2">
            <button
              class="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-300 hover:border-slate-500 hover:text-white"
              title="Copy the whole commit context, e.g. to paste into an LLM prompt"
              :disabled="!data.text"
              @click="copyText"
            >
              {{ copied ? 'Copied' : 'Copy as text' }}
            </button>
            <button
              class="rounded-md border border-slate-700 bg-slate-800 px-2 py-1 text-[11px] text-slate-300 hover:border-slate-500 hover:text-white"
              :disabled="!data.diff"
              @click="showDiff = !showDiff"
            >
              {{ showDiff ? 'Hide' : 'Show' }} raw diff
            </button>
            <span class="text-[11px] text-slate-500">{{ data.seconds }} s</span>
          </div>
        </div>

        <div v-if="data.note" class="rounded-md border border-slate-800 bg-slate-950 p-3 text-xs text-slate-400">
          {{ data.note === 'no C files changed' ? 'This commit changes no .c or .h files.' : data.note }}
        </div>
        <div v-if="data.cross_error" class="rounded-md border border-amber-900 bg-amber-950/50 p-3 text-xs text-amber-200">
          The cross-function step failed ({{ data.cross_error }}); showing the intra-procedural result.
        </div>

        <!-- changed functions -->
        <section v-if="data.functions.length">
          <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
            Changed functions
          </h3>
          <div class="flex flex-wrap gap-1.5">
            <button
              v-for="f in data.functions"
              :key="f"
              class="rounded-md border border-sky-900 bg-sky-950 px-2 py-0.5 font-mono text-[11px] text-sky-300 hover:border-sky-600 hover:text-sky-100"
              title="Show in the graph"
              @click="emit('focus', f)"
            >
              {{ f }}
            </button>
          </div>
          <p class="mt-1.5 text-[11px] text-slate-500">
            {{ data.files.length }} file{{ data.files.length === 1 ? '' : 's' }}: {{ data.files.join(', ') }}
          </p>
        </section>

        <section v-if="showDiff">
          <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">Raw diff</h3>
          <CodeBlock :text="data.diff" diff />
        </section>

        <!-- sections -->
        <template v-for="g in GROUPS" :key="g.key">
          <section v-if="groups[g.key].length">
            <button class="group flex w-full items-baseline gap-2 text-left" @click="open[g.key] = !open[g.key]">
              <span class="text-[10px] text-slate-500">{{ open[g.key] ? '▾' : '▸' }}</span>
              <h3 class="text-[11px] font-semibold tracking-wider text-slate-400 uppercase group-hover:text-slate-200">
                {{ g.title }}
              </h3>
              <span class="text-[11px] text-slate-600">{{ groups[g.key].length }}</span>
            </button>
            <p v-if="open[g.key]" class="mt-0.5 mb-2 pl-4 text-[11px] text-slate-500">{{ g.hint }}</p>
            <div v-if="open[g.key]" class="space-y-3">
              <div v-for="(s, i) in groups[g.key]" :key="i">
                <div v-if="s.kind !== 'ring2'" class="mb-1 flex items-baseline justify-between gap-2">
                  <p class="min-w-0 truncate font-mono text-[11px]">
                    <template v-if="s.kind === 'change'">
                      <button class="text-slate-200 hover:underline" :title="locTitle" @click="openLocation(s.file, 1)">{{ s.title }}</button>
                    </template>
                    <template v-else>
                      <span v-if="s.kind === 'caller'" class="text-slate-500">{{ s.of }} ← </span>
                      <button class="text-sky-300 hover:underline" title="Show in the graph" @click="focusSection(s)">
                        {{ s.name }}
                      </button>
                      <button class="text-slate-500 hover:text-slate-200" :title="locTitle" @click="openLocation(s.file, s.line)"> {{ s.file }}:{{ s.line }}</button>
                    </template>
                  </p>
                  <span v-if="s.version" class="shrink-0 rounded-full border border-violet-900 bg-violet-950 px-1.5 text-[10px] text-violet-300">
                    {{ s.version }} only
                  </span>
                  <span v-else-if="s.method" class="shrink-0 text-[10px] text-slate-600" title="How the definition was located">
                    {{ s.method }}
                  </span>
                </div>
                <CodeBlock :text="s.body" />
              </div>
            </div>
          </section>
        </template>
      </template>
    </div>
  </aside>
</template>
