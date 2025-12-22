<template>
  <div class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-600 hover:shadow-lg transition-all duration-300 transform hover:scale-105">
    <div class="text-4xl mb-3">{{ icon }}</div>
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">{{ name }}</h3>
    <p class="text-sm text-gray-700 dark:text-gray-300">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  name: string
  description: string
  icon: string
  color?: string
}>()
</script>


