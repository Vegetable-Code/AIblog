import { defineStore } from 'pinia'
import axios from 'axios'

const api = axios.create({ baseURL: '/api/v1' })

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('frontend_token') || '',
    user: null,
    showLogin: false,
  }),
  getters: {
    isLoggedIn: (state) => !!state.token && !!state.user,
  },
  actions: {
    async login(username, password) {
      const form = new FormData()
      form.append('username', username)
      form.append('password', password)
      const res = await api.post('/auth/login', form)
      this.token = res.data.access_token
      localStorage.setItem('frontend_token', res.data.access_token)
      api.defaults.headers.common['Authorization'] = 'Bearer ' + res.data.access_token
      await this.fetchUser()
      return true
    },
    async register(username, email, password, nickname) {
      const res = await api.post('/auth/register', null, {
        params: { username, email, password, nickname: nickname || '' }
      })
      // Auto login after register
      await this.login(username, password)
      return true
    },
    async fetchUser() {
      if (!this.token) return
      api.defaults.headers.common['Authorization'] = 'Bearer ' + this.token
      try {
        const res = await api.get('/auth/me')
        this.user = res.data
      } catch (e) {
        this.logout()
      }
    },
    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('frontend_token')
      delete api.defaults.headers.common['Authorization']
    },
    openLogin() { this.showLogin = true },
    closeLogin() { this.showLogin = false },
  },
})

export { api }
