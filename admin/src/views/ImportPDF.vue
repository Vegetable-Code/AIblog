<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">PDF 导入文章</h2>
    <el-row :gutter="24">
      <el-col :span="14">
        <el-card>
          <!-- Upload Area -->
          <div
            class="upload-area"
            :class="{ 'dragover': dragging }"
            @dragenter.prevent="dragging = true"
            @dragover.prevent="dragging = true"
            @dragleave.prevent="dragging = false"
            @drop.prevent="handleDrop"
            @click="triggerUpload"
          >
            <template v-if="!file">
              <el-icon class="upload-icon"><UploadFilled /></el-icon>
              <p class="text-slate-400 mt-3">拖拽 PDF 文件到此处，或点击选择文件</p>
              <p class="text-xs text-slate-400 mt-1">支持 PDF 格式，最大 50MB</p>
            </template>
            <template v-else>
              <el-icon class="text-4xl text-cyan-500"><Document /></el-icon>
              <p class="text-sm font-medium text-slate-700 mt-2">{{ file.name }}</p>
              <p class="text-xs text-slate-400">{{ (file.size / 1024).toFixed(1) }} KB</p>
              <el-button size="small" class="mt-2" @click.stop="file = null">重新选择</el-button>
            </template>
          </div>
          <input ref="fileInput" type="file" accept=".pdf" class="hidden" @change="handleFileChange" />
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <template #header><span class="font-medium">导入选项</span></template>
          <el-form label-width="60" v-loading="importing">
            <el-form-item label="分类">
              <el-select v-model="category_id" clearable placeholder="选择分类" class="w-full">
                <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
              </el-select>
            </el-form-item>
            <el-form-item label="标签">
              <el-select v-model="tag_ids" multiple clearable placeholder="选择标签" class="w-full">
                <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id" />
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" :loading="importing" :disabled="!file" @click="handleImport" class="w-full">
                {{ importing ? '导入中...' : '开始导入' }}
              </el-button>
            </el-form-item>
          </el-form>
        </el-card>
        <!-- Result Card -->
        <el-card v-if="result" class="mt-4 border-emerald-200" shadow="none">
          <template #header>
            <div class="flex items-center gap-2 text-emerald-600">
              <el-icon><CircleCheck /></el-icon>
              <span class="font-medium">导入成功</span>
            </div>
          </template>
          <div class="text-sm space-y-2">
            <p><span class="text-slate-400">标题：</span>{{ result.title }}</p>
            <p><span class="text-slate-400">页数：</span>{{ result.pages }} 页</p>
            <p><span class="text-slate-400">字数：</span>{{ result.char_count }} 字</p>
            <p class="text-xs text-slate-400 mt-2 line-clamp-3">{{ result.summary }}</p>
          </div>
          <div class="mt-4 flex gap-2">
            <el-button size="small" type="primary" @click="handleEdit(result.id)">编辑文章</el-button>
            <el-button size="small" @click="resetForm">继续导入</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UploadFilled, CircleCheck, Document } from '@element-plus/icons-vue'
import { api } from '../stores/auth'

const fileInput = ref(null)
const dragging = ref(false)
const importing = ref(false)
const file = ref(null)
const categories = ref([])
const tags = ref([])
const category_id = ref(null)
const tag_ids = ref([])
const result = ref(null)
const router = useRouter()

function handleEdit(id) {
  router.push('/posts/' + id + '/edit')
}

onMounted(async () => {
  const [catRes, tagRes] = await Promise.all([api.get('/categories'), api.get('/tags')])
  categories.value = catRes.data
  tags.value = tagRes.data
})

function triggerUpload() { fileInput.value?.click() }

function handleFileChange(e) {
  const f = e.target.files?.[0]
  if (f) validateAndSet(f)
}

function handleDrop(e) {
  dragging.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f) validateAndSet(f)
}

function validateAndSet(f) {
  if (f.type !== 'application/pdf' && !f.name.toLowerCase().endsWith('.pdf')) {
    ElMessage.warning('请选择 PDF 文件')
    return
  }
  if (f.size > 50 * 1024 * 1024) {
    ElMessage.warning('文件超过 50MB 限制')
    return
  }
  file.value = f
  result.value = null
}

async function handleImport() {
  if (!file.value) return
  importing.value = true
  try {
    const formData = new FormData()
    formData.append('file', file.value)
    if (category_id.value) formData.append('category_id', category_id.value)
    if (tag_ids.value.length) formData.append('tag_ids', tag_ids.value.join(','))

    const res = await api.post('/posts/import-pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    })
    result.value = res.data
    ElMessage.success('导入成功！')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '导入失败')
  } finally {
    importing.value = false
  }
}

function resetForm() {
  file.value = null
  result.value = null
  category_id.value = null
  tag_ids.value = []
}
</script>

<style scoped>
.upload-area {
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  padding: 48px 24px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background: #fafafa;
}
.upload-area:hover {
  border-color: #06b6d4;
  background: #ecfeff;
}
.upload-area.dragover {
  border-color: #06b6d4;
  background: #cffafe;
  transform: scale(1.01);
}
.upload-icon {
  font-size: 48px;
  color: #94a3b8;
}
.hidden { display: none; }
</style>