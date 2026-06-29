<template>
  <div>
    <h2 class="text-2xl font-bold mb-6">仪表盘</h2>
    <div v-if="loading" class="text-center py-10 text-gray-400">加载中...</div>
    <div v-else>
      <el-row :gutter="20" class="mb-6">
        <el-col :span="6" v-for="item in stats" :key="item.label">
          <el-card shadow="hover" class="text-center">
            <div class="text-3xl font-bold" :style="{ color: item.color }">{{ item.value }}</div>
            <div class="text-sm text-gray-500 mt-2">{{ item.label }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-card>
        <template #header><span>最近文章</span></template>
        <el-table :data="recentPosts" stripe style="width: 100%">
          <el-table-column prop="title" label="标题" min-width="200" />
          <el-table-column prop="views_count" label="浏览量" width="100" />
          <el-table-column width="100">
            <template #default="{ row }"><el-tag :type="row.is_published ? 'success' : 'info'" size="small">{{ row.is_published ? '已发布' : '草稿' }}</el-tag></template>
          </el-table-column>
          <el-table-column label="时间" width="180">
            <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import { api } from '../stores/auth'
const loading = ref(true)
const stats = ref([])
const recentPosts = ref([])
function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleString('zh-CN') }
onMounted(async () => {
  try {
    const [s, p] = await Promise.all([api.get('/dashboard/stats'), api.get('/dashboard/recent_posts')])
    stats.value = [
      { label: '文章总数', value: s.data.post_count, color: '#409eff' },
      { label: '已发布', value: s.data.published_count, color: '#67c23a' },
      { label: '评论总数', value: s.data.comment_count, color: '#e6a23c' },
      { label: '待审核评论', value: s.data.pending_comment_count, color: '#f56c6c' },
    ]
    recentPosts.value = p.data
  } finally { loading.value = false }
})
</script>
