import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import Posts from '../views/Posts.vue'
import PostEdit from '../views/PostEdit.vue'
import Categories from '../views/Categories.vue'
import Tags from '../views/Tags.vue'
import Comments from '../views/Comments.vue'
import Users from '../views/Users.vue'
import Profile from '../views/Profile.vue'

const routes = [
  { path: '/login', name: 'Login', component: Login },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: Dashboard },
      { path: 'posts', name: 'Posts', component: Posts },
      { path: 'posts/create', name: 'PostCreate', component: PostEdit },
      { path: 'posts/:id/edit', name: 'PostEdit', component: PostEdit, props: true },
      { path: 'categories', name: 'Categories', component: Categories },
      { path: 'tags', name: 'Tags', component: Tags },
      { path: 'comments', name: 'Comments', component: Comments },
      { path: 'users', name: 'Users', component: Users },
      { path: 'profile', name: 'Profile', component: Profile },
    ],
  },
]

const router = createRouter({ history: createWebHistory('/admin/'), routes })

router.beforeEach(async (to, from, next) => {
  const token = localStorage.getItem('token')
  
  // 未登录 -> 跳转登录页
  if (to.path !== '/login' && !token) {
    next('/login')
    return
  }
  
  // 已登录访问登录页 -> 跳转仪表盘
  if (to.path === '/login' && token) {
    next('/dashboard')
    return
  }
  
  next()
})

export default router
