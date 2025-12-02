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
    allowedHosts: true,
    proxy: {
      '/api': {
        target: process.env.VITE_BACKEND_URL || 'http://online-shop-appcompose-c9sen2-f6ce07-95-216-121-248.traefik.me',
        changeOrigin: true,
        secure: false,
      },
      '/accounts': {
        target: process.env.VITE_BACKEND_URL || 'http://online-shop-appcompose-c9sen2-f6ce07-95-216-121-248.traefik.me',
        changeOrigin: true,
        secure: false,
      },
      '/media': {
        target: process.env.VITE_BACKEND_URL || 'http://online-shop-appcompose-c9sen2-f6ce07-95-216-121-248.traefik.me',
        changeOrigin: true,
        secure: false,
      }
    }
  }
})

