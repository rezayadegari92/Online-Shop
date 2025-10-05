<template>
  <div class="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-red-50 flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <!-- Animated Background Shapes -->
      <div class="fixed inset-0 overflow-hidden pointer-events-none">
        <div class="absolute top-20 left-10 w-72 h-72 bg-amber-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div class="absolute top-40 right-10 w-72 h-72 bg-orange-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div class="absolute -bottom-8 left-20 w-72 h-72 bg-red-300 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      <!-- OTP Card -->
      <div class="relative bg-white rounded-3xl shadow-2xl overflow-hidden animate-slideUp">
        <!-- Gradient Header -->
        <div class="relative h-32 bg-gradient-to-r from-amber-600 via-orange-600 to-red-600 overflow-hidden">
          <div class="absolute inset-0 bg-pattern opacity-10"></div>
          <div class="absolute top-0 right-0 w-64 h-64 bg-white opacity-10 rounded-full -mr-32 -mt-32 animate-pulse-slow"></div>
          <div class="relative h-full flex items-center justify-center">
            <div class="text-center">
              <div class="inline-block p-4 bg-white bg-opacity-20 backdrop-blur-sm rounded-2xl mb-2 animate-bounce-slow">
                <svg class="w-10 h-10 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <h1 class="text-3xl font-bold text-white">Verify Your Email</h1>
            </div>
          </div>
        </div>

        <!-- Form Content -->
        <form class="p-8 space-y-6" @submit.prevent="submit">
          <!-- Progress Steps -->
          <div class="flex items-center justify-center space-x-2 mb-4">
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-gradient-to-r from-emerald-500 to-teal-500 flex items-center justify-center text-white font-bold text-sm">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <span class="ml-2 text-sm text-emerald-600 font-semibold">Signed Up</span>
            </div>
            <div class="w-12 h-0.5 bg-gradient-to-r from-emerald-500 to-orange-500"></div>
            <div class="flex items-center">
              <div class="w-8 h-8 rounded-full bg-gradient-to-r from-amber-600 to-orange-600 flex items-center justify-center text-white font-bold text-sm animate-pulse">2</div>
              <span class="ml-2 text-sm font-semibold text-orange-600">Verify</span>
            </div>
          </div>

          <!-- Info Box -->
          <div class="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-orange-200 rounded-2xl p-6 text-center">
            <div class="inline-block p-3 bg-white rounded-full mb-3">
              <svg class="w-8 h-8 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </div>
            <h3 class="font-bold text-gray-800 mb-2">Check Your Email!</h3>
            <p class="text-sm text-gray-600">
              We've sent a verification code to your email address. Please enter it below to complete your registration.
            </p>
          </div>

          <!-- Email Display (Read-only) -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
              <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
              <span>Email Address</span>
            </label>
            <div class="relative">
              <input 
                class="auth-input-readonly" 
                v-model="email" 
                type="email" 
                readonly
              />
              <div class="absolute right-3 top-1/2 transform -translate-y-1/2">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
            </div>
          </div>

          <!-- OTP Input -->
          <div class="space-y-2">
            <label class="text-sm font-semibold text-gray-700 flex items-center space-x-2">
              <svg class="w-4 h-4 text-orange-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Verification Code</span>
              <span class="text-red-500">*</span>
            </label>
            <div class="relative group">
              <input 
                class="auth-input peer text-center text-2xl font-bold tracking-widest" 
                v-model="otp_code" 
                placeholder="000000"
                maxlength="6"
                autofocus
                required
                @input="handleOtpInput"
              />
              <div class="input-border"></div>
            </div>
            <p class="text-xs text-gray-500 text-center mt-2">Enter the 6-digit code sent to your email</p>
          </div>

          <!-- Timer/Resend -->
          <div class="text-center">
            <p class="text-sm text-gray-600">
              Didn't receive the code? 
              <button type="button" class="text-orange-600 font-semibold hover:text-orange-700 underline ml-1">
                Resend Code
              </button>
            </p>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            class="w-full btn-gradient group"
            :disabled="loading || otp_code.length < 6"
          >
            <span v-if="!loading" class="flex items-center justify-center space-x-2">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span>Verify & Continue</span>
            </span>
            <span v-else class="flex items-center justify-center space-x-2">
              <svg class="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Verifying...</span>
            </span>
          </button>

          <!-- Security Note -->
          <div class="flex items-start space-x-2 p-4 bg-blue-50 rounded-xl border border-blue-200">
            <svg class="w-5 h-5 text-blue-600 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <p class="text-xs text-blue-800">
              For your security, this code will expire in 10 minutes. Never share your verification code with anyone.
            </p>
          </div>
        </form>
      </div>

      <!-- Footer Text -->
      <p class="text-center mt-6 text-gray-600 text-sm">
        Having trouble? Contact our support team
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../utils/http'
import { useAuthStore } from '../stores/auth.store'
import { useRouter } from 'vue-router'

const email = ref('')
const otp_code = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

// Auto-fill email from localStorage (set during signup)
onMounted(() => {
  const savedEmail = localStorage.getItem('signup_email')
  if (savedEmail) {
    email.value = savedEmail
  }
})

function handleOtpInput(event: Event) {
  const value = (event.target as HTMLInputElement).value
  // Only allow numbers
  otp_code.value = value.replace(/\D/g, '').slice(0, 6)
}

async function submit() {
  if (otp_code.value.length < 6) {
    alert('Please enter a valid 6-digit verification code')
    return
  }

  loading.value = true
  try {
    const { data } = await api.post('/accounts/api/verify-otp/', { 
      email: email.value, 
      otp_code: otp_code.value 
    })
    auth.setTokens({ access: data.access, refresh: data.refresh })
    localStorage.removeItem('signup_email')
    
    // Success animation
    alert('✅ Email verified successfully! Welcome aboard!')
    router.replace('/profile')
  } catch (e: any) {
    alert(e.response?.data?.error || 'OTP verification failed. Please check your code and try again.')
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

@keyframes bounceSlow {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
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

.animate-bounce-slow {
  animation: bounceSlow 2s ease-in-out infinite;
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

.auth-input-readonly {
  @apply w-full px-4 py-3 border-2 border-gray-200 rounded-xl bg-gray-50 text-gray-600 cursor-not-allowed;
}

.input-border {
  @apply absolute bottom-0 left-0 w-0 h-0.5 bg-gradient-to-r from-amber-600 via-orange-600 to-red-600 transition-all duration-300 rounded-full;
}

.auth-input:focus ~ .input-border {
  @apply w-full h-1;
}

.btn-gradient {
  @apply px-8 py-4 bg-gradient-to-r from-amber-600 via-orange-600 to-red-600 text-white rounded-xl font-bold text-lg shadow-lg hover:shadow-2xl transform hover:scale-[1.02] transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none;
}
</style>
