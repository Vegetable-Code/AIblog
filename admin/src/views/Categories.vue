<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h2 class="text-xl font-bold text-slate-800">分类管理</h2>
        <p class="text-sm text-slate-400 mt-0.5">管理文章分类</p>
      </div>
      <el-button type="primary" class="btn-gradient rounded-xl h-10" @click="openCreate">
        <el-icon class="mr-1.5"><Plus /></el-icon>新建分类
      </el-button>
    </div>

    <el-card class="rounded-2xl" shadow="sm">
      <el-table :data="list" stripe v-loading="loading" size="large">
        <el-table-column prop="name" label="分类名" min-width="150">
          <template #default="{ row }">
            <div class="flex items-center gap-2">
              <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-cyan-100 to-violet-100 flex items-center justify-center">
                <el-icon size="16" class="text-cyan-600"><Folder /></el-icon>
              </div>
              <span class="font-medium text-slate-700">{{ row.name }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="slug" label="Slug" width="180" />
        <el-table-column prop="post_count" label="文章数" width="100" align="center" />
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button size="small" round class="rounded-lg" @click="openEdit(row)">编辑</el-button>
            <el-popconfirm title="确定删除该分类？" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger" round class="rounded-lg">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="editForm.id ? '编辑分类' : '新建分类'" width="500" class="rounded-2xl">
      <el-form :model="editForm" label-width="70">
        <el-form-item label="名称"><el-input v-model="editForm.name" placeholder="分类名称" /></el-form-item>
        <el-form-item label="Slug"><el-input v-model="editForm.slug" placeholder="category-slug" /></el-form-item>
        <el-form-item label="描述"><el-input v-model="editForm.description" type="textarea" :rows="2" placeholder="分类描述（选填）" /></el-form-item>
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
import { Plus, Folder } from '@element-plus/icons-vue'
import { api } from '../stores/auth'

const list = ref([]), loading = ref(false), saving = ref(false), dialogVisible = ref(false)
const editForm = ref({ id: null, name: '', slug: '', description: '' })

async function loadData() { loading.value = true; try { const r = await api.get('/categories'); list.value = r.data } finally { loading.value = false } }
function openCreate() { editForm.value = { id: null, name: '', slug: '', description: '' }; dialogVisible.value = true }
function openEdit(row) { editForm.value = { id: row.id, name: row.name, slug: row.slug, description: row.description || '' }; dialogVisible.value = true }

async function handleSave() {
  saving.value = true
  try {
    if (editForm.value.id) { await api.put('/categories/' + editForm.value.id, editForm.value); ElMessage.success('更新成功') }
    else { await api.post('/categories', editForm.value); ElMessage.success('创建成功') }
    dialogVisible.value = false; loadData()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '操作失败') }
  finally { saving.value = false }
}
async function handleDelete(id) { await api.delete('/categories/' + id); ElMessage.success('删除成功'); loadData() }
onMounted(loadData)
</script>
