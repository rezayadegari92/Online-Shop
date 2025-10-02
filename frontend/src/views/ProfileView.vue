<template>
  <div class="max-w-xl mx-auto p-6 space-y-4">
    <h1 class="text-2xl font-semibold">Profile</h1>
    <div v-if="auth.user" class="space-y-2">
      <div><b>Email:</b> {{ auth.user.email }}</div>
      <div><b>Username:</b> {{ auth.user.username }}</div>
      <div><b>Name:</b> {{ auth.user.first_name }} {{ auth.user.last_name }}</div>
      <div><b>User Type:</b> {{ auth.user.user_type }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth.store'
const auth = useAuthStore()
</script>


