<script setup>
import { ref, watch } from 'vue'
import { api } from '../api'

const emit = defineEmits(['pick'])

const input = ref(null)
const query = ref('')
const results = ref(null) // null = closed; { hits, suggestions }
const searching = ref(false)
let timer = null

watch(query, (q) => {
  clearTimeout(timer)
  if (q.trim().length < 2) {
    results.value = null
    return
  }
  timer = setTimeout(doSearch, 250)
})

async function doSearch() {
  const q = query.value.trim()
  if (q.length < 2) return
  searching.value = true
  try {
    results.value = await api.search(q)
  } catch (err) {
    results.value = { hits: [], suggestions: [], error: err.message }
  } finally {
    searching.value = false
  }
}

function pick(hit) {
  emit('pick', hit)
  results.value = null
  query.value = ''
  input.value?.blur()
}

function onEnter() {
  if (results.value?.hits?.length) pick(results.value.hits[0])
  else if (query.value.trim()) pick({ name: query.value.trim() })
}

function close() {
  results.value = null
  input.value?.blur()
}

defineExpose({
  focus() {
    input.value?.focus()
    input.value?.select()
  },
})
</script>

<template>
  <div class="relative">
    <div class="relative">
      <svg
        class="pointer-events-none absolute top-1/2 left-2.5 h-3.5 w-3.5 -translate-y-1/2 text-slate-500"
        viewBox="0 0 20 20"
        fill="currentColor"
      >
        <path
          fill-rule="evenodd"
          d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.45 4.4l3.07 3.08a1 1 0 01-1.41 1.41l-3.08-3.07A7 7 0 012 9z"
          clip-rule="evenodd"
        />
      </svg>
      <input
        ref="input"
        v-model="query"
        type="text"
        placeholder="Search a function or macro…  ( / )"
        spellcheck="false"
        class="w-full rounded-lg border border-slate-700 bg-slate-800 py-1.5 pr-3 pl-8 font-mono text-xs text-slate-200 placeholder:font-sans placeholder:text-slate-500 focus:border-sky-600 focus:outline-none"
        @keydown.enter="onEnter"
        @keydown.escape.stop="close"
        @focus="query.trim().length >= 2 && doSearch()"
      />
    </div>

    <div
      v-if="results !== null"
      class="absolute top-full right-0 left-0 z-30 mt-1 max-h-80 overflow-y-auto rounded-lg border border-slate-700 bg-slate-800 shadow-xl"
    >
      <p v-if="searching" class="px-3 py-2 text-xs text-slate-400">searching…</p>
      <template v-else-if="!results.hits.length">
        <p class="px-3 py-2 text-xs text-slate-400">
          <span v-if="results.error" class="text-rose-300">{{ results.error }}</span>
          <template v-else>No definition named <span class="font-mono text-slate-200">{{ query.trim() }}</span> in this repository.</template>
        </p>
        <template v-if="results.suggestions?.length">
          <p class="border-t border-slate-700/50 px-3 pt-2 pb-1 text-[10px] tracking-wider text-slate-500 uppercase">Similar names</p>
          <button
            v-for="s in results.suggestions"
            :key="s"
            class="block w-full px-3 py-1.5 text-left font-mono text-xs text-sky-300 hover:bg-slate-700/60"
            @click="pick({ name: s })"
          >
            {{ s }}
          </button>
        </template>
      </template>
      <button
        v-for="(r, i) in results.hits"
        v-else
        :key="i"
        class="block w-full border-b border-slate-700/50 px-3 py-2 text-left last:border-0 hover:bg-slate-700/60"
        @click="pick(r)"
      >
        <div class="flex items-baseline justify-between gap-2">
          <span class="font-mono text-xs text-sky-300">{{ r.name }}</span>
          <span class="shrink-0 font-mono text-[10px] text-slate-500"><span v-if="r.kind === 'macro'" class="mr-1 rounded bg-amber-950 px-1 text-amber-300">macro</span>{{ r.file }}:{{ r.line }}</span>
        </div>
        <p class="mt-0.5 truncate font-mono text-[10px] text-slate-400">{{ r.code }}</p>
      </button>
    </div>
  </div>
</template>
