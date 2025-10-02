<template>
  <div v-if="cart.isOpen" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="cart.toggle(false)"></div>
    <aside class="absolute right-0 top-0 h-full w-full max-w-md bg-white shadow-2xl flex flex-col">
      <div class="flex items-center justify-between p-6 border-b">
        <h2 class="text-2xl font-bold">Shopping Cart</h2>
        <button class="text-gray-500 hover:text-black" @click="cart.toggle(false)">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div v-if="cart.items.length === 0" class="text-center py-12 text-gray-500">
          Your cart is empty
        </div>
        <div v-for="it in cart.items" :key="it.product_id" class="flex gap-4 p-4 border rounded-lg hover:shadow-md transition">
          <img :src="it.image || placeholder" class="w-20 h-20 object-cover rounded" />
          <div class="flex-1">
            <div class="font-semibold">{{ it.name }}</div>
            <div class="text-gray-600 text-sm">{{ currency(it.price) }}</div>
            <div class="flex items-center gap-2 mt-2">
              <label class="text-sm">Qty:</label>
              <input type="number" min="1" class="w-16 border rounded px-2 py-1 text-center" :value="it.quantity" @change="onQty(it.product_id, $event)" />
            </div>
          </div>
          <button class="text-red-500 hover:text-red-700" @click="cart.remove(it.product_id)">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
      
      <div class="border-t p-6">
        <div class="flex justify-between mb-4 text-lg font-semibold">
          <span>Total:</span>
          <span>{{ currency(total) }}</span>
        </div>
        <button class="w-full btn" @click="checkout">Proceed to Checkout</button>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCartStore } from '../../stores/cart.store'
const cart = useCartStore()
const placeholder = 'https://placehold.co/200x200?text=No+Image'

const total = computed(() => cart.items.reduce((sum, it) => sum + (it.price || 0) * it.quantity, 0))

function currency(v: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'IRR', maximumFractionDigits: 0 }).format(v)
}

function onQty(product_id: number, e: Event) {
  const value = Number((e.target as HTMLInputElement).value)
  if (value > 0) cart.update(product_id, value)
}

async function checkout() {
  try {
    const result = await cart.checkout()
    cart.toggle(false)
    // Redirect to orders page
    window.location.href = '/orders'
  } catch (e: any) {
    if (e.response?.status === 401) {
      alert('Please log in to checkout')
      window.location.href = '/login'
    } else {
      alert(e.response?.data?.detail || 'Checkout failed. Please ensure you have a default address.')
    }
  }
}
</script>

<style scoped>
.btn { @apply bg-black text-white rounded-lg px-6 py-3 hover:bg-gray-800 transition font-semibold; }
</style>
