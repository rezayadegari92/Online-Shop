<template>
  <div class="min-h-screen bg-gradient-to-br from-emerald-50 via-teal-50 to-cyan-50 flex items-center justify-center p-6 py-12">
    <div class="w-full max-w-2xl">
      <!-- Animated Background Shapes -->
      <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-10 w-72 h-72 bg-emerald-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-teal-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-72 h-72 bg-cyan-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Signup Card -->
      <div class="relative bg-white rounded-3xl shadow-2xl overflow-hidden animate-slideUp">
        <!-- Gradient Header -->
        <div class="relative h-32 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 overflow-hidden">
          <div class="absolute inset-0 bg-pattern opacity-10"></div>
          <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32 animate-pulse-slow"></div>
          <div class="relative h-full flex items-center justify-center">
            <div class="text-center">
              <div class="inline-block p-4 bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl mb-2">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
                </svg>
              </div>
              <h1 class="text-3xl font-bold text-white">Create Account</h1>
            </div>
          </div>
        </div>

        <!-- Form Content -->
        <form class="p-8 space-y-6" @submit.prevent="submit">
          <p class="text-center text-gray-600">Join us today! Fill in your details below</p>
          
          <!-- Progress Steps -->
          <div class="flex items-center justify-center space-x-2 mb-6">
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-600 to-teal-600 flex items-center justify-center text-white font-bold text-sm">1</div>
              <span class="ml-2 text-sm font-semibold text-emerald-600">Sign Up</span>
            </div>
            <div class="w-12 h-0.5 bg-gray-300"></div>
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-gray-500 font-bold text-sm">2</div>
              <span class="ml-2 text-sm text-gray-400">Verify</span>
            </div>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <!-- Email -->
            <div class="space-y-2 md:col-span-2">
              <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
                <span>Email Address</span>
                <span class="text-red-500">*</span>
              </label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.email" type="email" placeholder="your.email@example.com" required />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- Username -->
            <div class="space-y-2">
              <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <span>Username</span>
                <span class="text-xs text-gray-400">(optional)</span>
              </label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.username" placeholder="johndoe" />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- Password -->
            <div class="space-y-2">
              <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
                <span>Password</span>
                <span class="text-red-500">*</span>
              </label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.password" type="password" placeholder="••••••••" required />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- First Name -->
            <div class="space-y-2">
              <label class="text-sm font-semibold text-gray-700">First Name</label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.first_name" placeholder="John" />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- Last Name -->
            <div class="space-y-2">
              <label class="text-sm font-semibold text-gray-700">Last Name</label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.last_name" placeholder="Doe" />
                <div class="input-border"></div>
              </div>
            </div>

            <!-- Birth Date -->
            <div class="space-y-2">
              <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
                <svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <span>Birth Date</span>
                <span class="text-red-500">*</span>
              </label>
              <div class="relative group">
                <input class="auth-input peer" v-model="form.birth_date" type="date" required />
                <div class="input-border"></div>
              </div>
            </div>
          </div>

          <!-- Address Section -->
          <div class="mt-6 p-6 bg-gradient-to-br from-gray-50 to-emerald-50 rounded-2xl border-2 border-emerald-100">
            <div class="flex items-center justify-between mb-4">
              <h3 class="font-bold text-gray-700 flex items-center space-x-2">
                <svg class="w-5 h-5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>Address</span>
              </h3>
              <span class="text-xs text-gray-500 bg-white px-3 py-1 rounded-full">Optional</span>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2 md:col-span-2">
                <input class="auth-input" v-model="form.address.street" placeholder="Street Address" />
              </div>
              <div class="space-y-2">
                <input class="auth-input" v-model="form.address.city" placeholder="City" />
              </div>
              <div class="space-y-2">
                <input class="auth-input" v-model="form.address.state" placeholder="State/Province" />
              </div>
              <div class="space-y-2">
                <input class="auth-input" v-model="form.address.postal_code" placeholder="Postal Code" />
              </div>
              <div class="space-y-2">
                <input class="auth-input" v-model="form.address.phone_number" placeholder="+989123456789" />
              </div>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full btn-gradient group"
            :disabled="loading"
          >
            <span v-if="!loading" class="flex items-center justify-center space-x-2">
              <span>Create Account</span>
              <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <span v-else class="flex items-center justify-center space-x-2">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Creating account...</span>
            </span>
          </button>

          <!-- Divider -->
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4 bg-white text-gray-500">Already have an account?</span>
            </div>
          </div>

          <!-- Login Link -->
          <router-link 
            to="/login"
            class="block w-full text-center px-6 py-3 border-2 border-emerald-600 text-emerald-600 rounded-xl font-semibold hover:bg-emerald-50 transition-all duration-300 transform hover:scale-105"
          >
            Sign In Instead
          </router-link>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import api from '../utils/http'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  email: '', username: '', password: '', first_name: '', last_name: '', birth_date: '',
  address: { street: '', city: '', state: '', postal_code: '', phone_number: '', country: 'Iran' }
})

async function submit() {
  loading.value = true
  try {
    const payload: any = {
      email: form.email,
      password: form.password,
      birth_date: form.birth_date
    }
    
    if (form.username) payload.username = form.username
    if (form.first_name) payload.first_name = form.first_name
    if (form.last_name) payload.last_name = form.last_name
    
    if (form.address.street && form.address.city) {
      payload.address = {
        street: form.address.street,
        city: form.address.city,
        state: form.address.state || form.address.city,
        country: form.address.country || 'Iran'
      }
      if (form.address.postal_code) payload.address.postal_code = form.address.postal_code
      if (form.address.phone_number) payload.address.phone_number = form.address.phone_number
    }
    
    const { data } = await api.post('/accounts/api/signup/', payload)
    localStorage.setItem('signup_email', form.email)
    router.push('/verify-otp')
  } catch (e: any) {
    const errorMsg = e.response?.data?.birth_date?.[0] || 
                     e.response?.data?.password?.[0] ||
                     e.response?.data?.email?.[0] ||
                     e.response?.data?.detail || 
                     'Signup failed. Please try again.'
    alert(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes blob {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

@keyframes pulseSlow {
  0%, 100% {
    transform: scale(1);
    opacity: 0.1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.2;
  }
}

.animate-slideUp {
  animation: slideUp 0.6s ease-out;
}

.animate-blob {
  animation: blob 7s infinite;
}

.animation-delay-2000 {
  animation-delay: 2s;
}

.animation-delay-4000 {
  animation-delay: 4s;
}

.animate-pulse-slow {
  animation: pulseSlow 3s ease-in-out infinite;
}

.bg-pattern {
  background-image: 
    linear-gradient(30deg, transparent 12%, rgba(255, 255, 255, 0.05) 12%, rgba(255, 255, 255, 0.05) 13%, transparent 13%),
    linear-gradient(150deg, transparent 12%, rgba(255, 255, 255, 0.05) 12%, rgba(255, 255, 255, 0.05) 13%, transparent 13%);
  background-size: 60px 60px;
}

.auth-input {
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-transparent focus:outline-none transition-all duration-300 text-gray-900 placeholder:text-gray-400;
}

.input-border {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 transition-all duration-300 rounded-full;
}

.auth-input:focus ~ .input-border {
  @apply w-full h-1;
}

.btn-gradient {
  @apply px-8 py-4 bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none;
}
</style>
