<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
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

        <!-- Normal: Editable content -->
        <el-form-item v-else label="内容">
          <el-input v-model="form.content" type="textarea" :rows="16" placeholder="支持 Markdown 格式" />
        </el-form-item>

        <el-form-item label="分类">
          <el-select v-model="form.category_id" clearable placeholder="选择分类" class="w-full">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
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
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { api } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const creatingTag = ref(false)
const categories = ref([])
const tags = ref([])
const newTagName = ref('')
const contentHtml = ref('')
const form = ref({ title: '', slug: '', summary: '', content: '', category_id: null, tag_ids: [], cover_image: '', is_published: false, is_top: false })

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
</style>
