<template>
  <div>
    <div class="mb-6">
      <h2 class="text-xl font-bold text-slate-800">评论管理</h2>
      <p class="text-sm text-slate-400 mt-0.5">审核与管理读者评论</p>
    </div>

    <el-card class="rounded-2xl" shadow="sm">
      <el-table :data="list" stripe v-loading="loading" size="large">
        <el-table-column prop="content" label="评论内容" min-width="350" show-overflow-tooltip>
          <template #default="{ row }">
            <div class="flex items-start gap-3">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-violet-500 flex items-center justify-center text-white text-xs font-bold flex-shrink-0 mt-0.5">
                {{ (row.nickname || '?')[0] }}
              </div>
              <div>
                <div class="text-sm text-slate-700">{{ row.content }}</div>
                <div class="text-xs text-slate-400 mt-1">{{ row.nickname }} &middot; 文章 #{{ row.post_id }}</div>
              </div>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="110" align="center">
          <template #default="{ row }">
            <el-tag :type="row.is_approved ? 'success' : 'warning'" size="small" effect="light" round>
              {{ row.is_approved ? '已审核' : '待审核' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="时间" width="170">
          <template #default="{ row }">{{ formatDate(row.created_at) }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button v-if="!row.is_approved" size="small" type="success" round class="rounded-lg" @click="handleApprove(row.id)">审核通过</el-button>
            <el-popconfirm title="确定删除该评论？" @confirm="handleDelete(row.id)">
              <template #reference><el-button size="small" type="danger" round class="rounded-lg">删除</el-button></template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <div class="flex justify-center mt-6" v-if="totalPages > 1">
        <el-pagination background layout="prev, pager, next" :total="total" :page-size="pageSize"
          v-model:current-page="page" @current-change="loadData" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { api } from '../stores/auth'

const list = ref([]), total = ref(0), page = ref(1), pageSize = 20, loading = ref(false)
const totalPages = computed(() => Math.ceil(total.value / pageSize))

function formatDate(d) { if (!d) return ''; return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) }

async function loadData() {
  loading.value = true
  try { const r = await api.get('/comments', { params: { page: page.value, page_size: pageSize } }); list.value = r.data.items; total.value = r.data.total }
  finally { loading.value = false }
}

async function handleApprove(id) { await api.put('/comments/' + id, { is_approved: true }); ElMessage.success('已审核通过'); loadData() }
async function handleDelete(id) { await api.delete('/comments/' + id); ElMessage.success('删除成功'); loadData() }
onMounted(loadData)
</script>
