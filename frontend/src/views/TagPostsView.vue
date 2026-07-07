<template>
  <div>
    <!-- Back link -->
    <div class="mb-6">
      <router-link to="/" class="inline-flex items-center gap-1.5 text-sm text-slate-400 hover:text-cyan-400 transition-colors">
        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/>
        </svg>
        {{ $t('home.back') || '返回首页' }}
      </router-link>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="space-y-6">
      <div v-for="i in 3" :key="i" class="bg-slate-800/40 rounded-2xl p-6 animate-pulse">
        <div class="flex gap-4">
          <div class="flex-1 space-y-3">
            <div class="h-5 bg-slate-700/50 rounded w-3/4"></div>
            <div class="h-4 bg-slate-700/50 rounded w-1/2"></div>
            <div class="h-3 bg-slate-700/50 rounded w-1/4"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- No posts -->
    <div v-else-if="posts.length === 0 && tag" class="text-center py-20">
      <p class="text-slate-500">{{ $t('home.no_articles_tag', { tag: tag.name }) || '该标签下暂无文章' }}</p>
    </div>

    <!-- Tag heading -->
    <div v-if="tag" class="mb-8">
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-medium mb-3">
        <span class="w-2 h-2 rounded-full bg-cyan-400"></span>
        {{ $t('home.tag_filter') || '标签' }}: {{ tag.name }}
      </div>
      <h1 class="text-3xl font-bold text-white">{{ $t('home.articles_with_tag', { tag: tag.name }) || tag.name }}</h1>
    </div>

    <!-- Tag not found -->
    <div v-else-if="!loading" class="text-center py-20">
      <p class="text-slate-500">{{ $t('home.tag_not_found') || '标签不存在' }}</p>
    </div>

    <!-- Posts list -->
    <div v-if="posts.length > 0" class="space-y-5">
      <article v-for="post in posts" :key="post.id"
        class="group relative bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl overflow-hidden hover:border-cyan-500/30 hover:shadow-xl hover:shadow-cyan-500/5 transition-all duration-500">
        <router-link :to="'/post/' + post.slug" class="block p-6 md:p-8">
          <div class="flex items-start gap-6">
            <div v-if="post.cover_image" class="hidden md:block flex-shrink-0">
              <div class="w-28 h-28 rounded-xl overflow-hidden border border-slate-700/50">
                <img :src="post.cover_image" :alt="post.title" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" loading="lazy" />
              </div>
            </div>
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-2">
                <span v-if="post.category" class="px-2.5 py-0.5 rounded-md bg-slate-800 text-slate-400 text-xs border border-slate-700">{{ post.category.name }}</span>
              </div>
              <h2 class="text-xl md:text-2xl font-bold text-white group-hover:text-cyan-400 transition-colors mb-2">{{ post.title }}</h2>
              <p class="text-slate-400 text-sm leading-relaxed">{{ post.summary || $t('home.no_summary') || '暂无摘要' }}</p>
              <div class="flex items-center gap-4 mt-4 text-xs text-slate-500">
                <span>{{ formatDate(post.published_at || post.created_at) }}</span>
                <span>{{ $t('home.views', { count: post.views_count }) }}</span>
              </div>
            </div>
          </div>
        </router-link>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '../stores/app'
import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })
const route = useRoute()
const store = useAppStore()
const { locale } = useI18n()

const tag = ref(null)
const posts = ref([])
const loading = ref(true)

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString(locale.value, { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  const slug = route.params.slug
  // Ensure tags are loaded
  if (!store.tags.length) {
    await store.fetchTags()
  }
  // Find tag by slug
  tag.value = store.tags.find(t => t.slug === slug) || null
  if (!tag.value) {
    loading.value = false
    return
  }
  try {
    const res = await api.get('/posts', { params: { tag_id: tag.value.id, page: 1, page_size: 50 } })
    posts.value = res.data.items
  } catch {
    // noop
  }
  loading.value = false
})

// Dynamic SEO
useHead({
  title: () => tag.value ? tag.value.name + ' - AI宸ョ▼甯埚崥瀹' : '鏍囩 - AI宸ョ▼甯埚崥瀹',
  meta: () => [
    { name: 'description', content: tag.value ? '鏌ョ湅"' + tag.value.name + '"鏍囩鐩稿叧鏂囩珷' : '鏍囩鍒嗛〉' },
  ]
})
</script>
