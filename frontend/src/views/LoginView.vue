<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <!-- Animated Background Shapes -->
      <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-purple-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Login Card -->
      <div class="relative bg-white rounded-3xl shadow-2xl overflow-hidden animate-slideUp">
        <!-- Gradient Header -->
        <div class="relative h-32 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 overflow-hidden">
          <div class="absolute inset-0 bg-pattern opacity-10"></div>
          <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32 animate-pulse-slow"></div>
          <div class="relative h-full flex items-center justify-center">
            <div class="text-center">
              <div class="inline-block p-4 bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl mb-2">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1" />
                </svg>
              </div>
              <h1 class="text-3xl font-bold text-white">Welcome Back</h1>
            </div>
          </div>
        </div>

        <!-- Form Content -->
        <form class="p-8 space-y-6" @submit.prevent="submit">
          <p class="text-center text-gray-600">Sign in to your account to continue</p>
          
          <!-- Email/Username Input -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
              <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              <span>Email or Username</span>
            </label>
            <div class="relative group">
              <input 
                class="auth-input peer" 
                v-model="email_or_username" 
                placeholder="Enter your email or username"
                required
              />
              <div class="input-border"></div>
            </div>
          </div>

          <!-- Password Input -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
              <svg class="w-4 h-4 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Password</span>
            </label>
            <div class="relative group">
              <input 
                class="auth-input peer" 
                v-model="password" 
                type="password" 
                placeholder="Enter your password"
                required
              />
              <div class="input-border"></div>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full btn-gradient group"
            :disabled="loading"
          >
            <span v-if="!loading" class="flex items-center justify-center space-x-2">
              <span>Sign In</span>
              <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <span v-else class="flex items-center justify-center space-x-2">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Signing in...</span>
            </span>
          </button>

          <!-- Divider -->
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-4 bg-white text-gray-500">Don't have an account?</span>
            </div>
          </div>

          <!-- Sign Up Link -->
          <router-link 
            to="/signup"
            class="block w-full text-center px-6 py-3 border-2 border-indigo-600 text-indigo-600 rounded-xl font-semibold hover:bg-indigo-50 transition-all duration-300 transform hover:scale-105"
          >
            Create Account
          </router-link>
        </form>
      </div>

      <!-- Footer Text -->
      <p class="text-center mt-6 text-gray-600 text-sm">
        Secure login powered by JWT authentication
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth.store'
import { useRouter, useRoute } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email_or_username = ref('')
const password = ref('')
const loading = ref(false)

async function submit() {
  loading.value = true
  try {
    await auth.login({ email_or_username: email_or_username.value, password: password.value })
    const redirect = (route.query.redirect as string) || '/'
    router.replace(redirect)
  } catch (e: any) {
    alert(e.response?.data?.detail || 'Login failed. Please check your credentials.')
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
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-transparent focus:outline-none transition-all duration-300;
}

.input-border {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 transition-all duration-300 rounded-full;
}

.auth-input:focus ~ .input-border {
  @apply w-full h-1;
}

.btn-gradient {
  @apply px-8 py-4 bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none;
}
</style>
