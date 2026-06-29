<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <h2 class="text-2xl font-bold">文章管理</h2>
      <div class="flex items-center gap-3">
        <el-button v-if="selectedIds.length > 0" type="danger" plain @click="handleBatchDelete">
          <el-icon class="mr-1"><Delete /></el-icon>
          批量删除 ({{ selectedIds.length }})
        </el-button>
        <el-button type="primary" @click="$router.push('/posts/create')">新建文章</el-button>
      </div>
    </div>
    <el-card>
      <el-table :data="posts" stripe v-loading="loading" style="width: 100%" @selection-change="handleSelectionChange">
        <el-table-column type="selection" width="50" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="分类" width="120">
          <template #default="{ row }">{{ row.category?.name || '-' }}</template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }"><el-tag :type="row.is_published ? 'success' : 'info'" size="small">{{ row.is_published ? '已发布' : '草稿' }}</el-tag></template>
        </el-table-column>
        <el-table-column prop="views_count" label="浏览" width="80" />
        <el-table-column label="时间" width="180">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push('/posts/' + row.id + '/edit')">编辑</el-button>
            <el-popconfirm title="确定删除？" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
      <div class="flex justify-center mt-4" v-if="totalPages > 1">
        <el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSize" v-model:current-page="page" @current-change="loadPosts" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { Delete } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { api } from '../stores/auth'

const posts = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 10
const loading = ref(false)
const selectedIds = ref([])

const totalPages = computed(() => Math.ceil(total.value / pageSize))

function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleString('zh-CN') }

async function loadPosts() {
  loading.value = true
  try {
    const res = await api.get('/posts', { params: { page: page.value, page_size: pageSize, published_only: false } })
    posts.value = res.data.items
    total.value = res.data.total
  } finally { loading.value = false }
}

async function handleDelete(id) {
  await api.delete('/posts/' + id)
  ElMessage.success('删除成功')
  loadPosts()
}

function handleSelectionChange(rows) {
  selectedIds.value = rows.map(r => r.id)
}

async function handleBatchDelete() {
  if (selectedIds.value.length === 0) return
  await api.post('/posts/batch-delete', { ids: selectedIds.value })
  ElMessage.success('批量删除成功')
  selectedIds.value = []
  loadPosts()
}

onMounted(loadPosts)
</script>