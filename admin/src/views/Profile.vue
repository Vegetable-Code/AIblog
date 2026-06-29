<template>
  <div>
    <div class="mb-6">
      <h2 class="text-xl font-bold text-slate-800">个人设置</h2>
      <p class="text-sm text-slate-400 mt-0.5">管理你的账号信息</p>
    </div>

    <div v-if="auth.user" class="max-w-2xl">
      <!-- Profile Card -->
      <el-card class="rounded-2xl mb-6" shadow="sm">
        <template #header>
          <div class="flex items-center gap-4">
            <div class="w-14 h-14 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white text-xl font-bold shadow-lg shadow-cyan-500/20">
              {{ (auth.user.username || 'A')[0].toUpperCase() }}
            </div>
            <div>
              <div class="text-lg font-bold text-slate-800">{{ auth.user.nickname || auth.user.username }}</div>
              <div class="text-sm text-slate-400">{{ auth.user.email }}</div>
            </div>
          </div>
        </template>
        <el-form :model="form" label-width="70">
          <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
          <el-form-item label="昵称"><el-input v-model="form.nickname" /></el-form-item>
          <el-form-item label="头像"><el-input v-model="form.avatar" placeholder="头像图片链接" /></el-form-item>
          <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password placeholder="不填则不修改" /></el-form-item>
          <el-form-item>
            <el-button type="primary" :loading="saving" class="btn-gradient rounded-xl h-10 px-8" @click="handleSave">保存设置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore, api } from '../stores/auth'

const auth = useAuthStore()
const saving = ref(false)
const form = ref({ email: '', nickname: '', avatar: '', password: '' })

onMounted(async () => {
  if (!auth.user) await auth.fetchUser()
  if (auth.user) { form.value.email = auth.user.email; form.value.nickname = auth.user.nickname || ''; form.value.avatar = auth.user.avatar || '' }
})

async function handleSave() {
  saving.value = true
  try {
    const data = { ...form.value }
    if (!data.password) delete data.password
    await api.put('/users/' + auth.user.id, data)
    ElMessage.success('保存成功')
    if (auth.user) { auth.user.email = form.value.email; auth.user.nickname = form.value.nickname; auth.user.avatar = form.value.avatar }
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
  finally { saving.value = false }
}
</script>
