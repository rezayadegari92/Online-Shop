<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header Section -->
      <div class="text-center mb-12 animate-fadeIn">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-3">
          My Orders
        </h1>
        <p class="text-gray-600">Track and manage your purchase history</p>
      </div>
      
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-20">
        <div class="relative">
          <div class="w-16 h-16 border-4 border-blue-200 rounded-full animate-spin border-t-blue-600"></div>
          <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full animate-pulse"></div>
          </div>
        </div>
      </div>
      
      <!-- Empty State -->
      <div v-else-if="orders.length === 0" class="text-center py-20 animate-fadeIn">
        <div class="inline-block p-8 bg-white rounded-full shadow-lg mb-6 transform hover:scale-110 transition-transform duration-300">
          <svg class="w-20 h-20 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
        </div>
        <h3 class="text-2xl font-semibold text-gray-700 mb-2">No orders yet</h3>
        <p class="text-gray-500 mb-6">Start shopping to see your orders here!</p>
        <router-link to="/products" class="inline-block px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-300">
          Browse Products
        </router-link>
      </div>
      
      <!-- Orders List -->
      <div v-else class="space-y-6">
        <div 
          v-for="(o, index) in orders" 
          :key="o.id" 
          class="order-card group bg-white rounded-2xl overflow-hidden shadow-lg hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1"
          :style="{ animationDelay: `${index * 100}ms` }"
        >
          <!-- Order Header with Gradient -->
          <div class="relative bg-gradient-to-r from-blue-600 to-purple-600 p-6 text-white">
            <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32 transform group-hover:scale-150 transition-transform duration-700"></div>
            
            <div class="relative flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="w-14 h-14 bg-white bg-opacity-20 backdrop-blur-sm rounded-full flex items-center justify-center animate-bounce-slow">
                  <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
                  </svg>
                </div>
                <div>
                  <h3 class="text-2xl font-bold">Order #{{ o.id }}</h3>
                  <p class="text-blue-100 text-sm flex items-center">
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {{ formatDate(o.created_at) }}
                  </p>
                </div>
              </div>
              
              <div class="text-right">
                <div class="text-3xl font-bold mb-2">{{ formatPrice(o.total_price) }}</div>
                <span class="inline-block px-4 py-1.5 rounded-full text-xs font-semibold backdrop-blur-sm" :class="getStatusBadge(o.status)">
                  {{ o.status }}
                </span>
              </div>
            </div>
          </div>
          
          <!-- Order Progress Bar -->
          <div class="relative h-2 bg-gray-200">
            <div 
              class="absolute h-full bg-gradient-to-r from-blue-500 to-purple-500 transition-all duration-1000 ease-out"
              :style="{ width: getProgressWidth(o.status) }"
            ></div>
          </div>
          
          <!-- Order Content -->
          <div class="p-6">
            <!-- Items Section -->
            <div v-if="o.items && o.items.length > 0" class="mb-6">
              <div class="flex items-center mb-4">
                <svg class="w-5 h-5 text-purple-600 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                </svg>
                <h4 class="text-lg font-semibold text-gray-800">Order Items ({{ o.items.length }})</h4>
              </div>
              
              <div class="space-y-3">
                <div 
                  v-for="(item, idx) in o.items" 
                  :key="idx"
                  class="flex items-center justify-between p-4 bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl hover:from-blue-50 hover:to-purple-50 transition-all duration-300 transform hover:scale-[1.02]"
                >
                  <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold">
                      {{ idx + 1 }}
                    </div>
                    <div>
                      <p class="font-semibold text-gray-800">{{ item.product_name }}</p>
                      <p class="text-sm text-gray-500">Quantity: {{ item.quantity }}</p>
                    </div>
                  </div>
                  <div class="text-right">
                    <p class="font-bold text-gray-800">{{ formatPrice(item.total_item_price) }}</p>
                    <p class="text-xs text-gray-500">{{ formatPrice(item.price_at_purchase) }} each</p>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Shipping & Payment Info -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <!-- Shipping Address -->
              <div v-if="o.shipping_address" class="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border border-green-200">
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 bg-green-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-700 mb-1">Shipping Address</p>
                    <p class="text-sm text-gray-600">{{ o.shipping_address }}</p>
                  </div>
                </div>
              </div>
              
              <!-- Payment Status -->
              <div v-if="o.payment_status" class="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl border border-blue-200">
                <div class="flex items-start space-x-3">
                  <div class="w-10 h-10 bg-blue-500 rounded-lg flex items-center justify-center flex-shrink-0">
                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                    </svg>
                  </div>
                  <div>
                    <p class="font-semibold text-gray-700 mb-1">Payment Status</p>
                    <p class="text-sm text-gray-600 capitalize">{{ o.payment_status }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Order Footer -->
          <div class="bg-gray-50 px-6 py-4 flex items-center justify-between border-t">
            <button class="text-sm text-gray-600 hover:text-blue-600 transition-colors duration-300 flex items-center">
              <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
              </svg>
              View Details
            </button>
            <button class="text-sm px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:shadow-lg transform hover:scale-105 transition-all duration-300">
              Track Order
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../utils/http'

const loading = ref(true)
const orders = ref<any[]>([])

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function formatPrice(price: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(price)
}

function getStatusBadge(status: string) {
  const classes: Record<string, string> = {
    'Pending': 'bg-yellow-500 bg-opacity-90 text-white',
    'Processing': 'bg-blue-500 bg-opacity-90 text-white',
    'Completed': 'bg-green-500 bg-opacity-90 text-white',
    'Canceled': 'bg-red-500 bg-opacity-90 text-white'
  }
  return classes[status] || 'bg-gray-500 bg-opacity-90 text-white'
}

function getProgressWidth(status: string) {
  const progress: Record<string, string> = {
    'Pending': '25%',
    'Processing': '50%',
    'Completed': '100%',
    'Canceled': '0%'
  }
  return progress[status] || '25%'
}

async function loadOrders() {
  loading.value = true
  try {
    const { data } = await api.get('/api/orders/orders/')
    orders.value = data.results || data
  } finally {
    loading.value = false
  }
}

onMounted(loadOrders)
</script>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes bounceSlow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease-out;
}

.order-card {
  animation: slideInUp 0.5s ease-out backwards;
}

.animate-bounce-slow {
  animation: bounceSlow 3s ease-in-out infinite;
}

/* Gradient text effect */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Glass morphism effect */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}

/* Smooth transitions */
* {
  transition-property: transform, box-shadow, background-color;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Hover effects */
.group:hover .group-hover\:scale-150 {
  transform: scale(1.5);
}
</style>


