<template>
  <div class="min-h-screen flex flex-col bg-slate-900">
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
      <div class="absolute -top-40 -right-40 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-96 h-96 bg-violet-500/10 rounded-full blur-3xl"></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-slate-800/30 rounded-full blur-3xl"></div>
    </div>

    <header class="relative z-50 border-b border-slate-800 bg-slate-900/80 backdrop-blur-xl sticky top-0">
      <div class="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
        <router-link to="/" class="flex items-center gap-3 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center text-white font-bold text-sm group-hover:scale-110 transition-transform">AI</div>
          <span class="text-lg font-bold text-white tracking-tight">AI工程师博客</span>
        </router-link>
        <nav class="flex items-center gap-1">
          <router-link to="/" class="px-4 py-2 rounded-lg text-sm" :class="route.path === '/' ? 'text-white bg-slate-800/80' : 'text-slate-400 hover:text-white hover:bg-slate-800/80'">首页</router-link>
          <router-link to="/categories" class="px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800/80 transition-all">分类</router-link>
          <router-link to="/about" class="px-4 py-2 rounded-lg text-sm text-slate-400 hover:text-white hover:bg-slate-800/80 transition-all">关于</router-link>
        </nav>
          <div class="flex items-center gap-2 ml-3 pl-3 border-l border-slate-700/50">
  <template v-if="auth.isLoggedIn">
    <div class="flex items-center gap-2 text-sm">
      <div class="w-7 h-7 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-[10px] text-white font-bold">{{ (auth.user?.nickname || auth.user?.username || 'U')[0].toUpperCase() }}</div>
      <span class="text-slate-300 hidden md:inline">{{ auth.user?.nickname || auth.user?.username }}</span>
    </div>
    <button @click="auth.logout()" class="text-xs text-slate-500 hover:text-red-400 transition-colors">退出</button>
  </template>
  <template v-else>
    <button @click="auth.openLogin()" class="px-3 py-1.5 text-xs font-medium text-cyan-400 border border-cyan-500/30 rounded-lg hover:bg-cyan-500/10 transition-all">登录</button>
  </template>
</div>
      </div>
    </header>

    <main class="relative z-10 flex-1 max-w-5xl mx-auto w-full px-6 py-10">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <footer class="relative z-10 border-t border-slate-800 py-10">
      <div class="max-w-5xl mx-auto px-6 text-center">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-400/20 to-violet-500/20 flex items-center justify-center text-sm font-bold text-cyan-400 mx-auto mb-4">&lt;/&gt;</div>
        <p class="text-slate-500 text-sm">Built with Vue 3 &amp; FastAPI &middot; &copy; {{ new Date().getFullYear() }}</p>
        <p class="text-slate-600 text-xs mt-1">AI工程师 &middot; 探索技术与工程的边界</p>
      </div>
    </footer>
    <AIAssistant />
    <LoginModal />
    <Toast ref="toastRef" />

    <!-- Back to Top Button (Global) -->
    <button 
      v-show="showBackToTop"
      @click="scrollToTop"
      class="fixed bottom-24 right-8 z-[100] w-12 h-12 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white shadow-lg shadow-cyan-500/30 hover:shadow-cyan-500/50 hover:scale-110 transition-all duration-300 border border-cyan-400/20"
    >
      <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 15l7-7 7 7"/>
      </svg>
    </button>
  </div>
</template>

<style>
.page-enter-active, .page-leave-active { transition: opacity 0.2s ease, transform 0.2s ease; }
.page-enter-from { opacity: 0; transform: translateY(10px); }
.page-leave-to { opacity: 0; transform: translateY(-10px); }
html {
  scroll-padding-top: 80px;
}
</style>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import AIAssistant from './components/AIAssistant.vue'
import LoginModal from './components/LoginModal.vue'
import Toast from './components/Toast.vue'
import { useAuthStore } from './stores/auth'
const route = useRoute()
const showBackToTop = ref(false)

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function handleScroll() {
  showBackToTop.value = window.scrollY > 400
}
const toastRef = ref(null)
// Make toast available globally via window
onMounted(() => {
  window.$toast = toastRef.value?.show || (() => {})
})
const auth = useAuthStore()

// Restore login state on mount
if (auth.token) {
  auth.fetchUser()
}

window.addEventListener('scroll', handleScroll)
onUnmounted(() => window.removeEventListener('scroll', handleScroll))
</script>
