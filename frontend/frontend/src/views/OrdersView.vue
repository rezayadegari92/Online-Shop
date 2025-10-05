<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-6">My Orders</h1>
    
    <div v-if="loading" class="text-center py-8">Loading...</div>
    
    <div v-else-if="orders.length === 0" class="text-center py-12 bg-gray-50 rounded-lg">
      <p class="text-gray-500">No orders yet</p>
    </div>
    
    <div v-else class="space-y-4">
      <div v-for="o in orders" :key="o.id" class="border rounded-lg p-5 bg-white shadow-sm hover:shadow-md transition">
        <div class="flex items-start justify-between mb-3">
          <div>
            <h3 class="font-semibold text-lg">Order #{{ o.id }}</h3>
            <p class="text-sm text-gray-500">{{ formatDate(o.created_at) }}</p>
          </div>
          <div class="text-right">
            <div class="font-bold text-lg">{{ formatPrice(o.total_price) }}</div>
            <span class="inline-block px-3 py-1 text-xs rounded-full" :class="getStatusClass(o.status)">
              {{ o.status }}
            </span>
          </div>
        </div>
        
        <div v-if="o.items && o.items.length > 0" class="border-t pt-3 mt-3">
          <p class="text-sm font-medium mb-2">Items:</p>
          <div class="space-y-1">
            <div v-for="item in o.items" :key="item.product_name" class="text-sm text-gray-600">
              {{ item.product_name }} × {{ item.quantity }} - {{ formatPrice(item.total_item_price) }}
            </div>
          </div>
        </div>
        
        <div v-if="o.shipping_address" class="border-t pt-3 mt-3">
          <p class="text-sm"><span class="font-medium">Shipping:</span> {{ o.shipping_address }}</p>
        </div>
        
        <div v-if="o.payment_status" class="mt-2">
          <span class="text-sm text-gray-600">Payment: {{ o.payment_status }}</span>
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
    month: 'long',
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

function getStatusClass(status: string) {
  const classes: Record<string, string> = {
    'Pending': 'bg-yellow-100 text-yellow-800',
    'Processing': 'bg-blue-100 text-blue-800',
    'Completed': 'bg-green-100 text-green-800',
    'Canceled': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
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


