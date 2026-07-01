<template>
  <div class="fade-in-up">
    <div class="text-center py-8 mb-8">
      <h1 class="text-3xl md:text-4xl font-bold text-white mb-3 tracking-tight">文章<span class="gradient-text">分类</span></h1>
      <p class="text-slate-400">{{ $t('categories.subtitle') }}</p>
    </div>

    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div v-for="i in 6" :key="i" class="bg-slate-800/40 rounded-2xl p-6 animate-pulse">
        <div class="h-5 bg-slate-700/50 rounded w-1/2 mb-3"></div>
        <div class="h-3 bg-slate-700/50 rounded w-3/4"></div>
        <div class="h-3 bg-slate-700/50 rounded w-1/4 mt-4"></div>
      </div>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <router-link v-for="c in categories" :key="c.id" :to="'/?category_id=' + c.id"
        class="group relative bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl p-6 overflow-hidden hover:border-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/5 transition-all duration-300">
        <div class="flex items-start justify-between mb-3">
          <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-violet-500/20 flex items-center justify-center">
            <svg class="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2h-6l-2-2H5a2 2 0 00-2 2z"/></svg>
          </div>
          <span class="text-xs text-cyan-400 font-medium opacity-0 group-hover:opacity-100 transition-opacity">浏览 &rarr;</span>
        </div>
        <h3 class="text-lg font-semibold text-white group-hover:text-cyan-400 transition-colors">{{ c.name }}</h3>
        <p class="text-sm text-slate-500 mt-1 line-clamp-2">{{ c.description || $t('categories.no_description') }}</p>
        <div class="flex items-center gap-2 mt-4 text-xs text-slate-500">
          <span class="px-2 py-1 rounded bg-slate-800 border border-slate-700">{{ $t('categories.post_count', { count: c.post_count }) }}</span>
        </div>
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const categories = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await axios.get('/api/v1/categories')
    categories.value = res.data
  } finally {
    loading.value = false
  }
})
</script>
