<script setup>
import { computed, inject, ref } from 'vue'

const props = defineProps({
  detail: { type: Object, required: true },
  nodes: { type: Array, default: () => [] },
  edges: { type: Array, default: () => [] },
})
const emit = defineEmits(['close', 'select', 'expand'])
const openLocation = inject('openLocation', () => {})
const embedded = inject('embedded', false)
const locTitle = embedded ? 'Open in editor' : 'Copy file:line'

const me = computed(() => props.nodes.find((n) => n.id === props.detail.id))

function neighborList(direction) {
  if (!me.value) return []
  const byId = new Map(props.nodes.map((n) => [n.id, n]))
  const seen = new Set()
  const out = []
  for (const e of props.edges) {
    const other =
      direction === 'out'
        ? e.src === me.value.id && byId.get(e.dst)
        : e.dst === me.value.id && byId.get(e.src)
    if (other && !seen.has(other.id)) {
      seen.add(other.id)
      out.push(other)
    }
  }
  return out
}

const callees = computed(() => neighborList('out'))
const callers = computed(() => neighborList('in'))

const bodyMode = ref('sliced') // 'sliced' | 'full'
const bodyText = computed(() =>
  bodyMode.value === 'full' ? props.detail.body_full || props.detail.body : props.detail.body || props.detail.body_full,
)

const stateBadge = computed(() => {
  const s = props.detail.state
  if (s === 'analyzed') return 'bg-sky-950 text-sky-300 border-sky-800'
  if (s === 'stale') return 'bg-rose-950 text-rose-300 border-rose-800'
  return 'bg-slate-800 text-slate-300 border-slate-700'
})
</script>

<template>
  <aside
    class="z-10 flex w-96 shrink-0 flex-col overflow-hidden border-l border-slate-800 bg-slate-900"
  >
    <!-- header -->
    <div class="border-b border-slate-800 p-4">
      <div class="flex items-start justify-between gap-2">
        <h2 class="font-mono text-sm font-semibold break-all text-slate-100">
          {{ detail.name }}
        </h2>
        <button
          class="rounded p-0.5 text-slate-500 hover:bg-slate-800 hover:text-slate-200"
          @click="emit('close')"
        >
          <svg class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
            <path d="M6.3 6.3a1 1 0 011.4 0L10 8.6l2.3-2.3a1 1 0 111.4 1.4L11.4 10l2.3 2.3a1 1 0 01-1.4 1.4L10 11.4l-2.3 2.3a1 1 0 01-1.4-1.4L8.6 10 6.3 7.7a1 1 0 010-1.4z" />
          </svg>
        </button>
      </div>

      <p class="mt-1 font-mono text-[11px] break-all text-slate-400">
        <button class="hover:text-sky-300 hover:underline" :title="locTitle" @click="openLocation(detail.file, (detail.line ?? 0) + 1)">
          {{ detail.file }}:{{ (detail.line ?? 0) + 1 }}
        </button>
      </p>

      <div class="mt-2 flex flex-wrap gap-1.5 text-[10px]">
        <span class="rounded-full border px-2 py-0.5" :class="stateBadge">
          {{ detail.state }}
        </span>
        <span
          v-if="detail.kind && detail.kind !== 'function'"
          class="rounded-full border border-amber-800 bg-amber-950 px-2 py-0.5 text-amber-300"
        >
          {{ detail.kind }}
        </span>
        <span
          v-if="detail.resolution_method"
          class="rounded-full border border-slate-700 bg-slate-800 px-2 py-0.5 text-slate-400"
          title="How the definition was located (cascade tier)"
        >
          {{ detail.resolution_method }}
        </span>
      </div>

      <div class="mt-3 flex gap-2">
        <button
          class="flex-1 rounded-md bg-sky-600 px-2 py-1.5 text-xs font-medium text-white transition hover:bg-sky-500"
          @click="emit('expand', detail.id)"
        >
          Expand neighborhood
        </button>
      </div>
    </div>

    <!-- scrollable content -->
    <div class="min-h-0 flex-1 space-y-4 overflow-y-auto p-4">
      <section v-if="detail.summary">
        <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Effect summary
        </h3>
        <div class="flex flex-wrap gap-1">
          <span
            v-for="p in detail.summary.params_read || []"
            :key="'r' + p"
            class="rounded bg-sky-950 px-1.5 py-0.5 font-mono text-[11px] text-sky-300"
            >reads {{ p }}</span
          >
          <span
            v-for="p in detail.summary.params_written || []"
            :key="'w' + p"
            class="rounded bg-rose-950 px-1.5 py-0.5 font-mono text-[11px] text-rose-300"
            >writes {{ p }}</span
          >
          <span
            v-if="!(detail.summary.params_read || []).length && !(detail.summary.params_written || []).length"
            class="text-[11px] text-slate-500"
            >no parameter effects</span
          >
        </div>
        <div v-if="(detail.summary.returns || []).length" class="mt-2">
          <p
            v-for="(r, i) in detail.summary.returns.slice(0, 4)"
            :key="i"
            class="truncate font-mono text-[11px] text-slate-400"
          >
            {{ r }}
          </p>
        </div>
      </section>

      <section v-if="detail.signature">
        <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Signature
        </h3>
        <pre
          class="overflow-x-auto rounded-lg bg-slate-950 p-2.5 font-mono text-[11px] leading-relaxed whitespace-pre-wrap text-slate-300"
          >{{ detail.signature }}</pre
        >
      </section>

      <section v-if="detail.body || detail.body_full">
        <div class="mb-1.5 flex items-baseline justify-between">
          <h3 class="text-[11px] font-semibold tracking-wider text-slate-500 uppercase">Body</h3>
          <div class="flex rounded border border-slate-700 text-[10px]">
            <button
              class="px-1.5 py-0.5"
              :class="bodyMode === 'sliced' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-slate-200'"
              title="Only the statements connected to the parameters and return values (def-use slice)"
              @click="bodyMode = 'sliced'"
            >
              sliced
            </button>
            <button
              class="px-1.5 py-0.5"
              :class="bodyMode === 'full' ? 'bg-slate-700 text-white' : 'text-slate-400 hover:text-slate-200'"
              title="Every statement, control flow as headers"
              @click="bodyMode = 'full'"
            >
              full
            </button>
          </div>
        </div>
        <pre
          class="max-h-[45vh] overflow-auto rounded-lg bg-slate-950 p-2.5 font-mono text-[11px] leading-relaxed text-slate-300"
          >{{ bodyText }}</pre
        >
        <p v-if="bodyMode === 'sliced'" class="mt-1 text-[10px] text-slate-500">
          "..." marks statements left out because nothing flows from them to a parameter or a return value.
        </p>
      </section>
      <p v-else class="text-[11px] text-slate-500">
        Not analyzed yet — expand this node to slice its body.
      </p>

      <section v-if="detail.alternatives && detail.alternatives.length">
        <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Also defined at
        </h3>
        <p class="mb-1.5 text-[11px] text-slate-500">
          The name is ambiguous in this repository
          <template v-if="detail.resolution_method === 'priority_fallback'">
            and no call site disambiguated it; this definition was picked by path priority.
          </template>
          <template v-else-if="detail.resolution_method === 'lsp'">; clangd chose this definition from the call site.</template>
          <template v-else>.</template>
          Pick another one to explore it as its own node:
        </p>
        <ul class="space-y-0.5">
          <li v-for="(a, i) in detail.alternatives" :key="i">
            <button
              class="group flex w-full items-baseline gap-2 rounded px-1.5 py-1 text-left hover:bg-slate-800"
              @click="emit('expand', { name: detail.name, file: a.file, line: a.line + 1, kind: a.is_macro ? 'macro' : 'function' })"
            >
              <span class="font-mono text-[10px] text-slate-300 group-hover:underline">{{ a.file }}:{{ a.line + 1 }}</span>
              <span v-if="a.is_macro" class="rounded bg-amber-950 px-1 text-[10px] text-amber-300">macro</span>
            </button>
          </li>
        </ul>
      </section>

      <section v-if="callees.length">
        <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Calls ({{ callees.length }})
        </h3>
        <ul class="space-y-0.5">
          <li v-for="n in callees" :key="n.id">
            <button
              class="group flex w-full items-baseline gap-2 rounded px-1.5 py-1 text-left hover:bg-slate-800"
              @click="emit('select', n.id)"
              @dblclick="emit('expand', n.id)"
            >
              <span class="font-mono text-xs text-sky-300 group-hover:underline">{{ n.name }}</span>
              <span class="truncate font-mono text-[10px] text-slate-500 hover:text-slate-200" :title="locTitle" @click.stop="openLocation(n.file, n.line)">{{ n.file }}:{{ n.line }}</span>
            </button>
          </li>
        </ul>
      </section>

      <section v-if="callers.length">
        <h3 class="mb-1.5 text-[11px] font-semibold tracking-wider text-slate-500 uppercase">
          Called by ({{ callers.length }})
        </h3>
        <p v-if="detail.callers_truncated" class="mb-1.5 text-[11px] text-amber-300/80">
          Only the first {{ detail.callers_cap }} of {{ detail.callers_total }} reference sites were followed; the list is incomplete.
        </p>
        <ul class="space-y-0.5">
          <li v-for="n in callers" :key="n.id">
            <button
              class="group flex w-full items-baseline gap-2 rounded px-1.5 py-1 text-left hover:bg-slate-800"
              @click="emit('select', n.id)"
              @dblclick="emit('expand', n.id)"
            >
              <span class="font-mono text-xs text-emerald-300 group-hover:underline">{{ n.name }}</span>
              <span class="truncate font-mono text-[10px] text-slate-500 hover:text-slate-200" :title="locTitle" @click.stop="openLocation(n.file, n.line)">{{ n.file }}:{{ n.line }}</span>
            </button>
          </li>
        </ul>
      </section>
    </div>
  </aside>
</template>
