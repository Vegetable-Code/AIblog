<template>
  <div>
    <div class="mb-6">
      <router-link to="/" class="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-cyan-400 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        {{ $t('portfolio.back') || '返回首页' }}
      </router-link>
    </div>
    <div class="text-center py-10 mb-8">
      <h1 class="text-4xl font-bold text-white mb-3">{{ $t('portfolio.title') || '作品集' }}</h1>
      <p class="text-slate-400 max-w-xl mx-auto">{{ $t('portfolio.subtitle') || '我的个人项目与技术实践' }}</p>
    </div>
    <div v-if="loading" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="i in 4" :key="i" class="bg-slate-800/40 rounded-2xl p-6 animate-pulse">
        <div class="h-40 bg-slate-700/50 rounded-xl mb-4"></div>
        <div class="h-5 bg-slate-700/50 rounded w-3/4 mb-2"></div>
        <div class="h-4 bg-slate-700/50 rounded w-1/2"></div>
      </div>
    </div>
    <div v-else-if="projects.length === 0" class="text-center py-20">
      <p class="text-slate-500">{{ $t('portfolio.empty') || '????' }}</p>
    </div>
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div v-for="p in projects" :key="p.id"
        class="group bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl overflow-hidden hover:border-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/5 transition-all duration-500 cursor-pointer"
        @click="openDetail(p)">
        <div v-if="p.cover_image" class="h-48 overflow-hidden">
          <img :src="p.cover_image" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
        </div>
        <div class="p-6">
          <h3 class="text-lg font-bold text-white group-hover:text-cyan-400 transition-colors mb-2">{{ p.title }}</h3>
          <p class="text-sm text-slate-400 mb-3 line-clamp-2">{{ p.description }}</p>
          <div class="flex flex-wrap gap-1.5">
            <span v-for="t in (p.tags_str || '').split(',').filter(Boolean)" :key="t"
              class="px-2 py-0.5 rounded bg-slate-800 text-slate-500 border border-slate-700/50 text-xs">#{{ t.trim() }}</span>
          </div>
        </div>
      </div>
    </div>
    <Teleport to="body">
      <div v-if="detail" class="fixed inset-0 z-[200] flex items-center justify-center p-4" @click.self="closeDetail">
        <div class="fixed inset-0 bg-black/60 backdrop-blur-sm" @click="closeDetail"></div>
        <div class="relative bg-slate-900 border border-slate-700/60 rounded-2xl w-full max-w-3xl max-h-[85vh] overflow-y-auto shadow-2xl">
          <button @click="closeDetail" class="sticky top-4 float-right mr-4 w-8 h-8 rounded-full bg-slate-800 border border-slate-700 text-slate-400 hover:text-white hover:bg-slate-700 flex items-center justify-center z-10">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
          <div v-if="detailImages.length > 0" class="pt-6 px-6">
            <div class="rounded-xl overflow-hidden border border-slate-700/50 bg-slate-800/50">
              <img :src="detailImages[currentImageIndex]" class="w-full h-64 md:h-80 object-contain" />
            </div>
            <div v-if="detailImages.length > 1" class="flex justify-center gap-2 mt-3">
              <button v-for="(img, i) in detailImages" :key="i" @click="currentImageIndex = i"
                :class="['w-2.5 h-2.5 rounded-full transition-all', i === currentImageIndex ? 'bg-cyan-400 w-6' : 'bg-slate-600 hover:bg-slate-500']"></button>
            </div>
          </div>
          <div class="p-6 pt-4">
            <h2 class="text-2xl font-bold text-white mb-2">{{ detail.title }}</h2>
            <p class="text-slate-400 text-sm mb-4">{{ detail.description }}</p>
            <div v-if="detail.tags_str" class="flex flex-wrap gap-1.5 mb-4">
              <span v-for="t in (detail.tags_str || '').split(',').filter(Boolean)" :key="t"
                class="px-2 py-0.5 rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 text-xs">{{ t.trim() }}</span>
            </div>
            <div v-if="detail.content" class="prose prose-invert max-w-none text-sm text-slate-300 mb-4" v-html="renderMarkdown(detail.content)"></div>
            <div class="flex gap-3">
              <a v-if="detail.link" :href="detail.link" target="_blank"
                class="inline-flex items-center gap-1.5 px-4 py-2 rounded-xl text-sm font-medium bg-gradient-to-r from-cyan-500 to-violet-500 text-white hover:shadow-lg hover:shadow-cyan-500/30 transition-all">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"/></svg>
                {{ $t('portfolio.view_project') || '????' }}
              </a>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import axios from 'axios'
const api = axios.create({ baseURL: '/api/v1' })
const { locale } = useI18n()
const projects = ref([])
const loading = ref(true)
const detail = ref(null)
const currentImageIndex = ref(0)
const detailImages = computed(() => {
  if (!detail.value) return []
  try { return JSON.parse(detail.value.images || '[]') } catch { return [] }
})
function renderMarkdown(md) {
  if (!md) return ''
  return '<p class="mb-3">' + md
    .replace(/### (.+)/g, '<h3 class="text-lg font-semibold text-white mt-4 mb-2">$1</h3>')
    .replace(/## (.+)/g, '<h2 class="text-xl font-semibold text-white mt-5 mb-2">$1</h2>')
    .replace(/# (.+)/g, '<h1 class="text-2xl font-bold text-white mt-5 mb-2">$1</h1>')
    .replace(/\*\*(.+?)\*\*/g, '<strong class="text-white">$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/\`(.+?)\`/g, '<code class="px-1.5 py-0.5 rounded bg-slate-800 text-cyan-400 text-xs">$1</code>')
    .replace(/^- (.+)/gm, '<li class="text-slate-300 ml-4">$1</li>')
    .replace(/\n\n/g, '</p><p class="mb-3">')
    .replace(/\n/g, '<br/>') + '</p>'
}
function openDetail(p) {
  detail.value = p
  currentImageIndex.value = 0
  document.body.style.overflow = 'hidden'
}
function closeDetail() {
  detail.value = null
  document.body.style.overflow = ''
}
onMounted(async () => {
  try {
    const res = await api.get('/projects/public')
    projects.value = res.data
  } catch {}
  loading.value = false
})
</script>