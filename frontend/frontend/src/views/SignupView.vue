<template>
  <div class="min-h-screen grid place-items-center p-6">
    <form class="w-full max-w-md space-y-3" @submit.prevent="submit">
      <h1 class="text-2xl font-semibold">Sign up</h1>
      <input class="input" v-model="form.email" placeholder="Email" type="email" />
      <input class="input" v-model="form.password" placeholder="Password" type="password" />
      <div class="grid grid-cols-2 gap-2">
        <input class="input" v-model="form.first_name" placeholder="First name" />
        <input class="input" v-model="form.last_name" placeholder="Last name" />
      </div>
      <input class="input" v-model="form.birth_date" placeholder="YYYY-MM-DD" />
      <fieldset class="border p-3 rounded">
        <legend>Address (optional)</legend>
        <input class="input" v-model="form.address.street" placeholder="Street" />
        <div class="grid grid-cols-2 gap-2 mt-2">
          <input class="input" v-model="form.address.city" placeholder="City" />
          <input class="input" v-model="form.address.state" placeholder="State" />
        </div>
        <div class="grid grid-cols-2 gap-2 mt-2">
          <input class="input" v-model="form.address.postal_code" placeholder="Postal code" />
          <input class="input" v-model="form.address.phone_number" placeholder="Phone (+989... or 09...)" />
        </div>
      </fieldset>
      <button class="btn" :disabled="loading">Continue</button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import api from '../utils/http'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = reactive({
  email: '', password: '', first_name: '', last_name: '', birth_date: '',
  address: { street: '', city: '', state: '', postal_code: '', phone_number: '' }
})

async function submit() {
  loading.value = true
  try {
    await api.post('/accounts/api/signup/', form)
    router.push('/verify-otp')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.input { @apply w-full border rounded px-3 py-2; }
.btn { @apply w-full bg-black text-white rounded px-3 py-2; }
</style>


