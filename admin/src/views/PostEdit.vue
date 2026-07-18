<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>


    <!-- Edit / Preview tabs for non-PDF content -->
    <div v-if="!isPdfImport" class="flex items-center gap-2 mb-4">
      <div class="flex bg-slate-100 rounded-xl p-1">
        <button @click="mode = 'edit'"
          class="px-4 py-1.5 text-sm font-medium rounded-lg transition-all"
          :class="mode === 'edit' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'">
          <svg class="w-4 h-4 inline-block mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
          ??
        </button>
        <button @click="mode = 'preview'"
          class="px-4 py-1.5 text-sm font-medium rounded-lg transition-all"
          :class="mode === 'preview' ? 'bg-white text-slate-800 shadow-sm' : 'text-slate-500 hover:text-slate-700'">
          <svg class="w-4 h-4 inline-block mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
          ??
        </button>
      </div>
      <!-- Image upload button -->
      <button @click="openImageUpload"
        class="px-3 py-1.5 text-sm font-medium rounded-xl border border-slate-300 text-slate-600 hover:bg-slate-100 hover:border-slate-400 transition-all flex items-center gap-1.5">
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
        ????
      </button>
      <span v-if="uploading" class="text-xs text-slate-400">???...</span>
      <input ref="fileInput" type="file" accept="image/*" class="hidden" @change="handleImageUpload" />
    </div>

    <el-alert
      v-if="isPdfImport"
      title="此文章由 PDF 导入"
      type="warning"
      :closable="false"
      show-icon
      class="mb-4"
    >
      <template #default>
        内容以图片形式展示，下方为提取的纯文本（仅作参考，不可编辑）
      </template>
    </el-alert>
    <el-card>
      <el-form :model="form" label-width="80" v-loading="saving">
        <el-form-item label="标题">
          <el-input v-model="form.title" placeholder="文章标题" />
        </el-form-item>
        <el-form-item label="链接">
          <el-input v-model="form.slug" placeholder="url-slug" />
        </el-form-item>
        <el-form-item label="摘要">
          <el-input v-model="form.summary" type="textarea" :rows="2" placeholder="文章摘要" />
        </el-form-item>

        <!-- PDF Import: Show image preview -->
        <el-form-item v-if="isPdfImport" label="预览">
          <div class="pdf-preview border rounded-lg p-4 bg-gray-50 max-h-[600px] overflow-y-auto" v-html="contentHtml"></div>
        </el-form-item>

        <!-- PDF Import: Read-only text reference -->
        <el-form-item v-if="isPdfImport" label="文本">
          <el-input :model-value="form.content" type="textarea" :rows="8" disabled placeholder="PDF 提取的纯文本（仅参考）" />
        </el-form-item>

        <!-- Normal:         <!-- Normal: Editable content with preview toggle -->
        <el-form-item v-else label="内容">
          <div v-show="mode === 'edit'">
            <el-input v-model="form.content" type="textarea" :rows="16" placeholder="支持 Markdown 语法" style="width: 100%" />
          </div>
          <div v-show="mode === 'preview'" class="preview-panel border rounded-lg p-5 bg-white min-h-[300px] max-h-[600px] overflow-y-auto prose prose-sm max-w-none prose-headings:text-slate-800 prose-a:text-blue-600 prose-strong:text-slate-700 prose-code:text-blue-500 prose-pre:bg-slate-800 prose-pre:text-slate-100 prose-blockquote:border-blue-400 prose-blockquote:text-slate-500 prose-img:rounded-lg">
            <div v-if="form.content" v-html="renderedPreview"></div>
            <div v-else class="text-slate-400 text-center py-16">
              <svg class="w-12 h-12 mx-auto mb-3 text-slate-300" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"/></svg>
              <p class="mt-2">??????????????</p>
            </div>
          </div>
        </el-form-item>        <el-form-item label="标签">
          <div class="flex gap-2 w-full">
            <el-select v-model="form.tag_ids" multiple filterable clearable placeholder="搜索或选择已有标签" class="flex-1">
              <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id" />
            </el-select>
            <el-popover placement="bottom" trigger="click" width="240" @show="newTagName = ''">
              <template #reference>
                <el-button :icon="Plus" circle size="small" class="mt-[2px]" />
              </template>
              <div class="p-2">
                <p class="text-sm text-slate-500 mb-2">新建标签</p>
                <el-input v-model="newTagName" placeholder="输入标签名称" size="small" clearable
                  @keyup.enter="confirmCreateTag" />
                <el-button type="primary" size="small" class="mt-2 w-full" @click="confirmCreateTag" :loading="creatingTag">
                  创建
                </el-button>
              </div>
            </el-popover>
          </div>
        </el-form-item>
        <el-form-item label="封面">
          <el-input v-model="form.cover_image" placeholder="封面图片链接" />
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="form.is_published">发布</el-checkbox>
          <el-checkbox v-model="form.is_top" class="ml-4">置顶</el-checkbox>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
          <el-button @click="$router.back()">取消</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>
<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { api } from '../stores/auth'
import { marked } from 'marked'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const creatingTag = ref(false)
const categories = ref([])
const tags = ref([])
const newTagName = ref('')
const mode = ref('edit')
const fileInput = ref(null)
const contentHtml = ref('')
const uploading = ref(false)
const form = ref({ title: '', slug: '', summary: '', content: '', category_id: null, tag_ids: [], cover_image: '', is_published: false, is_top: false })

const renderedPreview = computed(() => {
  if (!form.value.content) return ''
  try {
    return marked(form.value.content, { breaks: true, gfm: true })
  } catch (e) {
    return '<p class="text-red-500">????</p>'
  }
})

const isPdfImport = computed(() => {
  return !!(contentHtml.value && contentHtml.value.indexOf('<div class="pdf-page">') !== -1)
})

onMounted(async () => {
  const [catRes, tagRes] = await Promise.all([api.get('/categories'), api.get('/tags')])
  categories.value = catRes.data
  tags.value = tagRes.data
  if (isEdit.value) {
    const res = await api.get('/posts/detail/' + route.params.id)
    const post = res.data
    contentHtml.value = post.content_html || ''
    form.value = { title: post.title, slug: post.slug, summary: post.summary || '', content: post.content,
      category_id: post.category?.id || null, tag_ids: post.tags?.map(t => t.id) || [],
      cover_image: post.cover_image || '', is_published: post.is_published, is_top: post.is_top, }
  }
})

function openImageUpload() {
  if (fileInput.value) fileInput.value.click()
}

async function handleImageUpload(e) {
  const file = e.target?.files?.[0]
  if (!file) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('file', file)
    const res = await api.post('/posts/upload-image', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    const url = res.data.url
    const markdownImg = '![' + file.name + '](' + url + ')'
    form.value.content = (form.value.content || '') + '\n' + markdownImg + '\n'
    ElMessage.success('?????')
  } catch (e) {
    ElMessage.error('??????')
  } finally {
    uploading.value = false
    e.target.value = ''
  }
}

async function handleSave() {
  saving.value = true
  try {
    if (isEdit.value) { await api.put('/posts/' + route.params.id, form.value); ElMessage.success('更新成功') }
    else { await api.post('/posts', form.value); ElMessage.success('创建成功') }
    router.push('/posts')
  } catch (e) { ElMessage.error(e.response?.data?.detail || '保存失败') }
  finally { saving.value = false }
}

async function confirmCreateTag() {
  const name = newTagName.value?.trim()
  if (!name) return
  if (tags.value.some(t => t.name === name)) {
    const existing = tags.value.find(t => t.name === name)
    if (existing && !form.value.tag_ids.includes(existing.id)) {
      form.value.tag_ids.push(existing.id)
    }
    newTagName.value = ''
    return
  }
  creatingTag.value = true
  try {
    const res = await api.post('/tags', { name, slug: name })
    const tagRes = await api.get('/tags')
    tags.value = tagRes.data
    if (res.data?.id) form.value.tag_ids.push(res.data.id)
    ElMessage.success('\u6807\u7b7e "' + name + '" \u5df2\u521b\u5efa')
    newTagName.value = ''
  } catch (e) { ElMessage.error(e.response?.data?.detail || '\u521b\u5efa\u6807\u7b7e\u5931\u8d25') }
  finally { creatingTag.value = false }
}

</script>

<style scoped>
.pdf-preview {
  width: 100%;
  background: #f9fafb;
}
.pdf-preview :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  margin-bottom: 1rem;
}
.pdf-preview :deep(.pdf-download) {
  margin-top: 1.5rem;
  padding-top: 1rem;
  border-top: 1px solid #e2e8f0;
}
.preview-panel {
  background: #ffffff;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}
</style>
