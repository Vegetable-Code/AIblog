<template>
  <div>
    <div class="text-center py-12 mb-10" v-if="!loading && store.posts.length > 0">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-medium mb-6">
        <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
        共 {{ store.total }} 篇文章
      </div>
      <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight">
        探索 <span class="gradient-text">AI 技术与工程</span>
      </h1>
      <p class="text-slate-400 text-lg max-w-xl mx-auto">分享深度学习、大模型、工程实践与前沿思考</p>
    </div>

    <div v-if="loading" class="space-y-6">
      <div v-for="i in 3" :key="i" class="bg-slate-800/40 rounded-2xl p-6 animate-pulse">
        <div class="flex gap-4">
          <div class="w-24 h-24 bg-slate-700/50 rounded-xl flex-shrink-0"></div>
          <div class="flex-1 space-y-3">
            <div class="h-5 bg-slate-700/50 rounded w-3/4"></div>
            <div class="h-4 bg-slate-700/50 rounded w-1/2"></div>
            <div class="h-3 bg-slate-700/50 rounded w-1/4"></div>
          </div>
        </div>
      </div>
    </div>

    <div v-else-if="store.posts.length === 0" class="text-center py-20">
      <p class="text-slate-500">暂无文章</p>
    </div>

    <div v-else class="space-y-5">
      <article v-for="post in store.posts" :key="post.id"
        class="group relative bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl overflow-hidden hover:border-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/5 transition-all duration-500">
        <router-link :to="'/post/' + post.slug" class="block p-6 md:p-8">
          <div class="flex items-start gap-6">
            <div v-if="post.cover_image" class="hidden md:block flex-shrink-0">
              <div class="w-28 h-28 rounded-xl overflow-hidden border border-slate-700/50">
                <img :src="post.cover_image" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" />
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2">
                <span v-if="post.is_top" class="px-2 py-0.5 rounded-md bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 text-xs font-medium border border-cyan-500/20">置顶</span>
                <span v-if="post.category" class="px-2.5 py-0.5 rounded-md bg-slate-800 text-slate-400 text-xs border border-slate-700">{{ post.category.name }}</span>
              </div>
              <h2 class="text-xl md:text-2xl font-bold text-white group-hover:text-cyan-400 transition-colors mb-2">{{ post.title }}</h2>
              <p class="text-slate-400 text-sm leading-relaxed">{{ post.summary || '暂无摘要' }}</p>
              <div class="flex items-center gap-4 mt-4 text-xs text-slate-500">
                <span>{{ formatDate(post.published_at || post.created_at) }}</span>
                <span>{{ post.views_count }} 次阅读</span>
                <span v-if="post.tags?.length" class="flex gap-1.5">
                  <span v-for="t in post.tags.slice(0, 3)" :key="t.id" class="px-2 py-0.5 rounded bg-slate-800 text-slate-500 border border-slate-700/50">#{{ t.name }}</span>
                </span>
              </div>
            </div>
          </div>
        </router-link>
      </article>
    </div>

    <div v-if="totalPages > 1" class="flex justify-center items-center gap-2 mt-12">
      <button @click="goPage(page - 1)" :disabled="page <= 1"
        class="px-4 py-2 rounded-xl text-sm bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all">上一页</button>
      <button v-for="p in totalPages" :key="p" @click="goPage(p)"
        :class="['w-9 h-9 rounded-lg text-sm font-medium transition-all', p === page ? 'bg-gradient-to-br from-cyan-500 to-violet-500 text-white shadow-lg' : 'bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:border-slate-600']">{{ p }}</button>
      <button @click="goPage(page + 1)" :disabled="page >= totalPages"
        class="px-4 py-2 rounded-xl text-sm bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all">下一页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useAppStore } from '../stores/app'

const store = useAppStore()
const page = ref(1)
const pageSize = 10

const totalPages = computed(() => Math.ceil(store.total / pageSize))

let debounceTimer
function debounceSearch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => { page.value = 1; loadPosts() }, 300)
}

function goPage(p) {
  if (p < 1 || p > totalPages.value) return
  page.value = p
  window.scrollTo({ top: 0, behavior: 'smooth' })
  loadPosts()
}

async function loadPosts() {
  await store.fetchPosts({ page: page.value, page_size: pageSize })
}

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  await Promise.all([store.fetchCategories(), store.fetchTags(), loadPosts()])
})
</script>
