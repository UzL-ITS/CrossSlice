<script setup>
defineProps({ isGit: { type: Boolean, default: true } })
const emit = defineEmits(['close'])

const mouse = [
  ['click a node', 'details: sliced body, read/write summary, callers, callees'],
  ['double-click a node', 'expand one more ring (callers and callees); depth 2 expands two'],
  ['drag a node', 'move it; drag the background to pan; wheel to zoom'],
  ['click a location', 'open it in the editor (VS Code) or copy file:line'],
]
const keys = [
  ['/', 'search a function or macro'],
  ['Enter', 'in the search box: expand the first hit (or the typed name)'],
  ['e', 'expand the selected node'],
  ['f', 'fit the graph to the window'],
  ['c', 'show or hide the Commit tab'],
  ['Esc', 'close the panel on top (help, details, Commit tab)'],
  ['?', 'this help'],
]
const colors = [
  ['border-sky-400', '', 'analyzed: the body was sliced; details are complete'],
  ['border-slate-500', 'border-dashed', 'summarized: name, location and signature only; double-click to analyze'],
  ['border-amber-400', '', 'macro: shown with its #define'],
  ['border-rose-500', '', 'stale: the file changed on disk; expand again or press update'],
]
</script>

<template>
  <div class="absolute inset-0 z-40 flex items-center justify-center bg-slate-950/70 p-6" @click.self="emit('close')">
    <div class="max-h-full w-full max-w-2xl overflow-y-auto rounded-xl border border-slate-700 bg-slate-900 p-6 shadow-2xl">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-sm font-semibold text-slate-100">CrossSlice explorer</h2>
          <p class="mt-1 text-xs text-slate-400">
            The call graph grows on demand: only what you ask for is analyzed, one ring at a time.
            <template v-if="isGit"> The Commit tab shows a commit's change with its def-use slice and the code it depends on.</template>
          </p>
        </div>
        <button class="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-200" title="Close (Esc)" @click="emit('close')">
          <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6.3 6.3a1 1 0 011.4 0L10 8.6l2.3-2.3a1 1 0 111.4 1.4L11.4 10l2.3 2.3a1 1 0 01-1.4 1.4L10 11.4l-2.3 2.3a1 1 0 01-1.4-1.4L8.6 10 6.3 7.7a1 1 0 010-1.4z" />
          </svg>
        </button>
      </div>

      <div class="mt-5 grid gap-6 md:grid-cols-2">
        <section>
          <h3 class="mb-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">Mouse</h3>
          <dl class="space-y-1.5 text-xs">
            <div v-for="[k, v] in mouse" :key="k" class="flex gap-3">
              <dt class="w-36 shrink-0 text-slate-300">{{ k }}</dt>
              <dd class="text-slate-400">{{ v }}</dd>
            </div>
          </dl>
        </section>
        <section>
          <h3 class="mb-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">Keyboard</h3>
          <dl class="space-y-1.5 text-xs">
            <div v-for="[k, v] in keys" :key="k" class="flex gap-3">
              <dt class="w-36 shrink-0"><kbd>{{ k }}</kbd></dt>
              <dd class="text-slate-400">{{ v }}</dd>
            </div>
          </dl>
        </section>
        <section class="md:col-span-2">
          <h3 class="mb-2 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">Nodes</h3>
          <ul class="space-y-1.5 text-xs">
            <li v-for="[c, dash, v] in colors" :key="v" class="flex items-center gap-3">
              <span class="inline-block h-3 w-7 shrink-0 rounded-full border-2 bg-slate-800" :class="[c, dash]"></span>
              <span class="text-slate-400">{{ v }}</span>
            </li>
          </ul>
          <p class="mt-3 text-[11px] text-slate-500">
            Calls through function pointers are not followed; names without a definition in this repository
            (libc, other libraries) stay unresolved. Every result is cached, so the second visit is instant.
          </p>
        </section>
      </div>
    </div>
  </div>
</template>
