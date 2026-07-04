<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-bold">????</h2>
      <el-button type="primary" @click="openCreate">????</el-button>
    </div>
    <el-card v-loading="loading">
      <div v-if="projects.length === 0" class="text-center py-10 text-slate-400">????</div>
      <el-table v-else :data="projects" stripe style="width: 100%" @row-click="editProject">
        <el-table-column label="??" width="120">
          <template #default="{ row }">
            <img v-if="row.cover_image" :src="row.cover_image" class="w-16 h-12 object-cover rounded" />
            <span v-else class="text-slate-300 text-xs">???</span>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="??" min-width="180" />
        <el-table-column prop="description" label="??" min-width="200" show-overflow-tooltip />
        <el-table-column label="??" width="200">
          <template #default="{ row }">
            <el-tag v-for="t in (row.tags_str || '').split(',').filter(Boolean)" :key="t" size="small" class="mr-1 mb-1">{{ t.trim() }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="??" width="100">
          <template #default="{ row }"><el-tag :type="row.is_published ? 'success' : 'info'" size="small">{{ row.is_published ? '???' : '??' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="??" width="80" prop="sort_order" />
        <el-table-column label="??" width="180" fixed="right" @click.stop>
          <template #default="{ row }">
            <el-button size="small" @click.stop="editProject(row)">??</el-button>
            <el-popconfirm title="?????" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger" @click.stop>??</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog v-model="dialogVisible" :title="isEdit ? '????' : '????'" width="700px" :close-on-click-modal="false">
      <el-form :model="form" label-width="80" v-loading="saving">
        <el-form-item label="??"><el-input v-model="form.title" placeholder="????" /></el-form-item>
        <el-form-item label="??"><el-input v-model="form.slug" placeholder="url-slug" /></el-form-item>
        <el-form-item label="??"><el-input v-model="form.description" type="textarea" :rows="2" placeholder="????" /></el-form-item>
        <el-form-item label="??"><el-input v-model="form.content" type="textarea" :rows="8" placeholder="?? Markdown ??" /></el-form-item>
        <el-form-item label="????"><el-input v-model="form.link" placeholder="https://github.com/..." /></el-form-item>
        <el-form-item label="???">
          <div class="flex gap-2">
            <el-input v-model="form.cover_image" placeholder="???? URL" class="flex-1" />
            <el-upload :action="uploadUrl" :headers="uploadHeaders" :show-file-list="false" :on-success="onCoverUpload" accept="image/*">
              <el-button size="small">??</el-button>
            </el-upload>
          </div>
          <img v-if="form.cover_image" :src="form.cover_image" class="mt-2 h-24 rounded object-cover" />
        </el-form-item>
        <el-form-item label="??">
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
        <el-form-item label="???"><el-input v-model="form.tags_str" placeholder="React, Vue, Python ????" /></el-form-item>
        <el-form-item label="??"><el-input-number v-model="form.sort_order" :min="0" size="small" /></el-form-item>
        <el-form-item><el-checkbox v-model="form.is_published">??</el-checkbox></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">??</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">??</el-button>
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
async function loadProjects() { loading.value = true; try { const res = await api.get('/projects'); projects.value = res.data } catch { ElMessage.error('????') } finally { loading.value = false } }
async function handleSave() {
  if (!form.value.title || !form.value.slug) { ElMessage.warning('????????'); return }
  saving.value = true
  try {
    const payload = { ...form.value, images: JSON.stringify(imageList.value) }
    if (isEdit.value) { await api.put('/projects/' + editId.value, payload); ElMessage.success('????') }
    else { await api.post('/projects', payload); ElMessage.success('????') }
    dialogVisible.value = false; await loadProjects()
  } catch (e) { ElMessage.error(e.response?.data?.detail || '????') }
  finally { saving.value = false }
}
async function handleDelete(id) { try { await api.delete('/projects/' + id); ElMessage.success('????'); await loadProjects() } catch { ElMessage.error('????') } }
onMounted(loadProjects)
</script>