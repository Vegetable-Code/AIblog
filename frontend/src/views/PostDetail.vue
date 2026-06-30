<template>
  <div class="fade-in-up" v-if="!loading && post">
    <!-- Breadcrumb -->
    <nav class="flex items-center gap-2 text-sm text-slate-500 mb-8">
      <router-link to="/" class="hover:text-cyan-400 transition-colors">首页</router-link>
      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <span class="text-slate-400" v-if="post.category">{{ post.category.name }}</span>
      <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
      <span class="text-slate-400 truncate max-w-[200px]">{{ post.title }}</span>
    </nav>

    <!-- Article Header -->
    <header class="mb-10">
      <div class="flex items-center gap-2 mb-4">
        <span v-if="post.is_top"
          class="px-2.5 py-1 rounded-md bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 text-xs font-medium border border-cyan-500/20">置顶</span>
        <span v-if="post.category"
          class="px-3 py-1 rounded-md bg-slate-800 text-slate-400 text-xs border border-slate-700">{{ post.category.name }}</span>
      </div>
      <h1 class="text-3xl md:text-4xl lg:text-5xl font-bold text-white leading-tight mb-4 tracking-tight">{{ post.title }}</h1>
      <div class="flex flex-wrap items-center gap-4 text-sm text-slate-500">
        <span class="flex items-center gap-1.5">
          <div class="w-6 h-6 rounded-full bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center text-[10px] text-white font-bold">A</div>
          {{ post.author || 'AI工程师' }}
        </span>
        <span class="flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
          {{ formatDate(post.published_at || post.created_at) }}
        </span>
        <span class="flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          {{ post.views_count }} 次阅读
        </span>
        <span v-if="post.tags?.length" class="flex items-center gap-1.5">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"/></svg>
          <span v-for="t in post.tags" :key="t.id" class="px-2 py-0.5 rounded bg-slate-800 border border-slate-700">#{{ t.name }}</span>
        </span>
      </div>
    </header>

    <!-- Cover Image -->
    <div v-if="post.cover_image" class="mb-10 rounded-2xl overflow-hidden border border-slate-700/50">
      <img :src="post.cover_image" class="w-full max-h-[400px] object-cover" />
    </div>

    <!-- Content -->
    <div class="prose prose-invert max-w-none prose-headings:text-white prose-a:text-cyan-400 prose-strong:text-white prose-code:text-cyan-300 prose-pre:bg-slate-900 prose-pre:border prose-pre:border-slate-700 prose-pre:rounded-xl prose-blockquote:border-cyan-500 prose-blockquote:text-slate-400 prose-td:border-slate-700 prose-th:border-slate-700 prose-img:rounded-xl" v-html="renderedContent"></div>

    <!-- Tags at bottom -->
    <div class="flex flex-wrap gap-2 mt-10 pt-8 border-t border-slate-800" v-if="post.tags?.length">
      <span class="text-sm text-slate-500 mr-2">标签：</span>
      <span v-for="t in post.tags" :key="t.id" class="tag-pill bg-slate-800 text-slate-400 border border-slate-700">{{ t.name }}</span>
    </div>

    <!-- Navigation -->
    <div class="flex justify-between mt-12 pt-8 border-t border-slate-800">
      <router-link to="/" class="flex items-center gap-2 text-sm text-slate-500 hover:text-cyan-400 transition-colors">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18"/></svg>
        返回首页
      </router-link>
    </div>

    <!-- Comments -->
    <div class="mt-12 pt-8 border-t border-slate-800">
      <h2 class="text-xl font-bold text-white mb-6">
        <span class="flex items-center gap-2">
          <svg class="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
          评论
        </span>
      </h2>
      <CommentSection :post-id="post.id" />
    </div>

  </div>

  <!-- Loading -->
  <div v-else-if="loading" class="max-w-3xl mx-auto animate-pulse space-y-6 py-10">
    <div class="h-8 bg-slate-800/60 rounded w-3/4"></div>
    <div class="h-4 bg-slate-800/60 rounded w-1/4"></div>
    <div class="h-64 bg-slate-800/60 rounded-2xl"></div>
    <div class="space-y-3">
      <div class="h-4 bg-slate-800/60 rounded"></div>
      <div class="h-4 bg-slate-800/60 rounded w-5/6"></div>
      <div class="h-4 bg-slate-800/60 rounded w-2/3"></div>
      <div class="h-4 bg-slate-800/60 rounded w-4/5"></div>
    </div>
  </div>

  <!-- Not found -->
  <div v-else class="text-center py-20">
    <p class="text-slate-500">文章不存在</p>
    <router-link to="/" class="inline-block mt-4 text-cyan-400 hover:text-cyan-300">返回首页</router-link>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import { marked } from 'marked'
import CommentSection from '../components/CommentSection.vue'

const route = useRoute()
const post = ref(null)
const loading = ref(true)

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'long', day: 'numeric' })
}

function renderMarkdown(md) {
  if (!md) return ''
  return marked(md, {
    breaks: true,
    gfm: true,
  })
}

const renderedContent = computed(() => {
  if (post.value?.content_html) return post.value.content_html
  return renderMarkdown(post.value?.content || '')
})

onMounted(async () => {
  try {
    const res = await axios.get('/api/v1/posts/' + route.params.slug)
    post.value = res.data
  } catch (e) {
    post.value = null
  } finally {
    loading.value = false
  }
})
</script>


<style>
/* Markdown code block styling */
.prose pre {
  background: #0f172a !important;
  border: 1px solid #1e293b;
  border-radius: 12px;
  padding: 1.25rem;
  overflow-x: auto;
}
.prose code {
  font-size: 0.875em;
}
.prose pre code {
  background: transparent !important;
  padding: 0;
  border: none;
}
.prose img {
  border-radius: 12px;
}
.prose table {
  border-collapse: collapse;
  width: 100%;
}
.prose th, .prose td {
  border: 1px solid #1e293b;
  padding: 0.75rem;
}
.prose th {
  background: #0f172a;
  color: #e2e8f0;
}
</style>
