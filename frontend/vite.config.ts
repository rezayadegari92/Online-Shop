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
    proxy: {
      '/api': 'http://web:8000',
      '/accounts': 'http://web:8000',
      '/media': 'http://web:8000'
    }
  }
})

