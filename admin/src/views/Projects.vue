<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-bold">作品管理</h2>
      <el-button type="primary" @click="openCreate">新建作品</el-button>
    </div>
    <el-card v-loading="loading">
      <div v-if="projects.length === 0" class="text-center py-10 text-slate-400">暂无作品</div>
      <el-table v-else :data="projects" stripe style="width: 100%" @row-click="editProject">
        <el-table-column label="封面" width="120">
          <template #default="{ row }">
            <img v-if="row.cover_image" :src="row.cover_image" class="w-16 h-12 object-cover rounded" />
            <span v-else class="text-slate-300 text-xs">无封面</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="description" label="简介" min-width="200" show-overflow-tooltip />
        <el-table-column label="标签" width="200">
          <template #default="{ row }">
            <el-tag v-for="t in (row.tags_str || '').split(',').filter(Boolean)" :key="t" size="small" class="mr-1 mb-1">{{ t.trim() }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_published ? 'success' : 'info'" size="small">{{ row.is_published ? '已发布' : '草稿' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="排序" width="80" prop="sort_order" />
        <el-table-column label="操作" width="180" fixed="right" @click.stop>
          <template #default="{ row }">
            <el-button size="small" @click.stop="editProject(row)">编辑</el-button>
            <el-popconfirm title="确认删除？" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger" @click.stop>删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑作品' : '新建作品'" width="700px" :close-on-click-modal="false">
      <el-form :model="form" label-width="80" v-loading="saving">
        <el-form-item label="标题"><el-input v-model="form.title" placeholder="作品标题" /></el-form-item>
        <el-form-item label="链接"><el-input v-model="form.slug" placeholder="url-slug" /></el-form-item>
        <el-form-item label="简介"><el-input v-model="form.description" type="textarea" :rows="2" placeholder="简短描述" /></el-form-item>
        <el-form-item label="内容"><el-input v-model="form.content" type="textarea" :rows="8" placeholder="支持 Markdown 格式" /></el-form-item>
        <el-form-item label="项目链接"><el-input v-model="form.link" placeholder="https://github.com/..." /></el-form-item>
        <el-form-item label="封面图">
          <div class="flex gap-2">
            <el-input v-model="form.cover_image" placeholder="封面图片 URL" class="flex-1" />
            <el-upload :action="uploadUrl" :headers="uploadHeaders" :show-file-list="false" :on-success="onCoverUpload" accept="image/*">
              <el-button size="small">上传</el-button>
            </el-upload>
          </div>
          <img v-if="form.cover_image" :src="form.cover_image" class="mt-2 h-24 rounded object-cover" />
        </el-form-item>
        <el-form-item label="多图">
          <div class="flex flex-wrap gap-2">
            <div v-for="(img, i) in imageList" :key="i" class="relative group">
              <img :src="img" class="w-20 h-14 object-cover rounded border" />
              <button @click.prevent="removeImage(i)" class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white rounded-full text-xs leading-4 opacity-0 group-hover:opacity-100">x</button>
            </div>
            <el-upload :action="uploadUrl" :headers="uploadHeaders" :show-file-list="false" :on-success="onMultiUpload" accept="image/*">
              <div class="w-20 h-14 border-2 border-dashed border-slate-300 rounded flex items-center justify-center text-slate-400 cursor-pointer hover:border-cyan-400 text-lg">+</div>
            </el-upload>
          </div>
        </el-form-item>
        <el-form-item label="技术栈"><el-input v-model="form.tags_str" placeholder="React, Vue, Python 逗号分隔" /></el-form-item>
        <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" size="small" /></el-form-item>
        <el-form-item><el-checkbox v-model="form.is_published">发布</el-checkbox></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
const api = axios.create({ baseURL: '/api/v1' })
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = 'Bearer ' + token
  return config
})
const uploadUrl = '/api/v1/projects/upload'
const uploadHeaders = computed(() => {
  const t = localStorage.getItem('token')
  return t ? { Authorization: 'Bearer ' + t } : {}
})
const projects = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const editId = ref(null)
const imageList = ref([])
const defaultForm = { title: '', slug: '', description: '', content: '', link: '', cover_image: '', tags_str: '', is_published: false, sort_order: 0 }
const form = ref({ ...defaultForm })
function resetForm() { form.value = { ...defaultForm }; imageList.value = []; editId.value = null; isEdit.value = false }
function openCreate() { resetForm(); dialogVisible.value = true }
function editProject(row) { isEdit.value = true; editId.value = row.id; form.value = { ...row }; try { imageList.value = JSON.parse(row.images || '[]') } catch { imageList.value = [] }; dialogVisible.value = true }
function onCoverUpload(res) { form.value.cover_image = res.url }
function onMultiUpload(res) { imageList.value.push(res.url) }
function removeImage(idx) { imageList.value.splice(idx, 1) }
async function loadProjects() { loading.value = true; try { const res = await api.get('/projects'); projects.value = res.data } catch { ElMessage.error('加载失败') } finally { loading.value = false } }
async function handleSave() {
  if (!form.value.title || !form.value.slug) { ElMessage.warning('请填写标题和链接'); return }
  saving.value = true
  try {
    const payload = { ...form.value, images: JSON.stringify(imageList.value) }
    if (isEdit.value) { await api.put('/projects/' + editId.value, payload); ElMessage.success('更新成功') }
    else { await api.post('/projects', payload); ElMessage.success('创建成功') }
    dialogVisible.value = false; await loadProjects()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
  finally { saving.value = false }
}
async function handleDelete(id) { try { await api.delete('/projects/' + id); ElMessage.success('删除成功'); await loadProjects() } catch { ElMessage.error('删除失败') } }
onMounted(loadProjects)
</script>