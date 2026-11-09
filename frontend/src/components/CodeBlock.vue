<script setup>
import { computed } from 'vue'

// Renders enriched-context text: '+' / '-' lines of a merged diff, '>' marked
// call sites, '...' elisions and '[reads: ...]' summary lines get their own color.
const props = defineProps({
  text: { type: String, default: '' },
  diff: { type: Boolean, default: false }, // unified diff (headers, @@ hunks)
})

const lines = computed(() =>
  (props.text || '').split('\n').map((t) => {
    let cls = 'text-slate-300'
    if (props.diff && /^(diff --git|index |--- |\+\+\+ )/.test(t)) cls = 'text-slate-500'
    else if (props.diff && t.startsWith('@@')) cls = 'text-violet-300'
    else if (t.startsWith('+')) cls = 'bg-emerald-950/60 text-emerald-300'
    else if (t.startsWith('-')) cls = 'bg-rose-950/60 text-rose-300'
    else if (t.startsWith('>')) cls = 'bg-amber-950/60 text-amber-200'
    else if (/^\s*\.\.\.\s*$/.test(t)) cls = 'text-slate-600'
    else if (/^\s*\[reads:/.test(t) || /^\s*reads:/.test(t)) cls = 'text-sky-400/80 italic'
    return { t: t || ' ', cls }
  }),
)
</script>

<template>
  <pre
    class="overflow-x-auto rounded-md border border-slate-800 bg-slate-950 py-1.5 font-mono text-[11px] leading-[1.45]"
  ><div v-for="(l, i) in lines" :key="i" class="px-2 whitespace-pre" :class="l.cls">{{ l.t }}</div></pre>
</template>
