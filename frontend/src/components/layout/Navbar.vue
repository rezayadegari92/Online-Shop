<template>
  <nav class="sticky top-0 z-30 border-b bg-white/95 backdrop-blur supports-[backdrop-filter]:bg-white/80 shadow-sm">
    <div class="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
      <router-link to="/" class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
        OnlineShop
      </router-link>
      <div class="flex items-center gap-6">
        <router-link to="/" class="hover:text-blue-600 transition font-medium">Home</router-link>
        <router-link to="/products" class="hover:text-blue-600 transition font-medium">Products</router-link>
        <router-link v-if="auth.isAuthenticated" to="/orders" class="hover:text-blue-600 transition font-medium">Orders</router-link>
        <router-link v-if="auth.isAuthenticated" to="/profile" class="hover:text-blue-600 transition font-medium">Profile</router-link>
        <router-link v-if="!auth.isAuthenticated" to="/login" class="hover:text-blue-600 transition font-medium">Login</router-link>
        <router-link v-if="!auth.isAuthenticated" to="/signup" class="px-4 py-2 bg-black text-white rounded-lg hover:bg-gray-800 transition font-medium">
          Register
        </router-link>
        <button v-if="auth.isAuthenticated" class="px-4 py-2 border rounded-lg hover:bg-gray-50 transition font-medium" @click="logout">
          Logout
        </button>
        <button class="relative p-2 hover:bg-gray-100 rounded-full transition" @click="cart.toggle()">
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

const auth = useAuthStore()
const cart = useCartStore()

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
