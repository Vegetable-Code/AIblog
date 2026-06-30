<template>
  <Teleport to="body">
    <div v-if="auth.showLogin" class="fixed inset-0 z-[60] flex items-center justify-center p-4"
      @click.self="auth.closeLogin()">
      <div class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>
      
      <div class="relative w-full max-w-md bg-slate-800/95 backdrop-blur-xl rounded-2xl border border-slate-700/50 shadow-2xl overflow-hidden"
        style="animation: modalIn 0.25s ease-out">
        
        <!-- Header with close button -->
        <div class="flex items-center justify-between px-6 py-4 border-b border-slate-700/50">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white text-xs font-bold">A</div>
            <span class="text-sm font-semibold text-white">{{ activeTab === 'login' ? '登录' : '注册' }}</span>
          </div>
          <button @click="auth.closeLogin()" type="button"
            class="w-8 h-8 rounded-lg bg-slate-700/50 hover:bg-slate-600/50 flex items-center justify-center text-slate-400 hover:text-white transition-all">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
          </button>
        </div>
        
        <!-- Tabs -->
        <div class="flex border-b border-slate-700/50">
          <button v-for="tab in tabs" :key="tab.key"
            @click="activeTab = tab.key"
            :class="['flex-1 py-3 text-sm font-medium transition-colors relative',
              activeTab === tab.key ? 'text-cyan-400' : 'text-slate-500 hover:text-slate-300']">
            {{ tab.label }}
            <div v-if="activeTab === tab.key" class="absolute bottom-0 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-cyan-500 to-violet-500 rounded-full"></div>
          </button>
        </div>

        <div class="p-6">
          <form v-if="activeTab === 'login'" @submit.prevent="handleLogin" class="space-y-4">
            <div>
              <input v-model="loginForm.username" placeholder="用户名" required
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div>
              <input v-model="loginForm.password" type="password" placeholder="密码" required
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div v-if="loginError" class="text-red-400 text-xs">{{ loginError }}</div>
            <button type="submit" :disabled="loginLoading"
              class="w-full py-3 bg-gradient-to-r from-cyan-500 to-violet-500 text-white text-sm font-medium rounded-xl hover:from-cyan-400 hover:to-violet-400 disabled:opacity-50 transition-all shadow-lg shadow-cyan-500/20">
              {{ loginLoading ? '登录中...' : '登录' }}
            </button>
            <p class="text-center text-xs text-slate-600">
              <button type="button" @click="activeTab = 'register'; refreshCaptcha()" class="text-cyan-400 hover:text-cyan-300">没有账号？立即注册</button>
            </p>
          </form>

          <form v-else @submit.prevent="handleRegister" class="space-y-4">
            <div>
              <input v-model="regForm.username" placeholder="用户名" required
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div>
              <input v-model="regForm.email" type="email" placeholder="邮箱" required
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div>
              <input v-model="regForm.nickname" placeholder="昵称（选填）"
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div>
              <input v-model="regForm.password" type="password" placeholder="密码" required
                class="w-full bg-slate-700/50 border border-slate-600/50 rounded-xl px-4 py-3 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-cyan-500/50 transition-colors" />
            </div>
            <div v-if="regError" class="text-red-400 text-xs">{{ regError }}</div>
            <button type="submit" :disabled="regLoading"
              class="w-full py-3 bg-gradient-to-r from-cyan-500 to-violet-500 text-white text-sm font-medium rounded-xl hover:from-cyan-400 hover:to-violet-400 disabled:opacity-50 transition-all shadow-lg shadow-cyan-500/20">
              {{ regLoading ? '注册中...' : '注册' }}
            </button>
            <p class="text-center text-xs text-slate-600">
              <button type="button" @click="activeTab = 'login'" class="text-cyan-400 hover:text-cyan-300">已有账号？立即登录</button>
            </p>
          </form>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<style>
@keyframes modalIn {
  from { opacity: 0; transform: scale(0.95) translateY(10px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
</style>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()

// Load captcha on mount
refreshCaptcha()
const activeTab = ref('login')
const tabs = [
  { key: 'login', label: '登录' },
  { key: 'register', label: '注册' },
]

const loginForm = reactive({ username: '', password: '' })
const regForm = reactive({ username: '', email: '', password: '', nickname: '', captchaId: '', captchaText: '', emailCode: '' })
const loginLoading = ref(false)
const regLoading = ref(false)
const loginError = ref('')
const regError = ref('')

async function handleLogin() {
  loginLoading.value = true
  loginError.value = ''
  try {
    await auth.login(loginForm.username, loginForm.password)
    auth.closeLogin()
    loginForm.password = ''
  } catch (e) {
    loginError.value = e.response?.data?.detail || '登录失败'
  } finally {
    loginLoading.value = false
  }
}

async function handleRegister() {
  regLoading.value = true
  regError.value = ''
  try {
    await auth.register(regForm.username, regForm.email, regForm.password, regForm.nickname)
    auth.closeLogin()
    regForm.password = ''
  } catch (e) {
    regError.value = e.response?.data?.detail || '注册失败'
  } finally {
    regLoading.value = false
  }
}
</script>
