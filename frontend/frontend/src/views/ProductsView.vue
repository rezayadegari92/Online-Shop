<template>
  <div class="max-w-7xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Products</h1>
    <div v-if="loading" class="text-center py-12">Loading...</div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="p in products" :key="p.id" class="group bg-white rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300">
        <router-link :to="`/products/${p.id}`" class="block">
          <div class="relative overflow-hidden bg-gray-100">
            <img :src="p.images?.[0]?.image_url || placeholder" class="w-full h-56 object-cover group-hover:scale-110 transition-transform duration-300" alt="" />
            <div v-if="p.discount_percent > 0" class="absolute top-2 right-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold">
              -{{ p.discount_percent }}%
            </div>
          </div>
          <div class="p-4">
            <h3 class="font-semibold text-lg mb-2 truncate group-hover:text-blue-600 transition">{{ p.name }}</h3>
            <div class="flex items-center gap-2 mb-2">
              <span class="text-xl font-bold">{{ currency(p.discounted_price ?? p.price) }}</span>
              <span v-if="p.discount_percent > 0" class="text-sm text-gray-400 line-through">{{ currency(p.price) }}</span>
            </div>
            <div class="flex items-center gap-1 text-yellow-500 text-sm">
              <span>★</span>
              <span>{{ p.avg_rating || 'N/A' }}</span>
            </div>
          </div>
        </router-link>
        <div class="p-4 pt-0">
          <button class="w-full btn" @click="addToCart(p.id)">Add to Cart</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../utils/http'
import { useCartStore } from '../stores/cart.store'
import { useAuthStore } from '../stores/auth.store'

const loading = ref(true)
const products = ref<any[]>([])
const placeholder = 'https://placehold.co/600x400?text=No+Image'
const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)
}

async function loadProducts() {
  loading.value = true
  try {
    let url = '/api/products/'
    
    // If brand filter is applied, use the brand-specific endpoint
    if (route.query.brand) {
      url = `/api/brands/${route.query.brand}/products/`
      const { data } = await api.get(url)
      products.value = data.results || data
    } else {
      // Otherwise use the regular products endpoint with filters
      const params = new URLSearchParams()
      
      if (route.query.search) params.append('search', route.query.search as string)
      if (route.query.category) params.append('category', route.query.category as string)
      
      const queryString = params.toString()
      url = queryString ? `/api/products/?${queryString}` : '/api/products/'
      
      const { data } = await api.get(url)
      products.value = data.results || data
    }
  } finally {
    loading.value = false
  }
}

onMounted(loadProducts)

// Reload when query parameters change
watch(() => route.query, loadProducts)

async function addToCart(id: number) {
  try {
    await cart.add(id, 1)
  } catch (e: any) {
    if (e.response?.status === 401) {
      alert('Please log in to add items to cart')
      router.push('/login')
    } else {
      alert(e.response?.data?.detail || 'Failed to add to cart')
    }
  }
}
</script>

<style scoped>
.btn { @apply bg-gradient-to-r from-black to-gray-800 text-white rounded-lg px-4 py-2 hover:from-gray-800 hover:to-black transition font-semibold; }
</style>
