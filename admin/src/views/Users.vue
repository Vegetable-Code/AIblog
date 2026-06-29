<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-slate-800">用户管理</h2>
        <p class="text-sm text-slate-400 mt-0.5">管理系统用户账号</p>
      </div>
      <el-button type="primary" class="btn-gradient rounded-xl h-10" @click="openCreate">
        <el-icon class="mr-1.5"><Plus /></el-icon>新建用户
      </el-button>
    </div>

    <el-card class="rounded-2xl" shadow="sm">
      <el-table :data="list" stripe v-loading="loading" size="large">
        <el-table-column label="用户" min-width="200">
          <template #default="{ row }">
            <div class="flex items-center gap-3">
              <div class="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white text-sm font-bold">
                {{ (row.username || '?')[0].toUpperCase() }}
              </div>
              <div>
                <div class="font-medium text-slate-700">{{ row.username }}</div>
                <div class="text-xs text-slate-400">{{ row.email }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="nickname" label="昵称" width="120" />
        <el-table-column label="状态" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small" effect="light" round>
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="管理员" width="90" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_superuser ? 'warning' : 'info'" size="small" effect="light" round>
              {{ row.is_superuser ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" round class="rounded-lg" @click="openEdit(row)">编辑</el-button>
            <el-popconfirm title="确定删除该用户？" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger" round class="rounded-lg" :disabled="row.is_superuser">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editForm.id ? '编辑用户' : '新建用户'" width="500" class="rounded-2xl">
      <el-form :model="editForm" label-width="70">
        <el-form-item label="用户名"><el-input v-model="editForm.username" :disabled="!!editForm.id" /></el-form-item>
        <el-form-item label="邮箱"><el-input v-model="editForm.email" /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="editForm.nickname" /></el-form-item>
        <el-form-item :label="editForm.id ? '新密码' : '密码'">
          <el-input v-model="editForm.password" type="password" show-password :placeholder="editForm.id ? '不填则不修改' : ''" />
        </el-form-item>
        <template v-if="editForm.id">
          <el-form-item><el-checkbox v-model="editForm.is_active" size="large">激活</el-checkbox></el-form-item>
          <el-form-item><el-checkbox v-model="editForm.is_superuser" size="large">超级管理员</el-checkbox></el-form-item>
        </template>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false" class="rounded-xl">取消</el-button>
        <el-button type="primary" :loading="saving" class="rounded-xl" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { api } from '../stores/auth'

const list = ref([]), loading = ref(false), saving = ref(false), dialogVisible = ref(false)
const editForm = ref({})

function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) }

async function loadData() { loading.value = true; try { const r = await api.get('/users'); list.value = r.data.items } finally { loading.value = false } }
function openCreate() { editForm.value = { id: null, username: '', email: '', password: '', nickname: '' }; dialogVisible.value = true }
function openEdit(row) { editForm.value = { id: row.id, username: row.username, email: row.email, nickname: row.nickname, password: '', is_active: row.is_active, is_superuser: row.is_superuser }; dialogVisible.value = true }

async function handleSave() {
  saving.value = true
  try {
    const data = { ...editForm.value }
    if (!data.password) delete data.password
    if (data.id) { await api.put('/users/' + data.id, data); ElMessage.success('更新成功') }
    else { await api.post('/users', data); ElMessage.success('创建成功') }
    dialogVisible.value = false; loadData()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '操作失败') }
  finally { saving.value = false }
}
async function handleDelete(id) { await api.delete('/users/' + id); ElMessage.success('删除成功'); loadData() }
onMounted(loadData)
</script>
