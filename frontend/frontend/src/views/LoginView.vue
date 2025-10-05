<template>
  <div class="min-h-screen grid place-items-center p-6">
    <form class="w-full max-w-sm space-y-4" @submit.prevent="submit">
      <h1 class="text-2xl font-semibold">Login</h1>
      <input class="input" v-model="email_or_username" placeholder="Email or Username" />
      <input class="input" v-model="password" placeholder="Password" type="password" />
      <button class="btn" :disabled="loading">Login</button>
    </form>
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
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2; }
.btn { @apply w-full bg-black text-white rounded px-3 py-2; }
</style>


