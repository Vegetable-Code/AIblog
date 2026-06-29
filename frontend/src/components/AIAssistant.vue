<template>
  <div class="fixed top-20 right-6 z-50">
    <!-- Floating Button -->
    <button v-if="!isOpen" @click="open" 
      class="w-14 h-14 rounded-2xl bg-gradient-to-br from-cyan-500 to-violet-500 text-white shadow-2xl shadow-cyan-500/30 hover:shadow-violet-500/40 hover:scale-105 transition-all duration-300 flex items-center justify-center group">
      <svg class="w-6 h-6 group-hover:scale-110 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z"/>
      </svg>
      <span class="absolute -top-1 -right-1 w-4 h-4 bg-emerald-400 rounded-full border-2 border-slate-900 animate-pulse"></span>
    </button>

    <!-- Dialog -->
    <div v-else class="w-[380px] md:w-[420px] bg-slate-800/95 backdrop-blur-xl rounded-2xl border border-slate-700/50 shadow-2xl shadow-cyan-500/10 overflow-hidden"
      style="animation: slideUp 0.3s ease-out">
      
      <!-- Header -->
      <div class="flex items-center justify-between px-5 py-4 border-b border-slate-700/50">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/>
            </svg>
          </div>
          <div>
            <div class="text-sm font-semibold text-white">AI 助手</div>
            <div class="text-[10px] text-slate-500">智能搜索 · 技术问答</div>
          </div>
        </div>
        <button @click="close" class="w-7 h-7 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 flex items-center justify-center text-slate-400 hover:text-white transition-all">
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
        </button>
      </div>

      <!-- Messages -->
      <div ref="messagesRef" class="h-[350px] overflow-y-auto px-5 py-4 space-y-4 scroll-smooth">
        <!-- Welcome -->
        <div v-if="messages.length === 0" class="text-center py-8">
          <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500/20 to-violet-500/20 flex items-center justify-center mx-auto mb-3">
            <svg class="w-6 h-6 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/>
            </svg>
          </div>
          <p class="text-slate-400 text-sm">你好！我是 AI 助手 👋</p>
          <p class="text-slate-500 text-xs mt-1">输入技术问题，帮你搜索相关文章</p>
          <div class="flex flex-wrap justify-center gap-2 mt-4">
            <button v-for="suggestion in suggestions" :key="suggestion" @click="ask(suggestion)"
              class="px-3 py-1.5 rounded-lg bg-slate-700/50 border border-slate-600/50 text-xs text-slate-300 hover:border-cyan-500/30 hover:text-cyan-400 transition-all">
              {{ suggestion }}
            </button>
          </div>
        </div>

        <!-- Messages -->
        <div v-for="(msg, idx) in messages" :key="idx" :class="['flex gap-3', msg.role === 'user' ? 'justify-end' : 'justify-start']">
          <div v-if="msg.role === 'assistant'" class="w-7 h-7 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center flex-shrink-0 mt-1">
            <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>
          </div>
          <div :class="['max-w-[80%]', msg.role === 'user' ? 'order-1' : 'order-2']">
            <div v-if="msg.role === 'user'"
              class="bg-gradient-to-br from-cyan-500 to-violet-500 text-white text-sm rounded-2xl rounded-tr-md px-4 py-2.5">
              {{ msg.content }}
            </div>
            <div v-else class="space-y-2">
              <div class="bg-slate-700/50 text-slate-200 text-sm rounded-2xl rounded-tl-md px-4 py-2.5">
                <p>{{ msg.content }}</p>
                <div v-if="msg.articles?.length" class="mt-3 space-y-2 border-t border-slate-600/50 pt-3">
                  <p class="text-[10px] text-slate-500 uppercase tracking-wider font-medium">相关文章</p>
                  <a v-for="article in msg.articles" :key="article.id"
                    :href="'/post/' + article.slug"
                    target="_blank"
                    class="block bg-slate-800/80 rounded-xl p-3 hover:bg-slate-700/80 transition-all group border border-slate-600/30">
                    <div class="flex items-start gap-2">
                      <svg class="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.129 2.371a4.5 4.5 0 00-1.242-7.244l-4.5-4.5a4.5 4.5 0 00-6.364 6.364l1.757 1.757"/></svg>
                      <div class="min-w-0">
                        <div class="text-sm font-medium text-slate-200 group-hover:text-cyan-400 transition-colors">{{ article.title }}</div>
                        <div class="text-xs text-slate-500 mt-0.5 line-clamp-1">{{ article.summary || '' }}</div>
                        <div class="flex items-center gap-2 mt-1.5" v-if="article.tags?.length">
                          <span v-for="t in article.tags" :key="t" class="text-[10px] px-1.5 py-0.5 rounded bg-slate-700/80 text-slate-400">#{{ t }}</span>
                        </div>
                      </div>
                    </div>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Typing -->
        <div v-if="typing" class="flex gap-3">
          <div class="w-7 h-7 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center flex-shrink-0">
            <svg class="w-3.5 h-3.5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>
          </div>
          <div class="bg-slate-700/50 rounded-2xl rounded-tl-md px-4 py-3">
            <div class="flex gap-1.5">
              <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
              <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
              <span class="w-2 h-2 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="px-5 py-4 border-t border-slate-700/50">
        <form @submit.prevent="handleSubmit" class="flex gap-2">
          <input ref="inputRef" v-model="input" placeholder="输入技术问题..." 
            class="flex-1 bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-2.5 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-all"
            :disabled="typing" />
          <button type="submit" :disabled="!input.trim() || typing"
            class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 text-white flex items-center justify-center disabled:opacity-30 hover:shadow-lg hover:shadow-cyan-500/20 transition-all flex-shrink-0">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"/></svg>
          </button>
        </form>
        <p class="text-[10px] text-slate-600 mt-2">基于全文搜索，帮你快速查找技术文章</p>
      </div>
    </div>
  </div>
</template>

<style>
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px) scale(0.95); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
</style>

<script setup>
import { ref, nextTick, watch } from 'vue'
import axios from 'axios'

const isOpen = ref(false)
const input = ref('')
const messages = ref([])
const typing = ref(false)
const messagesRef = ref(null)
const inputRef = ref(null)

const suggestions = [
  'Transformer是什么',
  '怎么学 Python',
  'Docker 入门',
  '深度学习基础',
]

function scrollToBottom() {
  nextTick(() => {
    if (messagesRef.value) {
      messagesRef.value.scrollTop = messagesRef.value.scrollHeight
    }
  })
}

function open() {
  isOpen.value = true
  nextTick(() => inputRef.value?.focus())
}

function close() {
  isOpen.value = false
}

async function ask(question) {
  input.value = question
  await handleSubmit()
}

async function handleSubmit() {
  const q = input.value.trim()
  if (!q || typing.value) return

  messages.value.push({ role: 'user', content: q })
  input.value = ''
  typing.value = true
  scrollToBottom()

  try {
    const res = await axios.get('/api/v1/ai/search', { params: { q, limit: 5 } })
    await new Promise(r => setTimeout(r, 500))
    messages.value.push({
      role: 'assistant',
      content: res.data.answer,
      articles: res.data.articles || [],
    })
  } catch (e) {
    messages.value.push({
      role: 'assistant',
      content: '抱歉，服务出错了，请稍后再试。',
      articles: [],
    })
  } finally {
    typing.value = false
    scrollToBottom()
  }
}

watch(isOpen, (val) => {
  if (val) scrollToBottom()
})
</script>
