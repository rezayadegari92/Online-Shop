<template>
  <div class="max-w-4xl mx-auto p-6">
    <h1 class="text-3xl font-bold mb-6">Profile</h1>
    
    <!-- User Info Card -->
    <div v-if="!auth.isAuthenticated" class="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
      <p>Please log in to view your profile.</p>
    </div>
    <div v-else-if="auth.user" class="bg-white rounded-lg shadow p-6 mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold">User Information</h2>
        <button class="text-sm px-3 py-1 bg-black text-white rounded" @click="editMode = !editMode">
          {{ editMode ? 'Cancel' : 'Edit Profile' }}
        </button>
      </div>
      
      <form v-if="editMode" class="grid grid-cols-2 gap-3" @submit.prevent="updateProfile">
        <input class="input" v-model="profileForm.username" placeholder="Username" required />
        <input class="input" v-model="profileForm.email" type="email" placeholder="Email" />
        <input class="input" v-model="profileForm.first_name" placeholder="First Name" />
        <input class="input" v-model="profileForm.last_name" placeholder="Last Name" />
        <input class="input" v-model="profileForm.birth_date" type="date" placeholder="Birth Date" />
        <button class="btn col-span-2">Update Profile</button>
      </form>
      
      <div v-else class="grid grid-cols-2 gap-4">
        <div><span class="font-medium">Email:</span> {{ auth.user.email }}</div>
        <div><span class="font-medium">Username:</span> {{ auth.user.username }}</div>
        <div><span class="font-medium">Name:</span> {{ auth.user.first_name }} {{ auth.user.last_name }}</div>
        <div><span class="font-medium">Birth Date:</span> {{ auth.user.birth_date }}</div>
        <div><span class="font-medium">Type:</span> {{ auth.user.user_type }}</div>
      </div>
    </div>
    <div v-else class="bg-white rounded-lg shadow p-6 mb-6">
      <p>Loading user information...</p>
    </div>

    <!-- Addresses Section -->
    <div class="bg-white rounded-lg shadow p-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold">Addresses</h2>
        <button class="text-sm px-3 py-1 bg-black text-white rounded" @click="showForm = !showForm">
          {{ showForm ? 'Cancel' : '+ Add Address' }}
        </button>
      </div>

      <!-- Add Address Form -->
      <form v-if="showForm" class="mb-6 p-4 bg-gray-50 rounded grid grid-cols-2 gap-3" @submit.prevent="createAddress">
        <input class="input col-span-2" v-model="f.street" placeholder="Street" required />
        <input class="input" v-model="f.city" placeholder="City" required />
        <input class="input" v-model="f.state" placeholder="State" required />
        <input class="input" v-model="f.postal_code" placeholder="Postal Code" />
        <input class="input" v-model="f.phone_number" placeholder="Phone (+989... or 09...)" />
        <button class="btn col-span-2">Save Address</button>
      </form>

      <!-- Address List -->
      <div v-if="loading" class="text-center py-4">Loading addresses...</div>
      <div v-else-if="addresses.length === 0" class="text-center py-4 text-gray-500">No addresses yet</div>
      <div v-else class="space-y-3">
        <div v-for="a in addresses" :key="a.id" class="border rounded-lg p-4 hover:shadow-md transition">
          <form v-if="editingAddress === a.id" class="grid grid-cols-2 gap-3" @submit.prevent="updateAddress(a.id)">
            <input class="input col-span-2" v-model="editForm.street" placeholder="Street" required />
            <input class="input" v-model="editForm.city" placeholder="City" required />
            <input class="input" v-model="editForm.state" placeholder="State" required />
            <input class="input" v-model="editForm.postal_code" placeholder="Postal Code" />
            <input class="input" v-model="editForm.phone_number" placeholder="Phone" />
            <div class="col-span-2 flex gap-2">
              <button type="submit" class="btn flex-1">Save</button>
              <button type="button" class="btn-secondary flex-1" @click="editingAddress = null">Cancel</button>
            </div>
          </form>
          
          <div v-else class="flex items-start justify-between">
            <div class="flex-1">
              <div class="font-semibold text-lg">{{ a.street }}</div>
              <div class="text-gray-600">{{ a.city }}, {{ a.state }} {{ a.postal_code }}</div>
              <div class="text-sm text-gray-500 mt-1">{{ a.phone_number }}</div>
              <span v-if="a.is_default" class="inline-block mt-2 px-2 py-1 text-xs bg-green-100 text-green-700 rounded">Default</span>
            </div>
            <div class="flex flex-col gap-2">
              <button class="text-sm px-3 py-1 border rounded hover:bg-gray-50" @click="startEdit(a)">
                Edit
              </button>
              <button v-if="!a.is_default" class="text-sm px-3 py-1 border rounded hover:bg-gray-50" @click="setDefault(a.id)">
                Set Default
              </button>
              <button class="text-sm px-3 py-1 border rounded text-red-600 hover:bg-red-50" @click="remove(a.id)">
                Delete
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth.store'
import { onMounted, ref, reactive, watch } from 'vue'
import api from '../utils/http'
const auth = useAuthStore()

const addresses = ref<any[]>([])
const loading = ref(true)
const showForm = ref(false)
const editMode = ref(false)
const editingAddress = ref<number | null>(null)
const f = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '' })
const editForm = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '' })
const profileForm = reactive({ 
  username: '', 
  email: '', 
  first_name: '', 
  last_name: '', 
  birth_date: '' 
})

async function loadAddresses() {
  loading.value = true
  try {
    const { data } = await api.get('/api/addresses/')
    addresses.value = data.results || data
  } finally {
    loading.value = false
  }
}

async function createAddress() {
  await api.post('/api/addresses/', f)
  Object.assign(f, { street: '', city: '', state: '', postal_code: '', phone_number: '' })
  showForm.value = false
  await loadAddresses()
}

async function remove(id: number) {
  if (!confirm('Delete this address?')) return
  await api.delete(`/api/addresses/${id}/`)
  await loadAddresses()
}

async function setDefault(id: number) {
  await api.post(`/api/addresses/${id}/set-default/`)
  await loadAddresses()
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

async function updateProfile() {
  try {
    await api.patch('/accounts/api/profile/', profileForm)
    await auth.bootstrap()
    editMode.value = false
    alert('Profile updated successfully!')
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Failed to update profile')
  }
}

function initProfileForm() {
  if (auth.user) {
    profileForm.username = auth.user.username || ''
    profileForm.email = auth.user.email || ''
    profileForm.first_name = auth.user.first_name || ''
    profileForm.last_name = auth.user.last_name || ''
    profileForm.birth_date = auth.user.birth_date || ''
  }
}

watch(editMode, (newVal) => {
  if (newVal) {
    initProfileForm()
  }
})

onMounted(async () => {
  if (auth.isAuthenticated && !auth.user) {
    await auth.bootstrap()
  }
  if (auth.isAuthenticated) {
    initProfileForm()
    await loadAddresses()
  }
})
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2 focus:ring-2 focus:ring-black focus:outline-none; }
.btn { @apply bg-black text-white rounded px-4 py-2 hover:bg-gray-800 transition; }
.btn-secondary { @apply bg-gray-200 text-gray-800 rounded px-4 py-2 hover:bg-gray-300 transition; }
</style>
