<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-pink-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <!-- Animated Background Shapes -->
      <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-10 w-72 h-72 bg-orange-300 dark:bg-orange-900 rounded-full mix-blend-multiply dark:mix-blend-screen filter blur-xl opacity-70 dark:opacity-30 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-red-300 dark:bg-red-900 rounded-full mix-blend-multiply dark:mix-blend-screen filter blur-xl opacity-70 dark:opacity-30 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-72 h-72 bg-pink-300 dark:bg-pink-900 rounded-full mix-blend-multiply dark:mix-blend-screen filter blur-xl opacity-70 dark:opacity-30 animate-blob animation-delay-4000"></div>
      </div>

      <!-- Reset Password Card -->
      <div class="relative bg-white dark:bg-gray-800 rounded-3xl shadow-2xl dark:shadow-gray-900 overflow-hidden animate-slideUp">
        <!-- Gradient Header -->
        <div class="relative h-32 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 overflow-hidden">
          <div class="absolute inset-0 bg-pattern opacity-10"></div>
          <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32 animate-pulse-slow"></div>
          <div class="relative h-full flex items-center justify-center">
            <div class="text-center">
              <div class="inline-block p-4 bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl mb-2">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
                </svg>
              </div>
              <h1 class="text-3xl font-bold text-white">Reset Password</h1>
            </div>
          </div>
        </div>

        <!-- Form Content -->
        <form class="p-8 space-y-6" @submit.prevent="submit">
          <p class="text-center text-gray-600 dark:text-gray-300">
            Enter your new password below
          </p>
          
          <!-- New Password Input -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center space-x-2">
              <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>New Password</span>
            </label>
            <div class="relative group">
              <input 
                class="auth-input peer" 
                v-model="new_password" 
                type="password"
                placeholder="Enter new password"
                required
              />
              <div class="input-border"></div>
            </div>
          </div>

          <!-- Confirm New Password Input -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center space-x-2">
              <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Confirm New Password</span>
            </label>
            <div class="relative group">
              <input 
                class="auth-input peer" 
                v-model="new_password2" 
                type="password"
                placeholder="Confirm new password"
                required
              />
              <div class="input-border"></div>
              <p v-if="new_password2 && new_password !== new_password2" class="text-red-500 text-xs mt-1">Passwords do not match</p>
            </div>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full btn-gradient group"
            :disabled="loading || new_password !== new_password2"
          >
            <span v-if="!loading" class="flex items-center justify-center space-x-2">
              <span>Reset Password</span>
              <svg class="w-5 h-5 transform group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <span v-else class="flex items-center justify-center space-x-2">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Resetting...</span>
            </span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../utils/http'
import { useRouter } from 'vue-router'
import { showToast } from '../utils/toast'

const router = useRouter()
const loading = ref(false)
const email = ref('')
const otp_code = ref('')
const new_password = ref('')
const new_password2 = ref('')

onMounted(() => {
  const savedEmail = localStorage.getItem('forgot_password_email')
  const savedOTP = localStorage.getItem('forgot_password_otp')
  if (!savedEmail) {
    showToast.warning('Please verify OTP first')
    router.push('/forgot-password')
  } else {
    email.value = savedEmail
    otp_code.value = savedOTP || ''
  }
})

async function submit() {
  if (new_password.value !== new_password2.value) {
    showToast.error('Passwords do not match')
    return
  }
  
  loading.value = true
  try {
    const { data } = await api.post('/accounts/api/reset-password/', {
      email: email.value,
      otp_code: otp_code.value,
      new_password: new_password.value,
      new_password2: new_password2.value
    })
    showToast.success(data.message || 'Password reset successfully')
    localStorage.removeItem('forgot_password_email')
    localStorage.removeItem('forgot_password_otp')
    router.push('/login')
  } catch (e: any) {
    const errorMsg = e.response?.data?.error || 
                     e.response?.data?.new_password2?.[0] ||
                     e.response?.data?.detail || 
                     'Failed to reset password. Please try again.'
    showToast.error(errorMsg)
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
  @apply w-full px-4 py-3 border-2 border-gray-200 dark:border-gray-700 rounded-xl focus:border-transparent focus:outline-none transition-all duration-300 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 dark:placeholder:text-gray-500 bg-white dark:bg-gray-700;
}

.input-border {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 transition-all duration-300 rounded-full;
}

.auth-input:focus ~ .input-border {
  @apply w-full h-1;
}

.btn-gradient {
  @apply px-8 py-4 bg-gradient-to-r from-orange-600 via-red-600 to-pink-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none;
}
</style>

