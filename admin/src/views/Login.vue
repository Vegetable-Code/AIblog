<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-50 via-white to-cyan-50/30 relative overflow-hidden">
    <!-- Decorative -->
    <div class="absolute -top-40 -right-40 w-80 h-80 bg-cyan-400/10 rounded-full blur-3xl"></div>
    <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-violet-400/10 rounded-full blur-3xl"></div>

    <el-card class="w-[420px] relative shadow-2xl shadow-cyan-500/5 border-0" body-style="padding: 40px">
      <div class="text-center mb-8">
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white font-bold text-lg mx-auto mb-4 shadow-lg shadow-cyan-500/20">AI</div>
        <h2 class="text-2xl font-bold text-slate-800">管理后台</h2>
        <p class="text-sm text-slate-400 mt-1">AI工程师博客 · 内容管理系统</p>
      </div>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" size="large">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" :prefix-icon="User" class="rounded-xl" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" :prefix-icon="Lock" show-password class="rounded-xl" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" class="w-full btn-gradient rounded-xl h-11 text-base" @click="handleLogin">登 录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const formRef = ref(null)
const form = reactive({ username: '', password: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
}

async function handleLogin() {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await auth.login(form.username, form.password)
    // 检查是否为管理员
    if (!auth.user?.is_superuser) {
      auth.logout()
      ElMessage.error('只有管理员才能登录后台')
      loading.value = false
      return
    }
    ElMessage.success('登录成功')
    router.push('/dashboard')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>
