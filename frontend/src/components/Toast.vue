<template>
  <Teleport to="body">
    <TransitionGroup name="toast" tag="div" class="fixed top-5 right-5 z-[100] flex flex-col gap-3 pointer-events-none">
      <div v-for="t in toasts" :key="t.id"
        :class="['pointer-events-auto flex items-start gap-3 px-5 py-3.5 rounded-xl shadow-2xl border backdrop-blur-xl min-w-[300px] max-w-[420px] transition-all',
          t.type === 'success' ? 'bg-emerald-900/80 border-emerald-700/50 text-emerald-200' :
          t.type === 'error' ? 'bg-red-900/80 border-red-700/50 text-red-200' :
          'bg-slate-800/80 border-slate-700/50 text-slate-200']">
        <!-- Icon -->
        <div class="flex-shrink-0 mt-0.5">
          <svg v-if="t.type === 'success'" class="w-5 h-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else-if="t.type === 'error'" class="w-5 h-5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
          <svg v-else class="w-5 h-5 text-slate-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
          </svg>
        </div>
        <!-- Text -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium">{{ t.message }}</p>
          <p v-if="t.sub" class="text-xs mt-0.5 opacity-70">{{ t.sub }}</p>
        </div>
        <!-- Close -->
        <button @click="remove(t.id)" class="flex-shrink-0 opacity-50 hover:opacity-100 transition-opacity">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>
    </TransitionGroup>
  </Teleport>
</template>

<style>
.toast-enter-active { animation: toastIn 0.35s ease-out; }
.toast-leave-active { animation: toastOut 0.25s ease-in; }
@keyframes toastIn {
  from { opacity: 0; transform: translateX(30px) scale(0.95); }
  to { opacity: 1; transform: translateX(0) scale(1); }
}
@keyframes toastOut {
  from { opacity: 1; transform: translateX(0) scale(1); }
  to { opacity: 0; transform: translateX(30px) scale(0.95); }
}
</style>

<script setup>
import { ref } from 'vue'

const toasts = ref([])
let nextId = 0

function show(message, type = 'info', duration = 4000, sub = '') {
  const id = ++nextId
  toasts.value.push({ id, message, type, sub })
  if (duration > 0) {
    setTimeout(() => remove(id), duration)
  }
}

function remove(id) {
  const idx = toasts.value.findIndex(t => t.id === id)
  if (idx !== -1) toasts.value.splice(idx, 1)
}

defineExpose({ show })
</script>
