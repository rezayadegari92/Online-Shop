<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
    <!-- Hero Section with Search -->
    <div class="relative overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
      <!-- Animated Background Elements -->
      <div class="absolute inset-0 bg-pattern opacity-20"></div>
      
      <!-- Floating Elements -->
      <div class="absolute top-20 left-10 w-20 h-20 bg-gradient-to-br from-blue-400 to-purple-500 rounded-full opacity-20 animate-pulse"></div>
      <div class="absolute top-40 right-20 w-16 h-16 bg-gradient-to-br from-pink-400 to-red-500 rounded-full opacity-30 animate-bounce"></div>
      <div class="absolute bottom-20 left-1/4 w-12 h-12 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full opacity-25 animate-pulse delay-1000"></div>
      
      <div class="relative max-w-7xl mx-auto px-6 py-20 lg:py-32">
        <div class="text-center">
          <!-- Main Heading with Animation -->
          <div class="animate-fade-in-up">
            <h1 class="text-6xl lg:text-7xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-100 to-purple-200 mb-6 leading-tight">
              Discover Amazing
              <span class="block text-gradient bg-gradient-to-r from-blue-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
                Products
              </span>
            </h1>
          </div>
          
          <div class="animate-fade-in-up delay-200">
            <p class="text-xl lg:text-2xl text-blue-100 mb-12 max-w-3xl mx-auto leading-relaxed">
              Experience the future of shopping with our curated collection of premium electronics and innovative gadgets
            </p>
          </div>
          
          <!-- Enhanced Search Bar -->
          <div class="animate-fade-in-up delay-400 max-w-3xl mx-auto">
            <div class="relative group">
              <div class="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl blur opacity-75 group-hover:opacity-100 transition duration-300"></div>
              <div class="relative bg-white/10 backdrop-blur-md rounded-2xl p-2 border border-white/20">
                <div class="flex items-center">
                  <div class="flex-1 relative">
                    <svg class="absolute left-4 top-1/2 transform -translate-y-1/2 w-6 h-6 text-white/70" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                    </svg>
                    <input 
                      v-model="searchQuery" 
                      @keyup.enter="performSearch"
                      type="text" 
                      placeholder="Search for amazing products..." 
                      class="w-full pl-12 pr-4 py-4 bg-transparent text-white placeholder-white/70 text-lg focus:outline-none"
                    />
                  </div>
                  <button 
                    @click="performSearch"
                    class="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-8 py-4 rounded-xl font-semibold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5M6 12h12"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Stats Section -->
          <div class="animate-fade-in-up delay-600 mt-16 grid grid-cols-2 lg:grid-cols-4 gap-8 max-w-4xl mx-auto">
            <div class="text-center">
              <div class="text-3xl lg:text-4xl font-bold text-white mb-2">10K+</div>
              <div class="text-blue-200 text-sm lg:text-base">Happy Customers</div>
            </div>
            <div class="text-center">
              <div class="text-3xl lg:text-4xl font-bold text-white mb-2">5K+</div>
              <div class="text-blue-200 text-sm lg:text-base">Products</div>
            </div>
            <div class="text-center">
              <div class="text-3xl lg:text-4xl font-bold text-white mb-2">50+</div>
              <div class="text-blue-200 text-sm lg:text-base">Brands</div>
            </div>
            <div class="text-center">
              <div class="text-3xl lg:text-4xl font-bold text-white mb-2">24/7</div>
              <div class="text-blue-200 text-sm lg:text-base">Support</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Wave Separator -->
      <div class="absolute bottom-0 left-0 right-0">
        <svg class="w-full h-20 text-slate-50" fill="currentColor" viewBox="0 0 1200 120" preserveAspectRatio="none">
          <path d="M321.39,56.44c58-10.79,114.16-30.13,172-41.86,82.39-16.72,168.19-17.73,250.45-.39C823.78,31,906.67,72,985.66,92.83c70.05,18.48,146.53,26.09,214.34,3V0H0V27.35A600.21,600.21,0,0,0,321.39,56.44Z"></path>
        </svg>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-16 space-y-20">
      <!-- Categories Section -->
      <section class="animate-fade-in-up">
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent mb-4">
            Shop by Category
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Explore our carefully curated categories to find exactly what you're looking for
          </p>
        </div>
        
        <div v-if="loadingCategories" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent"></div>
        </div>
        
        <div v-else class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6">
          <div 
            v-for="(cat, index) in categories" 
            :key="cat.id" 
            @click="filterByCategory(cat.id)"
            class="group cursor-pointer transform transition-all duration-300 hover:scale-105"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <div class="relative bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 overflow-hidden">
              <!-- Gradient Background -->
              <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              
              <!-- Icon Container -->
              <div class="relative z-10 mb-4 flex justify-center">
                <div class="w-16 h-16 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl flex items-center justify-center text-white text-2xl font-bold shadow-lg group-hover:shadow-xl transition-all duration-300 transform group-hover:rotate-6">
                  {{ getCategoryIcon(cat.name) }}
                </div>
              </div>
              
              <!-- Category Name -->
              <div class="relative z-10 text-center">
                <h3 class="font-bold text-gray-800 group-hover:text-blue-600 transition-colors duration-300 text-sm lg:text-base">
                  {{ cat.name }}
                </h3>
              </div>
              
              <!-- Hover Effect -->
              <div class="absolute bottom-0 left-0 right-0 h-1 bg-gradient-to-r from-blue-500 to-purple-600 transform scale-x-0 group-hover:scale-x-100 transition-transform duration-300"></div>
            </div>
          </div>
        </div>
        
        <div class="text-center mt-12">
          <router-link 
            to="/products" 
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            View All Categories
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5M6 12h12"></path>
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Hot Deals Section -->
      <section class="animate-fade-in-up">
        <div class="relative bg-gradient-to-r from-red-500 via-pink-500 to-orange-500 rounded-3xl p-8 lg:p-12 text-white overflow-hidden">
          <!-- Background Pattern -->
          <div class="absolute inset-0 bg-pattern-circles opacity-20"></div>
          
          <div class="relative z-10">
            <div class="flex flex-col lg:flex-row items-center justify-between mb-8">
              <div>
                <h2 class="text-4xl lg:text-5xl font-bold mb-4 flex items-center">
                  🔥 Hot Deals
                  <span class="ml-4 bg-white/20 backdrop-blur-sm px-4 py-2 rounded-full text-lg font-medium">
                    Limited Time
                  </span>
                </h2>
                <p class="text-xl text-white/90 max-w-2xl">
                  Don't miss out on these incredible deals! Save up to 70% on selected items
                </p>
              </div>
              <router-link 
                to="/products?discounted=true" 
                class="bg-white text-red-500 hover:bg-red-50 px-8 py-4 rounded-2xl font-bold transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl mt-4 lg:mt-0"
              >
                View All Deals →
              </router-link>
            </div>
            
            <div v-if="loadingDiscounted" class="flex justify-center py-16">
              <div class="animate-spin rounded-full h-16 w-16 border-4 border-white border-t-transparent"></div>
            </div>
            
            <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
              <div 
                v-for="(p, index) in discountedProducts.slice(0, 5)" 
                :key="p.id"
                class="animate-slide-up"
                :style="{ animationDelay: `${index * 100}ms` }"
              >
                <ProductCard 
                  :product="p"
                  @add-to-cart="addToCart"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Brands Section -->
      <section class="animate-fade-in-up">
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-gray-900 via-blue-800 to-purple-800 bg-clip-text text-transparent mb-4">
            Popular Brands
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Shop from the world's most trusted and innovative brands
          </p>
        </div>
        
        <div v-if="loadingBrands" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-blue-500 border-t-transparent"></div>
        </div>
        
        <div v-else class="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 lg:grid-cols-8 gap-6">
          <div 
            v-for="(brand, index) in brands" 
            :key="brand.id"
            @click="filterByBrand(brand.id)"
            class="group cursor-pointer transform transition-all duration-300 hover:scale-110"
            :style="{ animationDelay: `${index * 50}ms` }"
          >
            <div class="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-blue-200 flex items-center justify-center h-24 relative overflow-hidden">
              <!-- Gradient Background -->
              <div class="absolute inset-0 bg-gradient-to-br from-blue-50 to-purple-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
              
              <div class="relative z-10">
                <img v-if="brand.image" :src="brand.image" :alt="brand.name" class="h-12 object-contain filter grayscale group-hover:grayscale-0 transition-all duration-300" />
                <span v-else class="text-sm font-bold text-gray-700 group-hover:text-blue-600 transition-colors duration-300">{{ brand.name }}</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Top Rated Products Section -->
      <section class="animate-fade-in-up">
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-yellow-600 via-orange-600 to-red-600 bg-clip-text text-transparent mb-4">
            ⭐ Top Rated Products
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Discover products loved by thousands of satisfied customers
          </p>
        </div>
        
        <div v-if="loadingTopRated" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-yellow-500 border-t-transparent"></div>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div 
            v-for="(p, index) in topRatedProducts.slice(0, 5)" 
            :key="p.id"
            class="animate-slide-up"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <ProductCard 
              :product="p"
              @add-to-cart="addToCart"
            />
          </div>
        </div>
        
        <div class="text-center mt-12">
          <router-link 
            to="/products?sort=rating" 
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            View All Top Rated
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5M6 12h12"></path>
            </svg>
          </router-link>
        </div>
      </section>

      <!-- Featured Products Section -->
      <section class="animate-fade-in-up">
        <div class="text-center mb-16">
          <h2 class="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-green-600 via-blue-600 to-purple-600 bg-clip-text text-transparent mb-4">
            Featured Products
          </h2>
          <p class="text-xl text-gray-600 max-w-2xl mx-auto">
            Handpicked selection of our most popular and innovative products
          </p>
        </div>
        
        <div v-if="loadingProducts" class="flex justify-center py-16">
          <div class="animate-spin rounded-full h-16 w-16 border-4 border-green-500 border-t-transparent"></div>
        </div>
        
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
          <div 
            v-for="(p, index) in allProducts.slice(0, 10)" 
            :key="p.id"
            class="animate-slide-up"
            :style="{ animationDelay: `${index * 100}ms` }"
          >
            <ProductCard 
              :product="p"
              @add-to-cart="addToCart"
            />
          </div>
        </div>
        
        <div class="text-center mt-12">
          <router-link 
            to="/products" 
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700 text-white font-semibold rounded-2xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
          >
            Explore All Products
            <svg class="ml-2 w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5-5 5M6 12h12"></path>
            </svg>
          </router-link>
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
    const items = Array.isArray(data) ? data : (data.results || [])
    categories.value = items.slice(0, 8)
  } catch (e) {
    console.error('Failed to load categories:', e)
    categories.value = []
  } finally {
    loadingCategories.value = false
  }
}

async function loadBrands() {
  try {
    const { data } = await api.get('/api/brands/')
    const items = Array.isArray(data) ? data : (data.results || [])
    brands.value = items.slice(0, 10)
  } catch (e) {
    console.error('Failed to load brands:', e)
    brands.value = []
  } finally {
    loadingBrands.value = false
  }
}

async function loadDiscountedProducts() {
  try {
    const { data } = await api.get('/api/discounted-products/')
    const items = Array.isArray(data) ? data : (data.results || [])
    discountedProducts.value = items
  } catch (e) {
    console.error('Failed to load discounted products:', e)
    discountedProducts.value = []
  } finally {
    loadingDiscounted.value = false
  }
}

async function loadTopRatedProducts() {
  try {
    const { data } = await api.get('/api/products/top-rated/')
    const items = Array.isArray(data) ? data : (data.results || [])
    topRatedProducts.value = items
  } catch (e) {
    console.error('Failed to load top rated products:', e)
    topRatedProducts.value = []
  } finally {
    loadingTopRated.value = false
  }
}

async function loadAllProducts() {
  try {
    const { data } = await api.get('/api/products/')
    const items = Array.isArray(data) ? data : (data.results || [])
    allProducts.value = items
  } catch (e) {
    console.error('Failed to load products:', e)
    allProducts.value = []
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

function getCategoryIcon(categoryName: string): string {
  const icons: { [key: string]: string } = {
    'Electronics': '📱',
    'Computers': '💻',
    'Phones': '📱',
    'Tablets': '📱',
    'Laptops': '💻',
    'Gaming': '🎮',
    'Audio': '🎧',
    'Cameras': '📷',
    'Accessories': '🔌',
    'Smart Home': '🏠',
    'Wearables': '⌚',
    'TV': '📺',
    'default': '🛍️'
  }
  
  // Find matching icon or use default
  for (const [key, icon] of Object.entries(icons)) {
    if (categoryName.toLowerCase().includes(key.toLowerCase())) {
      return icon
    }
  }
  return icons.default
}
</script>

<style scoped>
@keyframes fade-in-up {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slide-up {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in-up {
  animation: fade-in-up 0.8s ease-out forwards;
}

.animate-slide-up {
  animation: slide-up 0.6s ease-out forwards;
}

.delay-200 {
  animation-delay: 200ms;
}

.delay-400 {
  animation-delay: 400ms;
}

.delay-600 {
  animation-delay: 600ms;
}

.delay-1000 {
  animation-delay: 1000ms;
}

/* Custom gradient text animation */
.text-gradient {
  background-size: 200% 200%;
  animation: gradient-shift 3s ease-in-out infinite;
}

@keyframes gradient-shift {
  0%, 100% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
}

/* Floating animation for background elements */
@keyframes float {
  0%, 100% {
    transform: translateY(0px);
  }
  50% {
    transform: translateY(-20px);
  }
}

.animate-float {
  animation: float 6s ease-in-out infinite;
}

/* Enhanced hover effects */
.group:hover .transform {
  transform: scale(1.05) rotate(2deg);
}

/* Smooth scrolling */
html {
  scroll-behavior: smooth;
}

/* Custom scrollbar */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f5f9;
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(to bottom, #3b82f6, #8b5cf6);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(to bottom, #2563eb, #7c3aed);
}

/* Background patterns */
.bg-pattern {
  background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%239C92AC' fill-opacity='0.1'%3E%3Ccircle cx='30' cy='30' r='4'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

.bg-pattern-circles {
  background-image: url("data:image/svg+xml,%3Csvg width='40' height='40' viewBox='0 0 40 40' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Cpath d='M20 20c0-5.5-4.5-10-10-10s-10 4.5-10 10 4.5 10 10 10 10-4.5 10-10zm10 0c0-5.5-4.5-10-10-10s-10 4.5-10 10 4.5 10 10 10 10-4.5 10-10z'/%3E%3C/g%3E%3C/svg%3E");
}
</style>

