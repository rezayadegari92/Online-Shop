import { defineStore } from 'pinia'
import api from '../utils/http'

interface Tokens {
  access: string
  refresh: string
}

interface AuthState {
  user: any | null
  tokens: Tokens | null
  isBootstrapped: boolean
}

const ACCESS_KEY = 'os_access'
const REFRESH_KEY = 'os_refresh'

export const useAuthStore = defineStore('auth', {
  state: (): AuthState => ({ user: null, tokens: null, isBootstrapped: false }),
  getters: {
    isAuthenticated: (s) => !!s.tokens?.access,
  },
  actions: {
    async bootstrap() {
      const access = localStorage.getItem(ACCESS_KEY)
      const refresh = localStorage.getItem(REFRESH_KEY)
      if (access && refresh) {
        this.tokens = { access, refresh }
        try {
          const { data } = await api.get('/accounts/api/profile/')
          this.user = data
        } catch (e) {
          this.tokens = null
          localStorage.removeItem(ACCESS_KEY)
          localStorage.removeItem(REFRESH_KEY)
        }
      }
      this.isBootstrapped = true
    },
    setTokens(tokens: Tokens) {
      this.tokens = tokens
      localStorage.setItem(ACCESS_KEY, tokens.access)
      localStorage.setItem(REFRESH_KEY, tokens.refresh)
    },
    async login(payload: { email_or_username?: string; email?: string; username?: string; password: string }) {
      const { data } = await api.post('/accounts/api/login/', payload)
      this.setTokens({ access: data.access, refresh: data.refresh })
      const profile = await api.get('/accounts/api/profile/')
      this.user = profile.data
    },
    async logout() {
      try {
        await api.post('/accounts/api/logout/', { refresh: this.tokens?.refresh })
      } catch {}
      this.tokens = null
      this.user = null
      localStorage.removeItem(ACCESS_KEY)
      localStorage.removeItem(REFRESH_KEY)
    },
  },
})


