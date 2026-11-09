<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  forceCollide,
  forceLink,
  forceManyBody,
  forceSimulation,
  forceX,
  forceY,
} from 'd3-force'

const props = defineProps({
  nodes: { type: Array, default: () => [] },
  edges: { type: Array, default: () => [] },
  selected: { type: Number, default: null },
})
const emit = defineEmits(['select', 'expand'])

const container = ref(null)
const transform = ref({ x: 0, y: 0, k: 1 })
const frame = ref(0) // bumped every simulation tick to trigger re-render

let sim = null
const simNodes = [] // plain objects mutated by d3
const simLinks = []
const savedPos = new Map() // node id -> {x, y} kept across data updates

function nodeWidth(n) {
  return Math.max(n.name.length * 7 + 22, 46)
}

function rebuild() {
  const byId = new Map()
  const prev = new Map(simNodes.map((n) => [n.id, n]))
  simNodes.length = 0

  for (const raw of props.nodes) {
    const existing = prev.get(raw.id) || savedPos.get(raw.id)
    const n = {
      ...raw,
      x: existing ? existing.x : (Math.random() - 0.5) * 60,
      y: existing ? existing.y : (Math.random() - 0.5) * 60,
      vx: 0,
      vy: 0,
    }
    byId.set(n.id, n)
    simNodes.push(n)
  }

  // new nodes spawn near an already-placed neighbor instead of the center
  const placed = new Set(prev.keys())
  for (const e of props.edges) {
    const a = byId.get(e.src)
    const b = byId.get(e.dst)
    if (!a || !b) continue
    if (placed.has(a.id) && !placed.has(b.id)) {
      b.x = a.x + (Math.random() - 0.5) * 120
      b.y = a.y + 60 + Math.random() * 60
    } else if (placed.has(b.id) && !placed.has(a.id)) {
      a.x = b.x + (Math.random() - 0.5) * 120
      a.y = b.y - 60 - Math.random() * 60
    }
  }

  // dedupe parallel edges for layout + rendering
  simLinks.length = 0
  const seen = new Set()
  for (const e of props.edges) {
    const key = `${e.src}->${e.dst}`
    if (seen.has(key) || !byId.has(e.src) || !byId.has(e.dst)) continue
    seen.add(key)
    simLinks.push({ source: byId.get(e.src), target: byId.get(e.dst) })
  }

  if (!sim) {
    sim = forceSimulation(simNodes)
      .force('charge', forceManyBody().strength(-420).distanceMax(600))
      .force('x', forceX(0).strength(0.03))
      .force('y', forceY(0).strength(0.03))
      .on('tick', () => {
        for (const n of simNodes) savedPos.set(n.id, { x: n.x, y: n.y })
        frame.value++
      })
  } else {
    sim.nodes(simNodes)
  }
  sim
    .force('link', forceLink(simLinks).distance(130).strength(0.5))
    .force('collide', forceCollide().radius((n) => nodeWidth(n) / 2 + 14))
  const hasNew = simNodes.some((n) => !prev.has(n.id))
  sim.alpha(hasNew ? 0.9 : 0.25).restart()
  frame.value++
}

watch(() => [props.nodes, props.edges], rebuild, { deep: false })

// ---------------------------------------------------------------- rendering

// Fresh array each tick: a computed returning the same (mutated) array
// reference would never re-trigger Vue's renderer.
const renderNodes = computed(() => {
  frame.value // dependency: re-run every tick
  return [...simNodes]
})
const renderLinks = computed(() => {
  frame.value
  return [...simLinks]
})

function nodeClass(n) {
  if (n.state === 'stale') return 'stroke-rose-500'
  if (n.kind === 'macro') return 'stroke-amber-400'
  if (n.state === 'analyzed') return 'stroke-sky-400'
  return 'stroke-slate-500'
}

// shorten the visible edge so the arrowhead ends at the node border
function linkPath(l) {
  const dx = l.target.x - l.source.x
  const dy = l.target.y - l.source.y
  const dist = Math.hypot(dx, dy) || 1
  const pad = nodeWidth(l.target) / 2 + 8
  const t = Math.max((dist - pad) / dist, 0.1)
  return {
    x1: l.source.x,
    y1: l.source.y,
    x2: l.source.x + dx * t,
    y2: l.source.y + dy * t,
  }
}

// ---------------------------------------------------------- pan/zoom/drag

let pointer = null // { mode, id, startX, startY, moved, node }

function toWorld(clientX, clientY) {
  const rect = container.value.getBoundingClientRect()
  const t = transform.value
  return {
    x: (clientX - rect.left - t.x) / t.k,
    y: (clientY - rect.top - t.y) / t.k,
  }
}

function onWheel(ev) {
  ev.preventDefault()
  const rect = container.value.getBoundingClientRect()
  const mx = ev.clientX - rect.left
  const my = ev.clientY - rect.top
  const t = transform.value
  const k = Math.min(4, Math.max(0.12, t.k * Math.exp(-ev.deltaY * 0.0018)))
  transform.value = {
    k,
    x: mx - ((mx - t.x) / t.k) * k,
    y: my - ((my - t.y) / t.k) * k,
  }
}

function onBackgroundDown(ev) {
  pointer = {
    mode: 'pan',
    startX: ev.clientX,
    startY: ev.clientY,
    origin: { ...transform.value },
    moved: false,
  }
  ev.currentTarget.setPointerCapture(ev.pointerId)
}

function onNodeDown(ev, n) {
  ev.stopPropagation()
  pointer = { mode: 'drag', node: n, startX: ev.clientX, startY: ev.clientY, moved: false }
  n.fx = n.x
  n.fy = n.y
  container.value.setPointerCapture(ev.pointerId)
  sim?.alphaTarget(0.25).restart()
}

function onPointerMove(ev) {
  if (!pointer) return
  const dx = ev.clientX - pointer.startX
  const dy = ev.clientY - pointer.startY
  if (Math.hypot(dx, dy) > 4) pointer.moved = true
  if (pointer.mode === 'pan') {
    transform.value = {
      ...transform.value,
      x: pointer.origin.x + dx,
      y: pointer.origin.y + dy,
    }
  } else if (pointer.mode === 'drag') {
    const w = toWorld(ev.clientX, ev.clientY)
    pointer.node.fx = w.x
    pointer.node.fy = w.y
  }
}

function onPointerUp(ev) {
  if (!pointer) return
  if (pointer.mode === 'drag') {
    sim?.alphaTarget(0)
    pointer.node.fx = null
    pointer.node.fy = null
    if (!pointer.moved) emit('select', pointer.node.id)
  }
  pointer = null
}

function fit() {
  if (!simNodes.length) return
  const xs = simNodes.map((n) => n.x)
  const ys = simNodes.map((n) => n.y)
  const minX = Math.min(...xs) - 80
  const maxX = Math.max(...xs) + 80
  const minY = Math.min(...ys) - 60
  const maxY = Math.max(...ys) + 60
  const rect = container.value.getBoundingClientRect()
  const k = Math.min(rect.width / (maxX - minX), rect.height / (maxY - minY), 1.4)
  transform.value = {
    k,
    x: rect.width / 2 - ((minX + maxX) / 2) * k,
    y: rect.height / 2 - ((minY + maxY) / 2) * k,
  }
}

defineExpose({ fit })

onMounted(() => {
  const rect = container.value.getBoundingClientRect()
  transform.value = { x: rect.width / 2, y: rect.height / 2, k: 1 }
  rebuild()
  // fit once the initial layout has roughly settled
  setTimeout(fit, 700)
})

onBeforeUnmount(() => sim?.stop())
</script>

<template>
  <div
    ref="container"
    class="relative h-full touch-none overflow-hidden bg-slate-950 select-none"
    @wheel="onWheel"
    @pointerdown="onBackgroundDown"
    @pointermove="onPointerMove"
    @pointerup="onPointerUp"
    @pointercancel="onPointerUp"
  >
    <svg class="h-full w-full cursor-grab active:cursor-grabbing">
      <defs>
        <marker
          id="arrow"
          viewBox="0 0 10 10"
          refX="9"
          refY="5"
          markerWidth="7"
          markerHeight="7"
          orient="auto-start-reverse"
        >
          <path d="M 0 1 L 9 5 L 0 9 z" class="fill-slate-500" />
        </marker>
        <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
          <circle cx="1" cy="1" r="1" class="fill-slate-800" />
        </pattern>
      </defs>

      <rect width="100%" height="100%" fill="url(#dots)" />

      <g :transform="`translate(${transform.x},${transform.y}) scale(${transform.k})`">
        <line
          v-for="(l, i) in renderLinks"
          :key="i"
          v-bind="linkPath(l)"
          class="stroke-slate-600"
          stroke-width="1.4"
          stroke-opacity="0.75"
          marker-end="url(#arrow)"
        />

        <g
          v-for="n in renderNodes"
          :key="n.id"
          :transform="`translate(${n.x},${n.y})`"
          class="cursor-pointer"
          @pointerdown="onNodeDown($event, n)"
          @dblclick.stop="emit('expand', n.id)"
        >
          <rect
            :x="-nodeWidth(n) / 2"
            y="-13"
            :width="nodeWidth(n)"
            height="26"
            rx="13"
            class="fill-slate-800 transition-[stroke-width]"
            :class="nodeClass(n)"
            :stroke-width="n.id === selected ? 3 : 1.6"
            :stroke-dasharray="n.state === 'summarized' ? '5 3' : undefined"
          />
          <rect
            v-if="n.id === selected"
            :x="-nodeWidth(n) / 2 - 4"
            y="-17"
            :width="nodeWidth(n) + 8"
            height="34"
            rx="17"
            class="fill-none stroke-emerald-400/60"
            stroke-width="1.5"
          />
          <text
            text-anchor="middle"
            dominant-baseline="central"
            class="pointer-events-none fill-slate-100 font-mono"
            font-size="11"
          >
            {{ n.name }}
          </text>
        </g>
      </g>
    </svg>

    <!-- controls -->
    <div class="absolute right-3 bottom-3 flex flex-col gap-1.5">
      <button
        class="flex items-center gap-1 rounded-md border border-slate-700 bg-slate-900/90 px-2 py-1 text-xs text-slate-300 hover:border-slate-500 hover:text-white"
        title="Fit graph to view"
        @click="fit"
      >
        <svg class="h-3 w-3" viewBox="0 0 20 20" fill="currentColor">
          <path d="M3 3h5v2H5v3H3V3zm14 0h-5v2h3v3h2V3zM3 17h5v-2H5v-3H3v5zm14 0h-5v-2h3v-3h2v5z" />
        </svg>
        fit
      </button>
    </div>

  </div>
</template>
