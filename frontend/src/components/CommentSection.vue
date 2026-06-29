<template>
  <div>
    <!-- Comments List -->
    <div v-if="loading" class="space-y-4">
      <div v-for="i in 2" :key="i" class="bg-slate-800/30 rounded-xl p-5 animate-pulse">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-8 h-8 rounded-full bg-slate-700/50"></div>
          <div class="h-3 bg-slate-700/50 rounded w-24"></div>
        </div>
        <div class="h-3 bg-slate-700/50 rounded w-3/4"></div>
        <div class="h-3 bg-slate-700/50 rounded w-1/2 mt-2"></div>
      </div>
    </div>

    <div v-else-if="comments.length === 0" class="text-center py-10">
      <div class="w-12 h-12 rounded-xl bg-slate-800/60 flex items-center justify-center mx-auto mb-3">
        <svg class="w-6 h-6 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/>
        </svg>
      </div>
      <p class="text-slate-500 text-sm">暂无评论，快来抢沙发吧~</p>
    </div>

    <div v-else class="space-y-4">
      <div v-for="c in comments" :key="c.id" class="bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-xl p-5 hover:border-slate-700 transition-colors">
        <div class="flex items-start gap-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white text-sm font-bold flex-shrink-0">
            {{ (c.nickname || '?')[0].toUpperCase() }}
          </div>
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-2">
              <span class="font-medium text-sm text-slate-200">{{ c.nickname }}</span>
              <span class="text-xs text-slate-600">{{ formatDate(c.created_at) }}</span>
            </div>
            <p class="text-sm text-slate-400 leading-relaxed">{{ c.content }}</p>
            <div v-if="c.replies?.length" class="mt-4 space-y-3 pl-5 border-l-2 border-slate-700">
              <div v-for="r in c.replies" :key="r.id" class="bg-slate-800/40 rounded-lg p-3">
                <div class="flex items-center gap-2 mb-1">
                  <span class="font-medium text-sm text-slate-200">{{ r.nickname }}</span>
                  <span class="text-xs text-slate-600">{{ formatDate(r.created_at) }}</span>
                </div>
                <p class="text-sm text-slate-400">{{ r.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Comment Form -->
    <div class="mt-8 bg-slate-800/30 backdrop-blur-sm border border-slate-700/40 rounded-2xl p-6 md:p-8">
      <h3 class="font-semibold text-white mb-5 flex items-center gap-2">
        <svg class="w-5 h-5 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
        </svg>
        发表评论
      </h3>

      <!-- Not logged in -->
      <div v-if="!auth.isLoggedIn" class="text-center py-6">
        <p class="text-slate-500 text-sm mb-3">需要登录后才能发表评论</p>
        <button @click="auth.openLogin()" class="px-5 py-2 bg-gradient-to-r from-cyan-500 to-violet-500 text-white text-sm font-medium rounded-xl hover:from-cyan-400 hover:to-violet-400 transition-all shadow-lg shadow-cyan-500/20">
          立即登录
        </button>
      </div>

      <!-- Logged in form -->
      <form v-else @submit.prevent="submitComment" class="space-y-4">
        <div class="flex items-center gap-3 mb-2">
          <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-xs text-white font-bold">
            {{ (auth.user?.nickname || auth.user?.username || 'U')[0].toUpperCase() }}
          </div>
          <span class="text-sm text-slate-300">{{ auth.user?.nickname || auth.user?.username }}</span>
          <span class="text-[10px] text-slate-600">· 将以你的账号发表</span>
        </div>
        <textarea v-model="content" rows="4" placeholder="写下你的评论..." required
          class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors resize-none"></textarea>
        <div class="flex justify-end">
          <button type="submit" :disabled="submitting || !content.trim()"
            class="px-6 py-2.5 bg-gradient-to-r from-cyan-500 to-violet-500 text-white text-sm font-medium rounded-xl hover:from-cyan-400 hover:to-violet-400 disabled:opacity-50 transition-all shadow-lg shadow-cyan-500/20">
            {{ submitting ? '提交中...' : '提交评论' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const props = defineProps({ postId: { type: Number, required: true } })
const auth = useAuthStore()
const comments = ref([])
const loading = ref(true)
const submitting = ref(false)
const content = ref('')

async function fetchComments() {
  try {
    const res = await axios.get('/api/v1/comments/post/' + props.postId)
    comments.value = res.data
  } finally {
    loading.value = false
  }
}

async function submitComment() {
  if (!content.value.trim() || !auth.isLoggedIn) return
  submitting.value = true
  try {
    // Use auth token for API call
    const token = localStorage.getItem('frontend_token')
    await axios.post('/api/v1/comments', {
      post_id: props.postId,
      content: content.value,
      nickname: auth.user?.nickname || auth.user?.username || '匿名',
      email: auth.user?.email || '',
    }, {
      headers: { Authorization: 'Bearer ' + token }
    })
    content.value = ''
    window.$toast('评论成功，等待审核', 'success')
    fetchComments()
  } catch (e) {
    window.$toast('评论失败，请重试', 'error')
  } finally {
    submitting.value = false
  }
}

function formatDate(d) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

onMounted(fetchComments)
</script>
