import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

export const useAppStore = defineStore('app', {
  state: () => ({
    posts: [],
    total: 0,
    categories: [],
    tags: [],
    loading: false,
  }),
  actions: {
    async fetchPosts(params = {}) {
      this.loading = true
      try {
        const res = await api.get('/posts', { params })
        this.posts = res.data.items
        this.total = res.data.total
        return res.data
      } finally {
        this.loading = false
      }
    },
    async fetchCategories() {
      const res = await api.get('/categories')
      this.categories = res.data
    },
    async fetchTags() {
      const res = await api.get('/tags')
      this.tags = res.data
    },
  },
})
