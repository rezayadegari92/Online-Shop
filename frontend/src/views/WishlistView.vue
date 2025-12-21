<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 py-8">
    <div class="container-custom">
      <!-- Header -->
      <div class="flex items-center justify-between mb-8 animate-fade-in">
        <div>
          <h1 class="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            <svg class="w-10 h-10 inline-block mr-3 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
            </svg>
            My Wishlist
          </h1>
          <p class="text-gray-600 dark:text-gray-400 text-lg">
            {{ wishlistStore.count }} {{ wishlistStore.count === 1 ? 'item' : 'items' }} saved
          </p>
        </div>
        <button
          v-if="!wishlistStore.isEmpty"
          @click="handleClearWishlist"
          class="btn btn-danger"
        >
          <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Clear All
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="wishlistStore.loading" class="flex justify-center items-center py-20">
        <div class="spinner"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="wishlistStore.error" class="card p-8 text-center animate-fade-in">
        <svg class="w-16 h-16 mx-auto mb-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Error Loading Wishlist</h2>
        <p class="text-gray-600 dark:text-gray-400 mb-4">{{ wishlistStore.error }}</p>
        <button @click="wishlistStore.fetchWishlist()" class="btn btn-primary">
          Try Again
        </button>
      </div>

      <!-- Empty State -->
      <div v-else-if="wishlistStore.isEmpty" class="empty-state py-20 animate-fade-in">
        <div class="card p-12 text-center max-w-2xl mx-auto">
          <svg class="w-24 h-24 mx-auto mb-6 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
          </svg>
          <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-4">Your Wishlist is Empty</h2>
          <p class="text-xl text-gray-600 dark:text-gray-400 mb-8">
            Start adding products you love to your wishlist!
          </p>
          <router-link to="/products" class="btn btn-primary text-lg">
            <svg class="w-6 h-6 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
            </svg>
            Browse Products
          </router-link>
        </div>
      </div>

      <!-- Wishlist Items Grid -->
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6 animate-fade-in">
        <div
          v-for="(item, index) in wishlistStore.items"
          :key="item.id"
          class="product-card animate-fade-in-up"
          :style="{ animationDelay: `${index * 50}ms` }"
        >
          <!-- Product Image -->
          <div class="relative">
            <router-link :to="`/products/${item.product.id}`">
              <img
                :src="getImageUrl(item.product.images?.[0]?.image_url || item.product.images?.[0]?.image)"
                :alt="item.product.name"
                class="product-image"
                @error="handleImageError"
              />
            </router-link>

            <!-- Discount Badge -->
            <div v-if="item.product.discount_percent > 0" class="product-badge">
              <span class="badge badge-danger text-sm font-bold px-3 py-1">
                -{{ item.product.discount_percent }}%
              </span>
            </div>

            <!-- Remove Button -->
            <button
              @click="handleRemoveFromWishlist(item.product.id)"
              class="absolute top-4 left-4 bg-white dark:bg-gray-800 p-2 rounded-full shadow-lg hover:scale-110 transition-transform duration-300 group"
              :disabled="removingId === item.product.id"
            >
              <svg
                class="w-6 h-6 text-red-500 group-hover:scale-110 transition-transform"
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path fill-rule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clip-rule="evenodd" />
              </svg>
            </button>
          </div>

          <!-- Product Info -->
          <div class="p-4 space-y-3">
            <!-- Brand & Category -->
            <div class="flex items-center gap-2">
              <span v-if="item.product.brand" class="badge badge-info text-xs">
                {{ item.product.brand.name }}
              </span>
              <span v-if="item.product.category" class="badge badge-secondary text-xs">
                {{ item.product.category.name }}
              </span>
            </div>

            <!-- Product Name -->
            <router-link :to="`/products/${item.product.id}`">
              <h3 class="font-bold text-lg text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors line-clamp-2">
                {{ item.product.name }}
              </h3>
            </router-link>

            <!-- Rating -->
            <div v-if="item.product.average_rating" class="flex items-center gap-2">
              <div class="flex">
                <svg v-for="n in 5" :key="n" :class="n <= Math.round(item.product.average_rating || 0) ? 'star-filled' : 'star-empty'" class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                </svg>
              </div>
              <span class="text-sm text-gray-600 dark:text-gray-400">
                {{ item.product.average_rating.toFixed(1) }}
              </span>
            </div>

            <!-- Price -->
            <div class="flex items-baseline gap-2">
              <span class="text-2xl font-bold text-gradient">
                {{ currency(item.product.discounted_price || item.product.price) }}
              </span>
              <span v-if="item.product.discount_percent > 0" class="price-old text-sm">
                {{ currency(item.product.price) }}
              </span>
            </div>

            <!-- Added Date -->
            <p class="text-xs text-gray-500 dark:text-gray-400">
              Added {{ formatDate(item.created_at) }}
            </p>

            <!-- Actions -->
            <div class="flex gap-2 pt-2">
              <button
                @click="handleAddToCart(item.product.id)"
                class="flex-1 btn btn-primary py-2"
                :disabled="addingToCart === item.product.id"
              >
                <svg v-if="addingToCart === item.product.id" class="w-5 h-5 inline animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <svg v-else class="w-5 h-5 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </button>
              <router-link
                :to="`/products/${item.product.id}`"
                class="btn btn-secondary px-4 py-2"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Continue Shopping -->
      <div v-if="!wishlistStore.isEmpty" class="text-center mt-12 animate-fade-in">
        <router-link to="/products" class="btn btn-secondary text-lg">
          <svg class="w-6 h-6 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
          </svg>
          Continue Shopping
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useWishlistStore } from '../stores/wishlist.store'
import { useCartStore } from '../stores/cart.store'
import { getImageUrl } from '../utils/image'
import { showToast } from '../utils/toast'

const router = useRouter()
const wishlistStore = useWishlistStore()
const cartStore = useCartStore()

const removingId = ref<number | null>(null)
const addingToCart = ref<number | null>(null)

const placeholder = 'https://placehold.co/400x400?text=No+Image'

// Currency formatter
function currency(value: string | number) {
  const n = typeof value === 'number' ? value : parseFloat(value as string)
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

// Date formatter
function formatDate(dateString: string) {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = Math.abs(now.getTime() - date.getTime())
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) return 'today'
  if (diffDays === 1) return 'yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`
  return date.toLocaleDateString()
}

// Handle image error
function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = placeholder
}

// Remove from wishlist
async function handleRemoveFromWishlist(productId: number) {
  removingId.value = productId
  const result = await wishlistStore.removeFromWishlist(productId)
  removingId.value = null

  if (!result.success) {
    showToast.error(result.error || 'Failed to remove from wishlist')
  } else {
    showToast.success('Removed from wishlist')
  }
}

// Clear entire wishlist
async function handleClearWishlist() {
  if (!confirm('Are you sure you want to clear your entire wishlist?')) {
    return
  }

  const result = await wishlistStore.clearWishlist()
  if (!result.success) {
    showToast.error(result.error || 'Failed to clear wishlist')
  } else {
    showToast.success('Wishlist cleared')
  }
}

// Add to cart
async function handleAddToCart(productId: number) {
  addingToCart.value = productId
  try {
    await cartStore.add(productId, 1)
    showToast.success('Item added to cart!')
    // Optionally remove from wishlist after adding to cart
    // await wishlistStore.removeFromWishlist(productId)
  } catch (e: any) {
    if (e.response?.status === 401) {
      showToast.warning('Please log in to add items to cart')
      router.push('/login')
    } else {
      showToast.error(e.response?.data?.detail || 'Failed to add to cart')
    }
  } finally {
    addingToCart.value = null
  }
}

// Load wishlist on mount
onMounted(() => {
  wishlistStore.fetchWishlist()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
