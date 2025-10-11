<template>
  <div v-if="cart.isOpen" class="fixed inset-0 z-50">
    <div class="absolute inset-0 bg-black/50 backdrop-blur-sm" @click="cart.toggle(false)"></div>
    <aside class="absolute right-0 top-0 h-full w-full max-w-md bg-white dark:bg-gray-800 shadow-2xl dark:shadow-gray-900 flex flex-col">
      <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
        <h2 class="text-2xl font-bold text-gray-900 dark:text-gray-100">Shopping Cart</h2>
        <button class="text-gray-500 dark:text-gray-400 hover:text-black dark:hover:text-white" @click="cart.toggle(false)">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
      
      <div class="flex-1 overflow-y-auto p-6 space-y-4">
        <div v-if="cart.items.length === 0" class="text-center py-12 text-gray-500 dark:text-gray-400">
          Your cart is empty
        </div>
        <div v-for="it in cart.items" :key="it.product_id" class="flex gap-4 p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md dark:hover:shadow-gray-900 transition bg-white dark:bg-gray-700">
          <div class="flex-shrink-0 w-24 h-24 bg-gray-50 dark:bg-gray-600 rounded-lg overflow-hidden flex items-center justify-center p-2">
            <img :src="getImageUrl(it.image)" class="w-full h-full object-contain" />
          </div>
          <div class="flex-1">
            <div class="font-semibold text-gray-900 dark:text-gray-100">{{ it.name }}</div>
            <div class="text-gray-600 dark:text-gray-400 text-sm">{{ currency(it.price) }}</div>
            <div class="flex items-center gap-2 mt-2">
              <label class="text-sm text-gray-700 dark:text-gray-300">Qty:</label>
              <input type="number" min="1" class="w-16 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded px-2 py-1 text-center" :value="it.quantity" @change="onQty(it.product_id, $event)" />
            </div>
          </div>
          <button class="text-red-500 hover:text-red-700" @click="cart.remove(it.product_id)">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
          </button>
        </div>
      </div>
      
      <div class="border-t border-gray-200 dark:border-gray-700 p-6">
        <div class="flex justify-between mb-4 text-lg font-semibold text-gray-900 dark:text-gray-100">
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
import { getImageUrl } from '../../utils/image'

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

function checkout() {
  cart.toggle(false)
  // Redirect to checkout page
  window.location.href = '/checkout'
}
</script>

<style scoped>
.btn { @apply bg-black text-white rounded-lg px-6 py-3 hover:bg-gray-800 transition font-semibold; }
</style>
