import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    user: null,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      const form = new FormData()
      form.append('username', username)
      form.append('password', password)
      const res = await api.post('/auth/login', form)
      this.token = res.data.access_token
      localStorage.setItem('token', res.data.access_token)
      api.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access_token
      await this.fetchUser()
    },
    async fetchUser() {
      if (!this.token) return
      api.defaults.headers.common['Authorization'] = 'Bearer ' + this.token
      const res = await api.get('/auth/me')
      this.user = res.data
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    },
  },
})

export { api }
