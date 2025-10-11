<template>
  <nav class="sticky top-0 z-30 border-b border-gray-200 dark:border-gray-700 bg-white/95 dark:bg-gray-900/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 dark:supports-[backdrop-filter]:bg-gray-900/80 shadow-sm dark:shadow-gray-800">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <router-link to="/" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        OnlineShop
      </router-link>
      <div class="flex items-center gap-6">
        <router-link to="/" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Home</router-link>
        <router-link to="/products" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Products</router-link>
        <router-link v-if="auth.isAuthenticated" to="/orders" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Orders</router-link>
        <router-link v-if="auth.isAuthenticated" to="/profile" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Profile</router-link>
        <router-link v-if="!auth.isAuthenticated" to="/login" class="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition font-medium">Login</router-link>
        <router-link v-if="!auth.isAuthenticated" to="/signup" class="px-4 py-2 bg-black dark:bg-white text-white dark:text-black rounded-lg hover:bg-gray-800 dark:hover:bg-gray-200 transition font-medium">
          Register
        </router-link>
        <button v-if="auth.isAuthenticated" class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-800 transition font-medium" @click="logout">
          Logout
        </button>
        
        <!-- Dark Mode Toggle -->
        <button 
          @click="theme.toggleTheme()" 
          class="p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition-all duration-300"
          :title="theme.isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
        >
          <!-- Sun Icon (shown in dark mode) -->
          <svg v-if="theme.isDark" class="w-6 h-6 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
          </svg>
          <!-- Moon Icon (shown in light mode) -->
          <svg v-else class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
          </svg>
        </button>
        
        <!-- Cart Button -->
        <button class="relative p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-full transition" @click="cart.toggle()">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <span v-if="cart.items.length > 0" class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold">
            {{ cart.items.length }}
          </span>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useAuthStore } from '../../stores/auth.store'
import { useCartStore } from '../../stores/cart.store'
import { useThemeStore } from '../../stores/theme.store'

const auth = useAuthStore()
const cart = useCartStore()
const theme = useThemeStore()

async function logout() {
  await auth.logout()
  window.location.href = '/login'
}

onMounted(() => {
  if (auth.isAuthenticated) {
    cart.load()
  }
})
</script>
