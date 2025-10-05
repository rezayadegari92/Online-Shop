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
          
          <div v-else class="space-y-4">
            <div v-for="item in cart.items" :key="item.product_id" class="flex gap-4 p-4 border rounded-lg">
              <img :src="item.image || placeholder" class="w-20 h-20 object-cover rounded" />
              <div class="flex-1">
                <h3 class="font-semibold">{{ item.name }}</h3>
                <p class="text-gray-600">{{ formatPrice(item.price) }}</p>
                <div class="flex items-center gap-2 mt-2">
                  <label class="text-sm">Qty:</label>
                  <input 
                    type="number" 
                    min="1" 
                    class="w-16 border rounded px-2 py-1 text-center" 
                    :value="item.quantity" 
                    @change="updateQuantity(item.product_id, $event)"
                  />
                  <button @click="removeItem(item.product_id)" class="text-red-500 hover:text-red-700 ml-auto">
                    Remove
                  </button>
                </div>
              </div>
              <div class="text-right">
                <p class="font-bold">{{ formatPrice(item.price * item.quantity) }}</p>
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
          
          <div class="space-y-3 mb-6">
            <div class="flex justify-between text-gray-600">
              <span>Subtotal:</span>
              <span>{{ formatPrice(subtotal) }}</span>
            </div>
            <div class="flex justify-between text-gray-600">
              <span>Shipping:</span>
              <span>Free</span>
            </div>
            <div class="border-t pt-3 flex justify-between text-xl font-bold">
              <span>Total:</span>
              <span>{{ formatPrice(subtotal) }}</span>
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

const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()

const cartLoading = ref(true)
const loadingAddresses = ref(true)
const processing = ref(false)
const addresses = ref<any[]>([])
const showAddressForm = ref(false)
const editingAddress = ref<number | null>(null)
const placeholder = 'https://placehold.co/200x200?text=No+Image'

const addressForm = reactive({
  street: '',
  city: '',
  state: '',
  postal_code: '',
  phone_number: ''
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

const hasDefaultAddress = computed(() => {
  return addresses.value.some(addr => addr.is_default)
})

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
    Object.assign(addressForm, { street: '', city: '', state: '', postal_code: '', phone_number: '' })
    showAddressForm.value = false
    await loadAddresses()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to create address')
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
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to update address')
  }
}

async function setDefault(id: number) {
  try {
    await api.post(`/api/addresses/${id}/set-default/`)
    await loadAddresses()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to set default address')
  }
}

async function deleteAddress(id: number) {
  if (!confirm('Delete this address?')) return
  try {
    await api.delete(`/api/addresses/${id}/`)
    await loadAddresses()
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to delete address')
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

async function completeCheckout() {
  if (!hasDefaultAddress.value) {
    alert('Please set a default address before checkout')
    return
  }

  if (cart.items.length === 0) {
    alert('Your cart is empty')
    return
  }

  processing.value = true
  try {
    const { data } = await api.post('/api/cart/checkout/')
    alert('Order placed successfully!')
    router.push('/orders')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Checkout failed. Please try again.')
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
</style>

