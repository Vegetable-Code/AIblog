import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import PostDetail from '../views/PostDetail.vue'
import CategoriesView from '../views/CategoriesView.vue'
import AboutView from '../views/AboutView.vue'
import TagPostsView from '../views/TagPostsView.vue'
import PortfolioView from '../views/PortfolioView.vue'
import MahjongView from '../views/MahjongView.vue'

const routes = [
  { path: '/', name: 'Home', component: HomeView },
  { path: '/post/:slug', name: 'PostDetail', component: PostDetail },
  { path: '/categories', name: 'Categories', component: CategoriesView },
  { path: '/about', name: 'About', component: AboutView },
  { path: '/projects', name: 'Portfolio', component: PortfolioView },
  { path: '/mahjong', name: 'Mahjong', component: MahjongView },
  { path: '/tag/:slug', name: 'TagPosts', component: TagPostsView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
