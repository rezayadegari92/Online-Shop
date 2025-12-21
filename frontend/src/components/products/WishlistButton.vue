<template>
  <button
    @click.prevent.stop="handleToggle"
    :disabled="loading"
    :class="buttonClass"
    :title="isInWishlist ? 'Remove from wishlist' : 'Add to wishlist'"
    class="group relative"
  >
    <!-- Loading Spinner -->
    <svg
      v-if="loading"
      class="w-5 h-5 animate-spin"
      :class="spinnerClass"
      fill="none"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
      />
    </svg>

    <!-- Heart Icon -->
    <svg
      v-else
      class="transition-all duration-300"
      :class="heartClass"
      :fill="isInWishlist ? 'currentColor' : 'none'"
      stroke="currentColor"
      viewBox="0 0 24 24"
    >
      <path
        stroke-linecap="round"
        stroke-linejoin="round"
        stroke-width="2"
        d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z"
      />
    </svg>

    <!-- Pulse Effect on Add -->
    <span
      v-if="showPulse"
      class="absolute inset-0 rounded-full bg-red-500 animate-ping opacity-75"
    ></span>
  </button>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useWishlistStore } from '../../stores/wishlist.store'
import { useAuthStore } from '../../stores/auth.store'
import { showToast } from '../../utils/toast'

interface Props {
  productId: number
  size?: 'sm' | 'md' | 'lg'
  variant?: 'default' | 'floating' | 'icon-only'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'default',
})

const router = useRouter()
const wishlistStore = useWishlistStore()
const authStore = useAuthStore()

const loading = ref(false)
const showPulse = ref(false)

// Check if product is in wishlist
const isInWishlist = computed(() => {
  return wishlistStore.isInWishlist(props.productId)
})

// Size classes
const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-5 h-5',
  lg: 'w-6 h-6',
}

// Button classes based on variant
const buttonClass = computed(() => {
  const baseClasses = 'transition-all duration-300 disabled:opacity-50 disabled:cursor-not-allowed'

  switch (props.variant) {
    case 'floating':
      return `${baseClasses} absolute top-3 right-3 z-10 bg-white dark:bg-gray-800 p-2 rounded-full shadow-lg hover:shadow-xl hover:scale-110`
    case 'icon-only':
      return `${baseClasses} p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800`
    default:
      return `${baseClasses} p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 hover:scale-110`
  }
})

// Heart icon classes
const heartClass = computed(() => {
  const sizeClass = sizeClasses[props.size]
  const colorClass = isInWishlist.value
    ? 'text-red-500 scale-110'
    : 'text-gray-400 dark:text-gray-500 group-hover:text-red-400 group-hover:scale-110'
  return `${sizeClass} ${colorClass}`
})

// Spinner classes
const spinnerClass = computed(() => {
  return `${sizeClasses[props.size]} text-gray-400`
})

// Handle toggle wishlist
async function handleToggle() {
  // Check if user is authenticated
  if (!authStore.isAuthenticated) {
    showToast.warning('Please log in to add items to your wishlist')
    router.push('/login')
    return
  }

  loading.value = true

  try {
    const result = await wishlistStore.toggleWishlist(props.productId)

    if (result.success) {
      // Show pulse effect when adding to wishlist
      if (result.inWishlist) {
        showPulse.value = true
        setTimeout(() => {
          showPulse.value = false
        }, 600)
      }
      showToast.success(result.message || 'Wishlist updated!')
    } else {
      console.error('Failed to toggle wishlist:', result.error)
      showToast.error(result.error || 'Failed to update wishlist')
    }
  } catch (error) {
    console.error('Error toggling wishlist:', error)
    showToast.error('Failed to update wishlist. Please try again.')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
@keyframes pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.5;
  }
}

.animate-pulse {
  animation: pulse 0.6s ease-in-out;
}
</style>
