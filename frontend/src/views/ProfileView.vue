<template>
  <div class="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 py-12 px-4">
    <div class="max-w-6xl mx-auto">
      <!-- Header Section -->
      <div class="text-center mb-12 animate-fadeIn">
        <h1 class="text-5xl font-bold bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 bg-clip-text text-transparent mb-3">
          My Profile
        </h1>
        <p class="text-gray-600">Manage your personal information and addresses</p>
      </div>

      <!-- Not Authenticated State -->
      <div v-if="!auth.isAuthenticated" class="max-w-md mx-auto animate-fadeIn">
        <div class="bg-gradient-to-r from-yellow-400 to-orange-400 rounded-2xl shadow-2xl p-8 text-white text-center">
          <svg class="w-16 h-16 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
          </svg>
          <h3 class="text-2xl font-bold mb-2">Authentication Required</h3>
          <p class="mb-6 opacity-90">Please log in to view your profile</p>
          <router-link to="/login" class="inline-block px-8 py-3 bg-white text-orange-600 rounded-full font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-300">
            Login Now
          </router-link>
        </div>
      </div>

      <!-- Profile Content -->
      <div v-else class="space-y-6">
        <!-- User Info Card -->
        <div class="profile-card group bg-white rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500">
          <!-- Profile Header with Gradient -->
          <div class="relative bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 p-8 text-white">
            <div class="absolute top-0 right-0 w-96 h-96 bg-white opacity-10 rounded-full -mr-48 -mt-48 transform group-hover:scale-150 transition-transform duration-700"></div>
            
            <div class="relative flex items-center justify-between">
              <div class="flex items-center space-x-6">
                <!-- Avatar -->
                <div class="w-24 h-24 bg-white bg-opacity-20 backdrop-blur-sm rounded-full flex items-center justify-center text-4xl font-bold border-4 border-white border-opacity-30 animate-pulse-slow">
                  {{ getInitials(auth.user) }}
                </div>
                <div>
                  <h2 class="text-3xl font-bold mb-1">{{ auth.user?.first_name }} {{ auth.user?.last_name }}</h2>
                  <p class="text-purple-100 flex items-center">
                    <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                    </svg>
                    @{{ auth.user?.username }}
                  </p>
                  <span class="inline-block mt-2 px-3 py-1 bg-white bg-opacity-20 backdrop-blur-sm rounded-full text-xs font-semibold">
                    {{ auth.user?.user_type }}
                  </span>
                </div>
              </div>
              
              <button 
                @click="editMode = !editMode"
                class="px-6 py-3 bg-white bg-opacity-20 backdrop-blur-sm text-white rounded-xl font-semibold hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 flex items-center space-x-2"
              >
                <svg v-if="!editMode" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>{{ editMode ? 'Cancel' : 'Edit Profile' }}</span>
              </button>
            </div>
          </div>

          <!-- Profile Content -->
          <div class="p-8">
            <!-- Edit Mode -->
            <form v-if="editMode" class="grid grid-cols-1 md:grid-cols-2 gap-6" @submit.prevent="updateProfile">
              <div class="form-group">
                <label class="form-label">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                  Username
                </label>
                <input class="form-input" v-model="profileForm.username" placeholder="Username" required />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  Email
                </label>
                <input class="form-input" v-model="profileForm.email" type="email" placeholder="Email" />
              </div>
              
              <div class="form-group">
                <label class="form-label">First Name</label>
                <input class="form-input" v-model="profileForm.first_name" placeholder="First Name" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Last Name</label>
                <input class="form-input" v-model="profileForm.last_name" placeholder="Last Name" />
              </div>
              
              <div class="form-group">
                <label class="form-label">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  Birth Date
                </label>
                <input class="form-input" v-model="profileForm.birth_date" type="date" />
              </div>
              
              <div class="flex items-end">
                <button type="submit" class="btn-gradient w-full">
                  <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                  Update Profile
                </button>
              </div>
            </form>

            <!-- View Mode -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="info-card">
                <div class="info-icon bg-gradient-to-br from-blue-500 to-cyan-500">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p class="info-label">Email</p>
                  <p class="info-value">{{ auth.user?.email }}</p>
                </div>
              </div>

              <div class="info-card">
                <div class="info-icon bg-gradient-to-br from-purple-500 to-pink-500">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="info-label">Username</p>
                  <p class="info-value">{{ auth.user?.username }}</p>
                </div>
              </div>

              <div class="info-card">
                <div class="info-icon bg-gradient-to-br from-green-500 to-emerald-500">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div>
                  <p class="info-label">Full Name</p>
                  <p class="info-value">{{ auth.user?.first_name }} {{ auth.user?.last_name }}</p>
                </div>
              </div>

              <div class="info-card">
                <div class="info-icon bg-gradient-to-br from-orange-500 to-red-500">
                  <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
                <div>
                  <p class="info-label">Birth Date</p>
                  <p class="info-value">{{ formatDate(auth.user?.birth_date) }}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Addresses Section -->
        <div class="profile-card bg-white rounded-2xl shadow-xl overflow-hidden">
          <div class="bg-gradient-to-r from-green-500 to-emerald-500 p-6 text-white">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <h2 class="text-2xl font-bold">My Addresses</h2>
              </div>
              
              <button 
                @click="showForm = !showForm"
                class="px-6 py-3 bg-white bg-opacity-20 backdrop-blur-sm text-white rounded-xl font-semibold hover:bg-opacity-30 transition-all duration-300 transform hover:scale-105 flex items-center space-x-2"
              >
                <svg v-if="!showForm" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                </svg>
                <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
                <span>{{ showForm ? 'Cancel' : 'Add Address' }}</span>
              </button>
            </div>
          </div>

          <div class="p-6">
            <!-- Add Address Form -->
            <form v-if="showForm" class="mb-6 p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl border-2 border-green-200 grid grid-cols-1 md:grid-cols-2 gap-4" @submit.prevent="createAddress">
              <div class="form-group col-span-full">
                <label class="form-label">Street Address</label>
                <input class="form-input" v-model="f.street" placeholder="123 Main Street" required />
              </div>
              
              <div class="form-group">
                <label class="form-label">City</label>
                <input class="form-input" v-model="f.city" placeholder="City" required />
              </div>
              
              <div class="form-group">
                <label class="form-label">State/Province</label>
                <input class="form-input" v-model="f.state" placeholder="State" required />
              </div>
              
              <div class="form-group">
                <label class="form-label">Postal Code</label>
                <input class="form-input" v-model="f.postal_code" placeholder="12345" />
              </div>
              
              <div class="form-group">
                <label class="form-label">Phone Number</label>
                <input class="form-input" v-model="f.phone_number" placeholder="+989123456789" required />
              </div>
              
              <div class="form-group">
                <label class="form-label">Country</label>
                <input class="form-input" v-model="f.country" placeholder="Country" required />
              </div>
              
              <button type="submit" class="btn-gradient col-span-full">
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
                Save Address
              </button>
            </form>

            <!-- Loading State -->
            <div v-if="loading" class="flex items-center justify-center py-12">
              <div class="w-12 h-12 border-4 border-green-200 rounded-full animate-spin border-t-green-600"></div>
            </div>

            <!-- Empty State -->
            <div v-else-if="addresses.length === 0" class="text-center py-12">
              <div class="inline-block p-6 bg-gray-100 rounded-full mb-4">
                <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
              </div>
              <p class="text-gray-500">No addresses yet. Add your first address!</p>
            </div>

            <!-- Address List -->
            <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div 
                v-for="(a, index) in addresses" 
                :key="a.id"
                class="address-card group"
                :style="{ animationDelay: `${index * 100}ms` }"
              >
                <!-- Edit Mode -->
                <form v-if="editingAddress === a.id" class="space-y-3" @submit.prevent="updateAddress(a.id)">
                  <input class="form-input" v-model="editForm.street" placeholder="Street" required />
                  <div class="grid grid-cols-2 gap-2">
                    <input class="form-input" v-model="editForm.city" placeholder="City" required />
                    <input class="form-input" v-model="editForm.state" placeholder="State" required />
                  </div>
                  <div class="grid grid-cols-2 gap-2">
                    <input class="form-input" v-model="editForm.postal_code" placeholder="Postal Code" />
                    <input class="form-input" v-model="editForm.phone_number" placeholder="Phone" />
                  </div>
                  <div class="flex gap-2">
                    <button type="submit" class="btn-gradient flex-1">Save</button>
                    <button type="button" class="btn-secondary flex-1" @click="editingAddress = null">Cancel</button>
                  </div>
                </form>

                <!-- View Mode -->
                <div v-else>
                  <div class="flex items-start justify-between mb-3">
                    <div class="flex items-start space-x-3">
                      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-green-500 to-emerald-500 flex items-center justify-center flex-shrink-0">
                        <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
                        </svg>
                      </div>
                      <div class="flex-1">
                        <h3 class="font-bold text-gray-800 mb-1">{{ a.street }}</h3>
                        <p class="text-sm text-gray-600">{{ a.city }}, {{ a.state }} {{ a.postal_code }}</p>
                        <p class="text-sm text-gray-500 mt-1 flex items-center">
                          <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                          </svg>
                          {{ a.phone_number }}
                        </p>
                      </div>
                    </div>
                    
                    <span v-if="a.is_default" class="px-3 py-1 bg-gradient-to-r from-green-500 to-emerald-500 text-white text-xs rounded-full font-semibold">
                      Default
                    </span>
                  </div>

                  <div class="flex gap-2 mt-4">
                    <button @click="startEdit(a)" class="btn-icon flex-1" title="Edit">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                      </svg>
                    </button>
                    <button v-if="!a.is_default" @click="setDefault(a.id)" class="btn-icon flex-1" title="Set as Default">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                      </svg>
                    </button>
                    <button @click="remove(a.id)" class="btn-icon-danger flex-1" title="Delete">
                      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
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
const f = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '', country: 'Iran' })
const editForm = reactive({ street: '', city: '', state: '', postal_code: '', phone_number: '' })
const profileForm = reactive({ 
  username: '', 
  email: '', 
  first_name: '', 
  last_name: '', 
  birth_date: '' 
})

function getInitials(user: any) {
  if (!user) return '?'
  const first = user.first_name?.[0] || user.username?.[0] || '?'
  const last = user.last_name?.[0] || ''
  return (first + last).toUpperCase()
}

function formatDate(dateString: string) {
  if (!dateString) return 'Not set'
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

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
  try {
    await api.post('/api/addresses/', f)
    Object.assign(f, { street: '', city: '', state: '', postal_code: '', phone_number: '', country: 'Iran' })
    showForm.value = false
    await loadAddresses()
  } catch (e: any) {
    alert(e.response?.data?.detail || e.response?.data?.phone_number?.[0] || 'Failed to create address')
  }
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

@keyframes pulseSlow {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.9;
  }
}

.animate-fadeIn {
  animation: fadeIn 0.6s ease-out;
}

.profile-card {
  animation: slideInUp 0.5s ease-out backwards;
}

.address-card {
  @apply bg-gradient-to-br from-white to-gray-50 rounded-xl p-5 border border-gray-200 hover:border-green-300 hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1;
  animation: slideInUp 0.5s ease-out backwards;
}

.animate-pulse-slow {
  animation: pulseSlow 3s ease-in-out infinite;
}

/* Gradient text */
.bg-clip-text {
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Form Styles */
.form-group {
  @apply space-y-2;
}

.form-label {
  @apply text-sm font-semibold text-gray-700 flex items-center space-x-2;
}

.form-input {
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-purple-400 focus:ring-4 focus:ring-purple-100 focus:outline-none transition-all duration-300;
}

/* Buttons */
.btn-gradient {
  @apply px-6 py-3 bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 text-white rounded-xl font-semibold hover:shadow-xl transform hover:scale-105 transition-all duration-300 flex items-center justify-center;
}

.btn-secondary {
  @apply px-6 py-3 bg-gray-200 text-gray-800 rounded-xl font-semibold hover:bg-gray-300 transition-all duration-300;
}

.btn-icon {
  @apply p-2 bg-gray-100 hover:bg-blue-100 text-gray-700 hover:text-blue-600 rounded-lg transition-all duration-300;
}

.btn-icon-danger {
  @apply p-2 bg-gray-100 hover:bg-red-100 text-gray-700 hover:text-red-600 rounded-lg transition-all duration-300;
}

/* Info Cards */
.info-card {
  @apply flex items-center space-x-4 p-4 bg-gradient-to-br from-gray-50 to-white rounded-xl border border-gray-200 hover:border-purple-300 hover:shadow-md transition-all duration-300;
}

.info-icon {
  @apply w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0;
}

.info-label {
  @apply text-xs font-semibold text-gray-500 uppercase tracking-wide;
}

.info-value {
  @apply text-base font-bold text-gray-800 mt-1;
}

/* Glass morphism */
.backdrop-blur-sm {
  backdrop-filter: blur(8px);
}
</style>
