import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': 'http://localhost:8000',
      '/accounts': 'http://localhost:8000'
    }
  },
  preview: {
    port: 3000,
    host: '0.0.0.0',
    allowedHosts: 'all',
    proxy: {
      '/api': {
        target: 'http://web:8000',
        changeOrigin: true,
        secure: false,
      },
      '/accounts': {
        target: 'http://web:8000',
        changeOrigin: true,
        secure: false,
      },
      '/media': {
        target: 'http://web:8000',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})

