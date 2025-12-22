<template>
  <div class="bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800 rounded-xl p-6 border border-gray-200 dark:border-gray-600">
    <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">{{ title }}</h3>
    <p class="text-gray-700 dark:text-gray-300 mb-4">{{ description }}</p>
    <ul v-if="details && details.length > 0" class="space-y-2">
      <li v-for="(detail, index) in details" :key="index" class="flex items-start text-sm text-gray-600 dark:text-gray-400">
        <span class="text-blue-500 mr-2">•</span>
        <span>{{ detail }}</span>
      </li>
    </ul>
    <pre v-if="code" class="mt-4 bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-xs"><code>{{ code }}</code></pre>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
  details?: string[]
  code?: string
}>()
</script>


