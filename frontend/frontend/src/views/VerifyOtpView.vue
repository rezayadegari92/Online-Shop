<template>
  <div class="min-h-screen grid place-items-center p-6">
    <form class="w-full max-w-sm space-y-4" @submit.prevent="submit">
      <h1 class="text-2xl font-semibold">Verify OTP</h1>
      <input class="input" v-model="email" placeholder="Email" type="email" />
      <input class="input" v-model="otp_code" placeholder="OTP Code" />
      <button class="btn" :disabled="loading">Verify</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import api from '../utils/http'
import { useAuthStore } from '../stores/auth.store'
import { useRouter } from 'vue-router'

const email = ref('')
const otp_code = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function submit() {
  loading.value = true
  try {
    const { data } = await api.post('/accounts/api/verify-otp/', { email: email.value, otp_code: otp_code.value })
    auth.setTokens({ access: data.access, refresh: data.refresh })
    router.replace('/profile')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2; }
.btn { @apply w-full bg-black text-white rounded px-3 py-2; }
</style>


