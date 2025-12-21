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

      <div class="flex-1 overflow-y-auto p-4 sm:p-6">
        <div v-if="cart.items.length === 0" class="flex flex-col items-center justify-center py-16 text-gray-500 dark:text-gray-400">
          <svg class="w-20 h-20 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
          </svg>
          <p class="text-lg font-medium">Your cart is empty</p>
          <p class="text-sm mt-2">Add some products to get started!</p>
        </div>
        <div v-else class="space-y-3">
          <div v-for="it in cart.items" :key="it.product_id" class="group relative flex gap-3 sm:gap-4 p-3 sm:p-4 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-xl hover:shadow-lg dark:hover:shadow-gray-900/50 transition-all duration-200">
            <!-- Product Image -->
            <div class="flex-shrink-0 w-20 h-20 sm:w-24 sm:h-24 bg-gray-50 dark:bg-gray-700 rounded-lg overflow-hidden flex items-center justify-center p-2">
              <img :src="getImageUrl(it.image)" :alt="it.name" class="w-full h-full object-contain" @error="handleImageError" />
            </div>
            
            <!-- Product Info -->
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-sm sm:text-base text-gray-900 dark:text-gray-100 mb-1 line-clamp-2">{{ it.name }}</h3>
              <p class="text-sm sm:text-base font-bold text-blue-600 dark:text-blue-400 mb-2">{{ currency(it.price) }}</p>
              
              <!-- Quantity Controls -->
              <div class="flex items-center gap-2">
                <label class="text-xs sm:text-sm text-gray-600 dark:text-gray-400 font-medium">Qty:</label>
                <input 
                  type="number" 
                  min="1" 
                  class="w-14 sm:w-16 h-8 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-md px-2 text-center text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent" 
                  :value="it.quantity" 
                  @change="onQty(it.product_id, $event)" 
                />
              </div>
              
              <!-- Item Total -->
              <p class="text-xs text-gray-500 dark:text-gray-400 mt-2">
                Total: <span class="font-semibold text-gray-900 dark:text-gray-100">{{ currency((it.price || 0) * it.quantity) }}</span>
              </p>
            </div>
            
            <!-- Remove Button -->
            <button 
              class="flex-shrink-0 w-8 h-8 sm:w-10 sm:h-10 flex items-center justify-center text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors duration-200" 
              @click="cart.remove(it.product_id)"
              title="Remove item"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 p-4 sm:p-6 space-y-4">
        <!-- Cart Summary -->
        <div class="space-y-2">
          <div class="flex justify-between text-sm text-gray-600 dark:text-gray-400">
            <span>Items ({{ cart.items.length }}):</span>
            <span>{{ currency(total) }}</span>
          </div>
          <div class="flex justify-between text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100 pt-2 border-t border-gray-200 dark:border-gray-700">
            <span>Total:</span>
            <span class="text-blue-600 dark:text-blue-400">{{ currency(total) }}</span>
          </div>
        </div>

        <button class="w-full btn" @click="checkout">
          <span class="flex items-center justify-center gap-2">
            Proceed to Checkout
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </span>
        </button>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useCartStore } from '../../stores/cart.store'
import { useAuthStore } from '../../stores/auth.store'
import { getImageUrl } from '../../utils/image'

const cart = useCartStore()
const auth = useAuthStore()
const placeholder = 'https://placehold.co/200x200?text=No+Image'

const total = computed(() => cart.items.reduce((sum, it) => sum + (it.price || 0) * it.quantity, 0))

function currency(v: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v)
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

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = placeholder
}
</script>

<style scoped>
.btn { 
  @apply bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl px-6 py-3.5 hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-semibold shadow-lg hover:shadow-xl transform hover:scale-[1.02] active:scale-[0.98]; 
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
