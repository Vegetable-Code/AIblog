<template>
  <el-container class="min-h-screen bg-slate-50">
    <!-- Sidebar -->
    <el-aside width="240px" class="bg-white border-r border-slate-200 flex flex-col sticky top-0 h-screen">
      <!-- Logo -->
      <div class="h-16 flex items-center gap-3 px-5 border-b border-slate-100 flex-shrink-0">
        <div class="w-8 h-8 rounded-xl bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-cyan-500/20">AI</div>
        <div>
          <div class="text-sm font-bold text-slate-800 leading-tight">AI工程师</div>
          <div class="text-[10px] text-slate-400">内容管理后台</div>
        </div>
      </div>

      <!-- User Info -->
      <div class="px-5 py-4 border-b border-slate-100 flex-shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-br from-cyan-500 to-violet-500 flex items-center justify-center text-white text-sm font-bold shadow-sm">
            {{ (auth.user?.username || 'A')[0].toUpperCase() }}
          </div>
          <div>
            <div class="text-sm font-medium text-slate-700">{{ auth.user?.username || '加载中...' }}</div>
            <div class="text-xs text-slate-400">管理员</div>
          </div>
        </div>
      </div>

      <!-- Navigation -->
      <el-menu :default-active="route.path" router class="border-0 flex-1 overflow-y-auto py-2"
        :popper-class="'rounded-xl shadow-lg'">
        <el-menu-item index="/dashboard" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><DataAnalysis /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        <el-menu-item index="/posts" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><Document /></el-icon>
          <span>文章管理</span>
        </el-menu-item>
        <el-menu-item index="/categories" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><Folder /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/tags" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><PriceTag /></el-icon>
          <span>标签管理</span>
        </el-menu-item>
        <el-menu-item index="/comments" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><ChatDotSquare /></el-icon>
          <span>评论管理</span>
        </el-menu-item>
        <el-menu-item index="/users" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/profile" class="sidebar-link mx-2 rounded-xl my-0.5 h-10">
          <el-icon><Setting /></el-icon>
          <span>个人设置</span>
        </el-menu-item>
      </el-menu>

      <!-- Logout -->
      <div class="p-4 border-t border-slate-100 flex-shrink-0">
        <el-button class="w-full rounded-xl" plain size="small" @click="handleLogout">
          <el-icon class="mr-1.5"><SwitchButton /></el-icon>退出登录
        </el-button>
      </div>
    </el-aside>

    <!-- Main Content -->
    <el-container>
      <!-- Top Bar -->
      <el-header class="bg-white border-b border-slate-200 h-16 flex items-center justify-between px-6 sticky top-0 z-10">
        <div class="flex items-center gap-3">
          <h1 class="text-lg font-semibold text-slate-800">{{ pageTitle }}</h1>
          <el-tag size="small" effect="plain" round class="bg-cyan-50 text-cyan-600 border-cyan-200">v1.0</el-tag>
        </div>
        <div class="flex items-center gap-4 text-sm text-slate-400">
          <el-tooltip content="数据每 30 秒自动刷新" placement="bottom">
            <span class="flex items-center gap-1.5 cursor-default">
              <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              系统运行中
            </span>
          </el-tooltip>
        </div>
      </el-header>

      <!-- Page Content -->
      <el-main class="p-6">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SwitchButton } from '@element-plus/icons-vue'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const pageTitle = computed(() => {
  const titles = {
    '/dashboard': '仪表盘',
    '/posts': '文章管理',
    '/posts/create': '新建文章',
    '/categories': '分类管理',
    '/tags': '标签管理',
    '/comments': '评论管理',
    '/users': '用户管理',
    '/profile': '个人设置',
  }
  // Check for edit route
  if (route.path.match(/^\/posts\/\d+\/edit$/)) return '编辑文章'
  return titles[route.path] || '管理后台'
})

onMounted(() => {
  if (!auth.user) auth.fetchUser()
})

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
