<template>
  <div>
    <h2 class="text-2xl font-bold mb-4">{{ isEdit ? '编辑文章' : '新建文章' }}</h2>
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
        <el-form-item label="内容">
          <el-input v-model="form.content" type="textarea" :rows="16" placeholder="支持 Markdown 格式" />
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="form.category_id" clearable placeholder="选择分类" class="w-full">
            <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="form.tag_ids" multiple clearable placeholder="选择标签" class="w-full">
            <el-option v-for="t in tags" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
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
import { api } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)
const saving = ref(false)
const categories = ref([])
const tags = ref([])
const form = ref({ title: '', slug: '', summary: '', content: '', category_id: null, tag_ids: [], cover_image: '', is_published: false, is_top: false })

onMounted(async () => {
  const [catRes, tagRes] = await Promise.all([api.get('/categories'), api.get('/tags')])
  categories.value = catRes.data
  tags.value = tagRes.data
  if (isEdit.value) {
    const res = await api.get('/posts/detail/' + route.params.id)
    const post = res.data
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
</script>
