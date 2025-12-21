<template>
  <div class="max-w-6xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-8">Checkout</h1>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column: Cart Items & Addresses -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Cart Items Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <h2 class="text-2xl font-semibold mb-4">Order Summary</h2>

          <div v-if="cartLoading" class="text-center py-8">Loading cart...</div>

          <div v-else-if="cart.items.length === 0" class="text-center py-8 text-gray-500">
            <p>Your cart is empty</p>
            <router-link to="/products" class="text-blue-600 hover:underline mt-2 inline-block">Continue Shopping</router-link>
          </div>

          <div v-else class="space-y-3">
            <div v-for="item in cart.items" :key="item.product_id" class="group relative flex gap-4 p-4 bg-gray-50 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-xl hover:shadow-md transition-all duration-200">
              <!-- Product Image -->
              <div class="flex-shrink-0 w-20 h-20 sm:w-24 sm:h-24 bg-white dark:bg-gray-700 rounded-lg overflow-hidden flex items-center justify-center p-2">
                <img :src="getImageUrl(item.image)" :alt="item.name" class="w-full h-full object-contain" @error="handleImageError" />
              </div>
              
              <!-- Product Info -->
              <div class="flex-1 min-w-0">
                <h3 class="font-semibold text-base sm:text-lg text-gray-900 dark:text-gray-100 mb-1 line-clamp-2">{{ item.name }}</h3>
                <p class="text-sm sm:text-base font-bold text-blue-600 dark:text-blue-400 mb-3">{{ formatPrice(item.price) }}</p>
                
                <!-- Quantity Controls -->
                <div class="flex items-center gap-3">
                  <label class="text-sm text-gray-600 dark:text-gray-400 font-medium">Quantity:</label>
                  <input
                    type="number"
                    min="1"
                    class="w-16 h-9 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 rounded-lg px-2 text-center text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    :value="item.quantity"
                    @change="updateQuantity(item.product_id, $event)"
                  />
                  <button 
                    @click="removeItem(item.product_id)" 
                    class="ml-auto text-red-500 hover:text-red-700 hover:bg-red-50 dark:hover:bg-red-900/20 px-3 py-1.5 rounded-lg transition-colors duration-200 text-sm font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>
              
              <!-- Item Total -->
              <div class="flex-shrink-0 text-right">
                <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Total</p>
                <p class="text-lg sm:text-xl font-bold text-gray-900 dark:text-gray-100">{{ formatPrice(item.price * item.quantity) }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Addresses Section -->
        <div class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center justify-between mb-4">
            <h2 class="text-2xl font-semibold">Shipping Address</h2>
            <button
              @click="showAddressForm = !showAddressForm"
              class="text-sm px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
            >
              {{ showAddressForm ? 'Cancel' : '+ Add Address' }}
            </button>
          </div>

          <!-- Add Address Form -->
          <form v-if="showAddressForm" class="mb-6 p-4 bg-gray-50 rounded grid grid-cols-2 gap-3" @submit.prevent="createAddress">
            <input class="input col-span-2" v-model="addressForm.street" placeholder="Street" required />
            <input class="input" v-model="addressForm.city" placeholder="City" required />
            <input class="input" v-model="addressForm.state" placeholder="State" required />
            <input class="input" v-model="addressForm.postal_code" placeholder="Postal Code" />
            <input class="input" v-model="addressForm.phone_number" placeholder="Phone (+989... or 09...)" required />
            <input class="input" v-model="addressForm.country" placeholder="Country" required />
            <button type="submit" class="btn col-span-2">Save Address</button>
          </form>

          <!-- Address List -->
          <div v-if="loadingAddresses" class="text-center py-4">Loading addresses...</div>

          <div v-else-if="addresses.length === 0" class="text-center py-8 text-gray-500">
            <p>No addresses found. Please add a shipping address.</p>
          </div>

          <div v-else class="space-y-3">
            <div
              v-for="addr in addresses"
              :key="addr.id"
              class="border rounded-lg p-4 cursor-pointer transition"
              :class="addr.is_default ? 'border-blue-500 bg-blue-50' : 'hover:border-gray-300'"
            >
              <div v-if="editingAddress === addr.id">
                <form class="grid grid-cols-2 gap-3" @submit.prevent="updateAddress(addr.id)">
                  <input class="input col-span-2" v-model="editForm.street" placeholder="Street" required />
                  <input class="input" v-model="editForm.city" placeholder="City" required />
                  <input class="input" v-model="editForm.state" placeholder="State" required />
                  <input class="input" v-model="editForm.postal_code" placeholder="Postal Code" />
                  <input class="input" v-model="editForm.phone_number" placeholder="Phone" required />
                  <div class="col-span-2 flex gap-2">
                    <button type="submit" class="btn flex-1">Save</button>
                    <button type="button" class="btn-secondary flex-1" @click="editingAddress = null">Cancel</button>
                  </div>
                </form>
              </div>

              <div v-else>
                <div class="flex items-start justify-between">
                  <div class="flex-1">
                    <div class="font-semibold">{{ addr.street }}</div>
                    <div class="text-sm text-gray-600">{{ addr.city }}, {{ addr.state }} {{ addr.postal_code }}</div>
                    <div class="text-sm text-gray-500">{{ addr.phone_number }}</div>
                    <span v-if="addr.is_default" class="inline-block mt-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded font-semibold">
                      Default Address
                    </span>
                  </div>
                  <div class="flex flex-col gap-2">
                    <button @click="startEdit(addr)" class="text-sm px-3 py-1 border rounded hover:bg-gray-50">Edit</button>
                    <button v-if="!addr.is_default" @click="setDefault(addr.id)" class="text-sm px-3 py-1 border rounded hover:bg-gray-50">
                      Set Default
                    </button>
                    <button @click="deleteAddress(addr.id)" class="text-sm px-3 py-1 border rounded text-red-600 hover:bg-red-50">
                      Delete
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Order Total & Checkout Button -->
      <div class="lg:col-span-1">
        <div class="bg-white rounded-lg shadow p-6 sticky top-20">
          <h2 class="text-xl font-semibold mb-4">Order Total</h2>

          <!-- Discount Code Section -->
          <div v-if="cart.items.length > 0" class="mb-6 p-4 bg-gray-50 rounded-lg border border-gray-200">
            <label class="block text-sm font-semibold text-gray-700 mb-2">
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
                class="flex-1 border border-gray-300 bg-white text-gray-900 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
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
            <div v-if="discountApplied" class="mt-2 flex items-center text-green-600 text-sm">
              <svg class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
              </svg>
              Discount applied: {{ cart.discountPercent }}% off
            </div>

            <!-- Error Message -->
            <div v-if="discountError" class="mt-2 text-red-600 text-sm">
              {{ discountError }}
            </div>
          </div>

          <div class="space-y-3 mb-6">
            <div class="flex justify-between text-gray-600">
              <span>Subtotal:</span>
              <span>{{ formatPrice(subtotal) }}</span>
            </div>
            <div v-if="cart.discountPercent > 0" class="flex justify-between text-green-600">
              <span>Discount ({{ cart.discountPercent }}%):</span>
              <span>-{{ formatPrice(discountAmount) }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Shipping:</span>
              <span>Free</span>
            </div>
            <div class="border-t pt-3 flex justify-between text-xl font-bold">
              <span>Total:</span>
              <span>{{ formatPrice(finalTotal) }}</span>
            </div>
          </div>

          <button
            @click="completeCheckout"
            class="w-full btn-primary text-lg py-3"
            :disabled="cart.items.length === 0 || !hasDefaultAddress || processing"
          >
            {{ processing ? 'Processing...' : 'Complete Order' }}
          </button>

          <div v-if="!hasDefaultAddress && addresses.length > 0" class="mt-4 text-sm text-red-600 text-center">
            Please set a default address
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '../stores/cart.store'
import { useAuthStore } from '../stores/auth.store'
import api from '../utils/http'
import { showToast } from '../utils/toast'
import { getImageUrl } from '../utils/image'

const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()

const cartLoading = ref(true)
const loadingAddresses = ref(true)
const processing = ref(false)
const addresses = ref<any[]>([])
const showAddressForm = ref(false)
const editingAddress = ref<number | null>(null)

const discountCode = ref('')
const applyingDiscount = ref(false)
const discountError = ref('')

const addressForm = reactive({
  street: '',
  city: '',
  state: '',
  postal_code: '',
  phone_number: '',
  country: 'Iran'
})

const editForm = reactive({
  street: '',
  city: '',
  state: '',
  postal_code: '',
  phone_number: ''
})

const subtotal = computed(() => {
  return cart.items.reduce((sum, item) => sum + (item.price || 0) * item.quantity, 0)
})

const discountAmount = computed(() => {
  if (!cart.discountPercent) return 0
  return (subtotal.value * cart.discountPercent) / 100
})

const finalTotal = computed(() => {
  return subtotal.value - discountAmount.value
})

const hasDefaultAddress = computed(() => {
  return addresses.value.some(addr => addr.is_default)
})

const discountApplied = computed(() => cart.discountPercent > 0)

onMounted(async () => {
  if (!auth.isAuthenticated) {
    router.push('/login?redirect=/checkout')
    return
  }

  await loadCart()
  await loadAddresses()
})

async function loadCart() {
  cartLoading.value = true
  try {
    await cart.load()
    // Clear discount input if cart is empty or no discount applied
    if (cart.items.length === 0 || cart.discountPercent === 0) {
      discountCode.value = ''
      discountError.value = ''
    }
  } finally {
    cartLoading.value = false
  }
}

async function loadAddresses() {
  loadingAddresses.value = true
  try {
    const { data } = await api.get('/api/addresses/')
    addresses.value = data.results || data
  } finally {
    loadingAddresses.value = false
  }
}

async function createAddress() {
  try {
    await api.post('/api/addresses/', addressForm)
    Object.assign(addressForm, { street: '', city: '', state: '', postal_code: '', phone_number: '', country: 'Iran' })
    showAddressForm.value = false
    await loadAddresses()
    showToast.success('Address created successfully!')
  } catch (e: any) {
    showToast.error(e.response?.data?.detail || e.response?.data?.phone_number?.[0] || 'Failed to create address')
  }
}

function startEdit(address: any) {
  editingAddress.value = address.id
  editForm.street = address.street
  editForm.city = address.city
  editForm.state = address.state
  editForm.postal_code = address.postal_code
  editForm.phone_number = address.phone_number
}

async function updateAddress(id: number) {
  try {
    await api.patch(`/api/addresses/${id}/`, editForm)
    editingAddress.value = null
    await loadAddresses()
    showToast.success('Address updated successfully!')
  } catch (e: any) {
    showToast.error(e.response?.data?.detail || 'Failed to update address')
  }
}

async function setDefault(id: number) {
  try {
    await api.post(`/api/addresses/${id}/set-default/`)
    await loadAddresses()
    showToast.success('Default address updated!')
  } catch (e: any) {
    showToast.error(e.response?.data?.detail || 'Failed to set default address')
  }
}

async function deleteAddress(id: number) {
  if (!confirm('Delete this address?')) return
  try {
    await api.delete(`/api/addresses/${id}/`)
    await loadAddresses()
    showToast.success('Address deleted successfully!')
  } catch (e: any) {
    showToast.error(e.response?.data?.detail || 'Failed to delete address')
  }
}

function updateQuantity(productId: number, event: Event) {
  const value = Number((event.target as HTMLInputElement).value)
  if (value > 0) {
    cart.update(productId, value)
  }
}

async function removeItem(productId: number) {
  await cart.remove(productId)
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
    discountCode.value = '' // Clear input after successful application
  } catch (error: any) {
    discountError.value = error.response?.data?.code?.[0] || error.response?.data?.detail || 'Invalid discount code'
  } finally {
    applyingDiscount.value = false
  }
}

async function completeCheckout() {
  if (!hasDefaultAddress.value) {
    showToast.warning('Please set a default address before checkout')
    return
  }

  if (cart.items.length === 0) {
    showToast.warning('Your cart is empty')
    return
  }

  processing.value = true
  try {
    const { data } = await api.post('/api/cart/checkout/')
    // Clear the cart and discount after successful checkout
    await cart.load()
    discountCode.value = ''
    discountError.value = ''
    showToast.success('Order placed successfully!')
    router.push('/orders')
  } catch (e: any) {
    showToast.error(e.response?.data?.detail || 'Checkout failed. Please try again.')
  } finally {
    processing.value = false
  }
}

function formatPrice(price: number) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0
  }).format(price)
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = 'https://placehold.co/200x200?text=No+Image'
}
</script>

<style scoped>
.input {
  @apply w-full border rounded px-3 py-2 focus:ring-2 focus:ring-blue-300 focus:outline-none;
}
.btn {
  @apply bg-gray-800 text-white rounded px-4 py-2 hover:bg-gray-900 transition;
}
.btn-secondary {
  @apply bg-gray-200 text-gray-800 rounded px-4 py-2 hover:bg-gray-300 transition;
}
.btn-primary {
  @apply bg-blue-600 text-white rounded px-6 py-3 hover:bg-blue-700 transition font-semibold disabled:bg-gray-300 disabled:cursor-not-allowed;
}
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
