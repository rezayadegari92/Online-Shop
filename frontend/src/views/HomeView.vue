<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section with Search -->
    <div class="bg-gradient-to-r from-gray-900 to-gray-700 text-white py-16">
      <div class="max-w-7xl mx-auto px-6">
        <h1 class="text-5xl font-bold mb-4 text-center">Welcome to Our Store</h1>
        <p class="text-xl mb-8 text-center text-gray-300">Find the best deals on electronics</p>
        
        <!-- Search Bar -->
        <div class="max-w-2xl mx-auto">
          <div class="relative">
            <input 
              v-model="searchQuery" 
              @keyup.enter="performSearch"
              type="text" 
              placeholder="Search for products..." 
              class="w-full px-6 py-4 rounded-full text-gray-900 text-lg focus:outline-none focus:ring-4 focus:ring-blue-300"
            />
            <button 
              @click="performSearch"
              class="absolute right-2 top-2 bg-blue-600 hover:bg-blue-700 text-white px-8 py-2 rounded-full font-semibold transition"
            >
              Search
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-8 space-y-12">
      <!-- Categories Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-800">Shop by Category</h2>
          <router-link to="/products" class="text-blue-600 hover:text-blue-800 font-semibold">View All →</router-link>
        </div>
        <div v-if="loadingCategories" class="text-center py-8">Loading categories...</div>
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-8 gap-4">
          <div 
            v-for="cat in categories" 
            :key="cat.id" 
            @click="filterByCategory(cat.id)"
            class="bg-white rounded-lg p-4 text-center cursor-pointer hover:shadow-lg transition group"
          >
            <div class="text-4xl mb-2">📱</div>
            <p class="text-sm font-semibold text-gray-700 group-hover:text-blue-600">{{ cat.name }}</p>
          </div>
        </div>
      </section>

      <!-- Discounted Products Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-800">🔥 Hot Deals</h2>
          <router-link to="/products?discounted=true" class="text-blue-600 hover:text-blue-800 font-semibold">View All →</router-link>
        </div>
        <div v-if="loadingDiscounted" class="text-center py-8">Loading deals...</div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <ProductCard 
            v-for="p in discountedProducts.slice(0, 5)" 
            :key="p.id" 
            :product="p"
            @add-to-cart="addToCart"
          />
        </div>
      </section>

      <!-- Brands Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-800">Popular Brands</h2>
        </div>
        <div v-if="loadingBrands" class="text-center py-8">Loading brands...</div>
        <div v-else class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 lg:grid-cols-10 gap-4">
          <div 
            v-for="brand in brands" 
            :key="brand.id"
            @click="filterByBrand(brand.id)"
            class="bg-white rounded-lg p-4 flex items-center justify-center cursor-pointer hover:shadow-lg transition border-2 border-transparent hover:border-blue-500"
          >
            <img v-if="brand.image" :src="brand.image" :alt="brand.name" class="h-12 object-contain" />
            <span v-else class="text-sm font-semibold text-gray-700">{{ brand.name }}</span>
          </div>
        </div>
      </section>

      <!-- Top Rated Products Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-800">⭐ Top Rated Products</h2>
          <router-link to="/products?sort=rating" class="text-blue-600 hover:text-blue-800 font-semibold">View All →</router-link>
        </div>
        <div v-if="loadingTopRated" class="text-center py-8">Loading top rated...</div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <ProductCard 
            v-for="p in topRatedProducts.slice(0, 5)" 
            :key="p.id" 
            :product="p"
            @add-to-cart="addToCart"
          />
        </div>
      </section>

      <!-- All Products Section -->
      <section>
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-3xl font-bold text-gray-800">All Products</h2>
          <router-link to="/products" class="text-blue-600 hover:text-blue-800 font-semibold">View All →</router-link>
        </div>
        <div v-if="loadingProducts" class="text-center py-8">Loading products...</div>
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <ProductCard 
            v-for="p in allProducts.slice(0, 10)" 
            :key="p.id" 
            :product="p"
            @add-to-cart="addToCart"
          />
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../utils/http'
import { useCartStore } from '../stores/cart.store'
import ProductCard from '../components/ProductCard.vue'

const router = useRouter()
const cart = useCartStore()

const searchQuery = ref('')
const categories = ref<any[]>([])
const brands = ref<any[]>([])
const discountedProducts = ref<any[]>([])
const topRatedProducts = ref<any[]>([])
const allProducts = ref<any[]>([])

const loadingCategories = ref(true)
const loadingBrands = ref(true)
const loadingDiscounted = ref(true)
const loadingTopRated = ref(true)
const loadingProducts = ref(true)

onMounted(async () => {
  loadCategories()
  loadBrands()
  loadDiscountedProducts()
  loadTopRatedProducts()
  loadAllProducts()
})

async function loadCategories() {
  try {
    const { data } = await api.get('/api/categories/')
    categories.value = data.slice(0, 8)
  } finally {
    loadingCategories.value = false
  }
}

async function loadBrands() {
  try {
    const { data } = await api.get('/api/brands/')
    brands.value = data.slice(0, 10)
  } finally {
    loadingBrands.value = false
  }
}

async function loadDiscountedProducts() {
  try {
    const { data } = await api.get('/api/discounted-products/')
    discountedProducts.value = data
  } finally {
    loadingDiscounted.value = false
  }
}

async function loadTopRatedProducts() {
  try {
    const { data } = await api.get('/api/products/top-rated/')
    topRatedProducts.value = data
  } finally {
    loadingTopRated.value = false
  }
}

async function loadAllProducts() {
  try {
    const { data } = await api.get('/api/products/')
    allProducts.value = data.results || data
  } finally {
    loadingProducts.value = false
  }
}

function performSearch() {
  if (searchQuery.value.trim()) {
    router.push(`/products?search=${encodeURIComponent(searchQuery.value)}`)
  }
}

function filterByCategory(categoryId: number) {
  router.push(`/products?category=${categoryId}`)
}

function filterByBrand(brandId: number) {
  router.push(`/products?brand=${brandId}`)
}

async function addToCart(productId: number) {
  try {
    await cart.add(productId, 1)
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

