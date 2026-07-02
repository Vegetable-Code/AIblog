<template>
  <div class="grid grid-cols-1 lg:grid-cols-4 gap-8">
    <!-- Main content: articles list -->
    <div class="lg:col-span-3">
      <div class="text-center py-12 mb-10" v-if="!loading && store.posts.length > 0">
        <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-xs font-medium mb-6">
          <span class="w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
          {{ $t('home.articles_count', { count: store.total }) }}
        </div>
        <h1 class="text-4xl md:text-5xl font-bold text-white mb-4 tracking-tight" v-html="$t('home.title')"></h1>
        <p class="text-slate-400 text-lg max-w-xl mx-auto">{{ $t('home.subtitle') }}</p>
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
        <p class="text-slate-500">{{ $t('home.no_articles') }}</p>
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
                  <span v-if="post.is_top" class="px-2 py-0.5 rounded-md bg-gradient-to-r from-cyan-500/20 to-violet-500/20 text-cyan-400 text-xs font-medium border border-cyan-500/20">{{ $t('home.pinned') }}</span>
                  <span v-if="post.category" class="px-2.5 py-0.5 rounded-md bg-slate-800 text-slate-400 text-xs border border-slate-700">{{ post.category.name }}</span>
                </div>
                <h2 class="text-xl md:text-2xl font-bold text-white group-hover:text-cyan-400 transition-colors mb-2">{{ post.title }}</h2>
                <p class="text-slate-400 text-sm leading-relaxed">{{ post.summary || $t('home.no_summary') }}</p>
                <div class="flex items-center gap-4 mt-4 text-xs text-slate-500">
                  <span>{{ formatDate(post.published_at || post.created_at) }}</span>
                  <span>{{ $t('home.views', { count: post.views_count }) }}</span>
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
          class="px-4 py-2 rounded-xl text-sm bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all">{{ $t('home.prev_page') }}</button>
        <button v-for="p in totalPages" :key="p" @click="goPage(p)"
          :class="['w-9 h-9 rounded-lg text-sm font-medium transition-all', p === page ? 'bg-gradient-to-br from-cyan-500 to-violet-500 text-white shadow-lg' : 'bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:border-slate-600']">{{ p }}</button>
        <button @click="goPage(page + 1)" :disabled="page >= totalPages"
          class="px-4 py-2 rounded-xl text-sm bg-slate-800/60 border border-slate-700/50 text-slate-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-all">{{ $t('home.next_page') }}</button>
      </div>
    </div>

    <!-- Sidebar: Calendar + Tag Cloud -->
    <div class="lg:col-span-1 space-y-6">
      <!-- Calendar -->
      <div class="bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl p-4">
        <div class="flex items-center justify-between mb-3">
          <button @click="prevMonth" class="p-1.5 rounded-lg hover:bg-slate-700/50 text-slate-400 hover:text-white transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"/></svg>
          </button>
          <span class="text-sm font-medium text-white">{{ calYear }} {{ localeMonth(calMonth - 1) }}</span>
          <button @click="nextMonth" class="p-1.5 rounded-lg hover:bg-slate-700/50 text-slate-400 hover:text-white transition-colors">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"/></svg>
          </button>
        </div>
        <div class="grid grid-cols-7 gap-0.5 text-center">
          <div v-for="d in dayNames" :key="'h-'+d" class="text-[10px] text-slate-500 font-medium py-1">{{ d }}</div>
          <div v-for="(day, idx) in calendarDays" :key="idx"
            class="text-xs py-1.5 rounded-lg transition-colors relative"
            :class="dayClasses(day)">
            <span v-if="day > 0">{{ day }}</span>
          </div>
        </div>
      </div>

      <!-- Tag Cloud -->
      <div class="bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl p-4">
        <h3 class="text-sm font-medium text-white mb-3">\u6807\u7c7b\u4e91</h3>
        <div class="flex flex-wrap gap-2 justify-center">
          <router-link v-for="t in store.tags" :key="t.id"
            :to="'/tag/' + t.slug"
            class="inline-block rounded-lg transition-all duration-300 hover:opacity-100 hover:scale-110"
            :class="tagCloudClass(t)"
            :style="tagCloudStyle(t)">
            {{ t.name }}
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useAppStore } from '../stores/app'
import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })
const store = useAppStore()
const { t, locale } = useI18n()
const page = ref(1)
const pageSize = 10

const totalPages = computed(() => Math.ceil(store.total / pageSize))

// Calendar state
const now = new Date()
const calYear = ref(now.getFullYear())
const calMonth = ref(now.getMonth() + 1) // 1-based
const articleDates = ref([]) // dates that have articles

const dayNames = ['\u65e5', '\u4e00', '\u4e8c', '\u4e09', '\u56db', '\u4e94', '\u516d']

const calendarDays = computed(() => {
  const year = calYear.value
  const month = calMonth.value
  const firstDay = new Date(year, month - 1, 1).getDay()
  const daysInMonth = new Date(year, month, 0).getDate()
  const days = []
  for (let i = 0; i < firstDay; i++) days.push(0)
  for (let d = 1; d <= daysInMonth; d++) days.push(d)
  return days
})

function dayClasses(day) {
  if (day <= 0) return 'invisible'
  const dateStr = calYear.value + '-' + String(calMonth.value).padStart(2, '0') + '-' + String(day).padStart(2, '0')
  const hasArticle = articleDates.value.some(a => a.date === dateStr)
  const isToday = dateStr === new Date().toISOString().slice(0, 10)
  const classes = []
  if (isToday) classes.push('bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/30')
  else if (hasArticle) classes.push('bg-violet-500/10 text-violet-300 hover:bg-violet-500/20')
  else classes.push('text-slate-400 hover:bg-slate-700/30')
  if (hasArticle) classes.push('cursor-pointer')
  return classes.join(' ')
}

function localeMonth(m) {
  const names = ['\u4e00\u6708','\u4e8c\u6708','\u4e09\u6708','\u56db\u6708','\u4e94\u6708','\u516d\u6708','\u4e03\u6708','\u516b\u6708','\u4e5d\u6708','\u5341\u6708','\u5341\u4e00\u6708','\u5341\u4e8c\u6708']
  return names[m] || ''
}

async function fetchCalendar() {
  try {
    const res = await api.get('/posts/calendar/dates', { params: { year: calYear.value, month: calMonth.value } })
    articleDates.value = res.data
  } catch { articleDates.value = [] }
}

function prevMonth() {
  if (calMonth.value <= 1) { calMonth.value = 12; calYear.value-- }
  else calMonth.value--
  fetchCalendar()
}

function nextMonth() {
  if (calMonth.value >= 12) { calMonth.value = 1; calYear.value++ }
  else calMonth.value++
  fetchCalendar()
}

// Tag cloud
function tagCountMax() {
  if (!store.tags.length) return 1
  return Math.max(...store.tags.map(t => t.post_count || 1), 1)
}

function tagCloudClass(t) {
  const ratio = (t.post_count || 1) / tagCountMax()
  if (ratio > 0.7) return 'text-cyan-300'
  if (ratio > 0.4) return 'text-violet-300'
  return 'text-slate-400'
}

function tagCloudStyle(t) {
  const ratio = (t.post_count || 1) / tagCountMax()
  const size = 0.75 + ratio * 0.65
  return { fontSize: size + 'rem', opacity: 0.5 + ratio * 0.5 }
}

// Pagination
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
  return new Date(d).toLocaleDateString(locale.value, { year: 'numeric', month: 'long', day: 'numeric' })
}

onMounted(async () => {
  await Promise.all([store.fetchCategories(), store.fetchTags(), loadPosts(), fetchCalendar()])
})
</script>
