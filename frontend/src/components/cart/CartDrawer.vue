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

        <!-- Discount Code Section -->
        <div v-if="cart.items.length > 0" class="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
          <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
            <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            Have a discount code?
          </label>
          <div class="flex gap-2">
            <input
              v-model="discountCode"
              type="text"
              placeholder="Enter code (e.g. WELCOME10)"
              class="flex-1 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              :disabled="applyingDiscount || discountApplied"
              @keyup.enter="applyDiscount"
            />
            <button
              @click="applyDiscount"
              :disabled="!discountCode || applyingDiscount || discountApplied"
              class="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white rounded-lg font-semibold text-sm transition disabled:cursor-not-allowed"
            >
              <span v-if="applyingDiscount">
                <svg class="w-4 h-4 inline animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </span>
              <span v-else>{{ discountApplied ? 'Applied' : 'Apply' }}</span>
            </button>
          </div>

          <!-- Success Message -->
          <div v-if="discountApplied" class="mt-2 flex items-center text-green-600 dark:text-green-400 text-sm">
            <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
            </svg>
            Discount applied: {{ cart.discountPercent }}% off
          </div>

          <!-- Error Message -->
          <div v-if="discountError" class="mt-2 text-red-600 dark:text-red-400 text-sm">
            {{ discountError }}
          </div>
        </div>
      </div>

      <div class="border-t border-gray-200 dark:border-gray-700 p-6 space-y-3">
        <!-- Subtotal -->
        <div v-if="discountApplied" class="flex justify-between text-gray-600 dark:text-gray-400">
          <span>Subtotal:</span>
          <span>{{ currency(total) }}</span>
        </div>

        <!-- Discount -->
        <div v-if="discountApplied" class="flex justify-between text-green-600 dark:text-green-400">
          <span>Discount ({{ cart.discountPercent }}%):</span>
          <span>-{{ currency(discountAmount) }}</span>
        </div>

        <!-- Total -->
        <div class="flex justify-between text-lg font-bold text-gray-900 dark:text-gray-100 pt-3 border-t border-gray-200 dark:border-gray-700">
          <span>Total:</span>
          <span>{{ currency(finalTotal) }}</span>
        </div>

        <button class="w-full btn" @click="checkout">Proceed to Checkout</button>
      </div>
    </aside>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useCartStore } from '../../stores/cart.store'
import { useAuthStore } from '../../stores/auth.store'
import { getImageUrl } from '../../utils/image'
import api from '../../utils/http'

const cart = useCartStore()
const auth = useAuthStore()
const placeholder = 'https://placehold.co/200x200?text=No+Image'

const discountCode = ref('')
const applyingDiscount = ref(false)
const discountError = ref('')

const total = computed(() => cart.items.reduce((sum, it) => sum + (it.price || 0) * it.quantity, 0))

const discountApplied = computed(() => cart.discountPercent > 0)
const discountPercent = computed(() => cart.discountPercent)

const discountAmount = computed(() => {
  if (!cart.discountPercent) return 0
  return (total.value * cart.discountPercent) / 100
})

const finalTotal = computed(() => {
  return total.value - discountAmount.value
})

function currency(v: number) {
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', maximumFractionDigits: 0 }).format(v)
}

function onQty(product_id: number, e: Event) {
  const value = Number((e.target as HTMLInputElement).value)
  if (value > 0) cart.update(product_id, value)
}

async function applyDiscount() {
  if (!discountCode.value.trim()) return

  if (!auth.isAuthenticated) {
    discountError.value = 'Please login to apply discount codes'
    return
  }

  applyingDiscount.value = true
  discountError.value = ''

  try {
    const { data } = await api.post('/api/cart/apply-discount/', {
      code: discountCode.value.toUpperCase()
    })

    // Reload cart to get updated discount information
    await cart.load()
    discountError.value = ''
  } catch (error: any) {
    discountError.value = error.response?.data?.code?.[0] || error.response?.data?.detail || 'Invalid discount code'
  } finally {
    applyingDiscount.value = false
  }
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
