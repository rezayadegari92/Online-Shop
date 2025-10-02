<template>
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-2xl font-semibold mb-4">Products</h1>
    <div v-if="loading">Loading...</div>
    <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
      <div v-for="p in products" :key="p.id" class="border rounded p-3">
        <div class="font-medium truncate">{{ p.name }}</div>
        <div class="text-sm text-gray-600">{{ currency(p.price) }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import api from '../utils/http'

const loading = ref(true)
const products = ref<any[]>([])

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('fa-IR', { style: 'currency', currency: 'IRR', maximumFractionDigits: 0 }).format(n)
}

onMounted(async () => {
  try {
    const { data } = await api.get('/api/products/')
    products.value = data.results || data
  } finally {
    loading.value = false
  }
})
</script>


