import axios from 'axios'
import { useAuthStore } from '../stores/auth.store'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '',
  timeout: 15000,
})

api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth.tokens?.access) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${auth.tokens.access}`
  }
  return config
})

let isRefreshing = false
let queue: Array<() => void> = []

api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const { response, config } = error
    const auth = useAuthStore()
    if (response?.status === 401 && auth.tokens?.refresh && !isRefreshing) {
      isRefreshing = true
      try {
        const { data } = await axios.post((import.meta.env.VITE_API_BASE_URL || '') + '/api/token/refresh/', {
          refresh: auth.tokens.refresh,
        })
        auth.setTokens({ access: data.access, refresh: auth.tokens.refresh })
        queue.forEach((cb) => cb())
        queue = []
        isRefreshing = false
        config.headers = config.headers || {}
        config.headers.Authorization = `Bearer ${auth.tokens.access}`
        return api(config)
      } catch (e) {
        isRefreshing = false
        auth.logout()
      }
    } else if (response?.status === 401 && isRefreshing) {
      await new Promise<void>((resolve) => queue.push(resolve))
      config.headers = config.headers || {}
      config.headers.Authorization = `Bearer ${useAuthStore().tokens?.access}`
      return api(config)
    }
    return Promise.reject(error)
  }
)

export default api


