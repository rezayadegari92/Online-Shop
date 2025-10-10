<template>
  <div class="max-w-7xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Products</h1>
      <div v-if="totalCount > 0" class="text-gray-600">
        Showing {{ products.length }} of {{ totalCount }} products
      </div>
    </div>
    
    <!-- Products Grid -->
    <div v-if="loading" class="text-center py-12">Loading...</div>
    <div v-else-if="products.length === 0" class="text-center py-12 text-gray-500">
      No products found
    </div>
    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
      <div v-for="p in products" :key="p.id" class="group bg-white rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300">
        <router-link :to="`/products/${p.id}`" class="block">
          <div class="relative overflow-hidden bg-white">
            <!-- Fixed size container for consistent image display -->
            <div class="w-full h-64 flex items-center justify-center bg-gray-50 p-2">
              <img 
                :src="p.images?.[0]?.image_url || placeholder" 
                class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300" 
                alt=""
              />
            </div>
            <div v-if="p.discount_percent > 0" class="absolute top-3 right-3 bg-red-500 text-white px-3 py-1.5 rounded-full text-sm font-bold shadow-lg">
              -{{ p.discount_percent }}%
            </div>
          </div>
          <div class="p-4 bg-white">
            <h3 class="font-bold text-base mb-2 text-gray-900 overflow-hidden" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; min-height: 3rem;">{{ p.name }}</h3>
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

    <!-- Pagination Controls -->
    <div v-if="totalCount > 0" class="mt-12 flex items-center justify-center space-x-4">
      <!-- Previous Button -->
      <button 
        @click="goToPreviousPage"
        :disabled="!hasPrevious || loading"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
        </svg>
        Previous
      </button>

      <!-- Page Info -->
      <div class="flex items-center space-x-2">
        <span class="text-sm text-gray-700">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
      </div>

      <!-- Next Button -->
      <button 
        @click="goToNextPage"
        :disabled="!hasNext || loading"
        class="flex items-center px-4 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 hover:text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        Next
        <svg class="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
        </svg>
      </button>
    </div>

    <!-- Page Size Selector -->
    <div v-if="totalCount > 0" class="mt-6 flex items-center justify-center">
      <label class="text-sm text-gray-700 mr-2">Items per page:</label>
      <select 
        v-model="pageSize" 
        @change="changePageSize"
        class="px-3 py-1 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../utils/http'
import { useCartStore } from '../stores/cart.store'
import { useAuthStore } from '../stores/auth.store'

const loading = ref(true)
const products = ref<any[]>([])
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const hasNext = ref(false)
const hasPrevious = ref(false)
const nextUrl = ref<string | null>(null)
const previousUrl = ref<string | null>(null)

const placeholder = 'https://placehold.co/600x400?text=No+Image'
const cart = useCartStore()
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

// Computed property for total pages
const totalPages = computed(() => Math.ceil(totalCount.value / pageSize.value))

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(n)
}

async function loadProducts() {
  loading.value = true
  try {
    let url = '/api/products/'
    
    // Build query parameters
    const params = new URLSearchParams()
    
    // Add pagination parameters
    if (route.query.page) params.append('page', route.query.page as string)
    params.append('page_size', pageSize.value.toString())
    
    // Add filter parameters
    if (route.query.search) params.append('search', route.query.search as string)
    if (route.query.category) params.append('category', route.query.category as string)
    if (route.query.brand) params.append('brand', route.query.brand as string)
    if (route.query.sort) params.append('sort', route.query.sort as string)
    
    // If brand filter is applied, use the brand-specific endpoint
    if (route.query.brand && !route.query.search && !route.query.category) {
      url = `/api/brands/${route.query.brand}/products/`
      // Remove brand param since it's in the URL path
      params.delete('brand')
    }
    
    const queryString = params.toString()
    url = queryString ? `${url}?${queryString}` : url
    
    const { data } = await api.get(url)
    
    // Handle paginated response
    if (data && typeof data === 'object' && 'results' in data) {
      products.value = data.results || []
      totalCount.value = data.count || 0
      hasNext.value = !!data.next
      hasPrevious.value = !!data.previous
      nextUrl.value = data.next
      previousUrl.value = data.previous
      
      // Extract current page from URL or use default
      currentPage.value = parseInt(route.query.page as string) || 1
    } else {
      // Handle non-paginated response (fallback)
      products.value = Array.isArray(data) ? data : []
      totalCount.value = products.value.length
      hasNext.value = false
      hasPrevious.value = false
      nextUrl.value = null
      previousUrl.value = null
      currentPage.value = 1
    }
  } catch (error) {
    console.error('Failed to load products:', error)
    products.value = []
    totalCount.value = 0
    hasNext.value = false
    hasPrevious.value = false
  } finally {
    loading.value = false
  }
}

// Initialize and load products
onMounted(() => {
  // Initialize page size from query params
  const pageSizeParam = route.query.page_size as string
  if (pageSizeParam) {
    pageSize.value = parseInt(pageSizeParam) || 10
  }
  
  // Load products
  loadProducts()
})

// Reload when query parameters change
watch(() => route.query, loadProducts)

function goToNextPage() {
  if (hasNext.value) {
    const nextPage = currentPage.value + 1
    router.push({
      query: { ...route.query, page: nextPage.toString() }
    })
  }
}

function goToPreviousPage() {
  if (hasPrevious.value && currentPage.value > 1) {
    const prevPage = currentPage.value - 1
    router.push({
      query: { ...route.query, page: prevPage.toString() }
    })
  }
}

function changePageSize() {
  router.push({
    query: { 
      ...route.query, 
      page_size: pageSize.value.toString(),
      page: '1' // Reset to first page when changing page size
    }
  })
}

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
