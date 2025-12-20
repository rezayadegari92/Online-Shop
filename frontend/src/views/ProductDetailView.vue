<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-950 dark:via-gray-900 dark:to-gray-950 py-8">
    <!-- Loading State -->
    <div v-if="!product" class="container-custom">
      <div class="animate-pulse">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="skeleton h-96 rounded-2xl"></div>
          <div class="space-y-4">
            <div class="skeleton h-8 w-3/4 rounded"></div>
            <div class="skeleton h-6 w-1/2 rounded"></div>
            <div class="skeleton h-32 rounded"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Content -->
    <div v-else class="container-custom space-y-8">
      <!-- Breadcrumb -->
      <nav class="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400 animate-fade-in">
        <router-link to="/" class="hover:text-blue-600 dark:hover:text-blue-400 transition">Home</router-link>
        <span>/</span>
        <router-link to="/products" class="hover:text-blue-600 dark:hover:text-blue-400 transition">Products</router-link>
        <span>/</span>
        <span class="text-gray-900 dark:text-gray-100 font-medium">{{ product.name }}</span>
      </nav>

      <!-- Main Product Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12 animate-fade-in-up">
        <!-- Image Gallery -->
        <div class="space-y-4">
          <!-- Main Image -->
          <div class="relative group">
            <div class="absolute inset-0 bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all duration-300 opacity-0 group-hover:opacity-100"></div>
            <div class="relative card overflow-hidden">
              <img
                :src="getImageUrl(product.images?.[activeImageIndex]?.image_url || product.images?.[activeImageIndex]?.image)"
                :alt="product.name"
                class="w-full h-96 lg:h-[500px] object-cover rounded-xl"
                @error="handleImageError"
              />

              <!-- Discount Badge -->
              <div v-if="product.discount_percent > 0" class="absolute top-4 left-4 z-10">
                <div class="badge badge-danger text-lg font-bold px-4 py-2 shadow-lg animate-pulse">
                  -{{ product.discount_percent }}% OFF
                </div>
              </div>

              <!-- Favorite Button -->
              <button
                @click="handleToggleWishlist"
                :disabled="togglingWishlist"
                class="absolute top-4 right-4 bg-white dark:bg-gray-800 p-3 rounded-full shadow-lg hover:scale-110 transition-transform duration-300 group"
              >
                <svg
                  v-if="togglingWishlist"
                  class="w-6 h-6 text-gray-400 animate-spin"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <svg
                  v-else
                  class="w-6 h-6 group-hover:scale-110 transition-transform"
                  :class="isInWishlist ? 'text-red-500' : 'text-gray-400'"
                  :fill="isInWishlist ? 'currentColor' : 'none'"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Thumbnail Gallery -->
          <div v-if="product.images && product.images.length > 1" class="flex gap-3 overflow-x-auto pb-2">
            <button
              v-for="(img, index) in product.images"
              :key="img.id"
              @click="activeImageIndex = index"
              :class="[
                'flex-shrink-0 w-20 h-20 rounded-xl overflow-hidden border-2 transition-all duration-300',
                activeImageIndex === index
                  ? 'border-blue-500 scale-110 shadow-lg'
                  : 'border-gray-300 dark:border-gray-600 hover:border-blue-400 opacity-70 hover:opacity-100'
              ]"
            >
              <img
                :src="getImageUrl(img.image_url || img.image)"
                :alt="`${product.name} ${index + 1}`"
                class="w-full h-full object-cover"
              />
            </button>
          </div>
        </div>

        <!-- Product Info -->
        <div class="space-y-6">
          <!-- Title & Category -->
          <div class="space-y-3">
            <div class="flex items-center gap-3">
              <span v-if="product.brand" class="badge badge-info">{{ product.brand.name }}</span>
              <span class="badge badge-secondary">{{ product.category?.name }}</span>
            </div>

            <h1 class="text-4xl lg:text-5xl font-bold text-gray-900 dark:text-white leading-tight">
              {{ product.name }}
            </h1>
          </div>

          <!-- Rating & Reviews -->
          <div class="flex items-center gap-4">
            <div class="flex items-center gap-1">
              <svg v-for="n in 5" :key="n" :class="n <= averageRating ? 'star-filled' : 'star-empty'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            </div>
            <span class="text-lg font-semibold text-gray-700 dark:text-gray-300">
              {{ averageRating.toFixed(1) }}
            </span>
            <span class="text-gray-500 dark:text-gray-400">
              ({{ product.ratings?.length || 0 }} reviews)
            </span>
          </div>

          <!-- Price -->
          <div class="space-y-2">
            <div class="flex items-baseline gap-4">
              <span class="text-5xl font-bold text-gradient">
                {{ currency(product.discounted_price || product.price) }}
              </span>
              <span v-if="product.discount_percent > 0" class="price-old text-2xl">
                {{ currency(product.price) }}
              </span>
            </div>
            <p v-if="product.discount_percent > 0" class="text-green-600 dark:text-green-400 text-lg font-semibold">
              You save {{ currency(product.price - (product.discounted_price || product.price)) }}!
            </p>
          </div>

          <!-- Description -->
          <div class="card p-6">
            <h3 class="text-xl font-semibold mb-3 text-gray-900 dark:text-white">Product Details</h3>
            <p class="text-gray-600 dark:text-gray-300 leading-relaxed">
              {{ product.details || 'No description available for this product.' }}
            </p>
          </div>

          <!-- Stock Status -->
          <div class="flex items-center gap-3">
            <span class="text-gray-700 dark:text-gray-300 font-medium">Availability:</span>
            <span :class="product.quantity > 0 ? 'badge-success' : 'badge-danger'" class="badge">
              {{ product.quantity > 0 ? `In Stock (${product.quantity} available)` : 'Out of Stock' }}
            </span>
          </div>

          <!-- Add to Cart Section -->
          <div class="space-y-4">
            <div class="flex items-center gap-4">
              <label class="text-gray-700 dark:text-gray-300 font-medium">Quantity:</label>
              <div class="flex items-center border-2 border-gray-300 dark:border-gray-600 rounded-xl overflow-hidden">
                <button @click="decreaseQuantity" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
                  </svg>
                </button>
                <input v-model.number="quantity" type="number" min="1" :max="product.quantity" class="w-20 text-center bg-white dark:bg-gray-800 text-gray-900 dark:text-white font-semibold focus:outline-none" />
                <button @click="increaseQuantity" class="px-4 py-2 bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
                  </svg>
                </button>
              </div>
            </div>

            <div class="flex gap-4">
              <button
                @click="addToCart"
                :disabled="product.quantity === 0"
                class="flex-1 btn btn-primary text-lg py-4 flex items-center justify-center gap-3"
              >
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
                Add to Cart
              </button>
              <button class="btn btn-secondary px-6 py-4">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                </svg>
              </button>
            </div>
          </div>

          <!-- Additional Info Cards -->
          <div class="grid grid-cols-2 gap-4">
            <div class="card p-4 text-center">
              <svg class="w-8 h-8 mx-auto mb-2 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">Quality Guaranteed</p>
            </div>
            <div class="card p-4 text-center">
              <svg class="w-8 h-8 mx-auto mb-2 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 8h14M5 8a2 2 0 110-4h14a2 2 0 110 4M5 8v10a2 2 0 002 2h10a2 2 0 002-2V8m-9 4h4" />
              </svg>
              <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">Free Shipping</p>
            </div>
            <div class="card p-4 text-center">
              <svg class="w-8 h-8 mx-auto mb-2 text-purple-600 dark:text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
              <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">Secure Payment</p>
            </div>
            <div class="card p-4 text-center">
              <svg class="w-8 h-8 mx-auto mb-2 text-orange-600 dark:text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">Easy Returns</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Reviews & Comments Section -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-fade-in-up delay-200">
        <!-- Reviews Section -->
        <div class="card p-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Customer Reviews</h2>
            <span class="badge badge-info text-lg px-4 py-2">
              {{ product.ratings?.length || 0 }} reviews
            </span>
          </div>

          <!-- Add Rating -->
          <div class="mb-8 p-6 bg-gradient-to-br from-blue-50 to-purple-50 dark:from-gray-800 dark:to-gray-700 rounded-2xl">
            <h3 class="text-lg font-semibold mb-4 text-gray-900 dark:text-white">Rate this product</h3>
            <div class="flex items-center gap-4">
              <div class="flex gap-2">
                <button
                  v-for="n in 5"
                  :key="n"
                  @click="selectedRating = n"
                  class="transition-transform hover:scale-125"
                >
                  <svg :class="n <= selectedRating ? 'text-yellow-400' : 'text-gray-300 dark:text-gray-600'" class="w-10 h-10" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </button>
              </div>
              <button @click="submitRating" class="btn btn-primary">
                Submit Rating
              </button>
            </div>
          </div>

          <!-- Ratings List -->
          <div class="space-y-4 max-h-96 overflow-y-auto">
            <div v-if="!product.ratings || product.ratings.length === 0" class="empty-state">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
              </svg>
              <p class="text-lg">No reviews yet. Be the first to review!</p>
            </div>

            <div v-for="rating in product.ratings" :key="rating.id" class="p-4 bg-gray-50 dark:bg-gray-700 rounded-xl">
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div class="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                    {{ rating.user?.charAt(0)?.toUpperCase() || 'U' }}
                  </div>
                  <span class="font-semibold text-gray-900 dark:text-white">{{ rating.user || 'Anonymous' }}</span>
                </div>
                <div class="flex gap-1">
                  <svg v-for="n in rating.value" :key="n" class="w-5 h-5 star-filled" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              </div>
              <p class="text-sm text-gray-500 dark:text-gray-400">{{ new Date(rating.created_at).toLocaleDateString() }}</p>
            </div>
          </div>
        </div>

        <!-- Comments Section -->
        <div class="card p-8">
          <div class="flex items-center justify-between mb-6">
            <h2 class="text-3xl font-bold text-gray-900 dark:text-white">Comments</h2>
            <span class="badge badge-info text-lg px-4 py-2">
              {{ product.comments?.length || 0 }} comments
            </span>
          </div>

          <!-- Add Comment -->
          <form @submit.prevent="submitComment" class="mb-8">
            <textarea
              v-model="newComment"
              placeholder="Share your thoughts about this product..."
              rows="4"
              class="input resize-none mb-4"
              required
            ></textarea>
            <button type="submit" class="btn btn-primary w-full">
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
              Post Comment
            </button>
          </form>

          <!-- Comments List -->
          <div class="space-y-4 max-h-96 overflow-y-auto">
            <div v-if="!product.comments || product.comments.length === 0" class="empty-state">
              <svg class="w-16 h-16 mx-auto mb-4 text-gray-300 dark:text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <p class="text-lg">No comments yet. Start the conversation!</p>
            </div>

            <div v-for="comment in product.comments" :key="comment.id" class="p-4 bg-gray-50 dark:bg-gray-700 rounded-xl">
              <div class="flex items-start gap-3">
                <div class="w-10 h-10 bg-gradient-to-br from-green-500 to-teal-500 rounded-full flex items-center justify-center text-white font-bold flex-shrink-0">
                  {{ comment.author?.charAt(0)?.toUpperCase() || 'U' }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="flex items-center gap-2 mb-1">
                    <span class="font-semibold text-gray-900 dark:text-white">{{ comment.author || 'Anonymous' }}</span>
                    <span class="text-sm text-gray-500 dark:text-gray-400">•</span>
                    <span class="text-sm text-gray-500 dark:text-gray-400">
                      {{ new Date(comment.created_at).toLocaleDateString() }}
                    </span>
                  </div>
                  <p class="text-gray-700 dark:text-gray-300 leading-relaxed break-words">
                    {{ comment.content }}
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Related Products (Optional) -->
      <div v-if="relatedProducts && relatedProducts.length > 0" class="animate-fade-in-up delay-400">
        <h2 class="text-3xl font-bold text-gray-900 dark:text-white mb-8">You Might Also Like</h2>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="relatedProduct in relatedProducts" :key="relatedProduct.id" class="product-card">
            <router-link :to="`/products/${relatedProduct.id}`">
              <img :src="getImageUrl(relatedProduct.images?.[0]?.image_url)" class="product-image" />
              <div class="p-4">
                <h3 class="font-semibold text-gray-900 dark:text-white truncate">{{ relatedProduct.name }}</h3>
                <p class="text-xl font-bold text-blue-600 dark:text-blue-400 mt-2">
                  {{ currency(relatedProduct.discounted_price || relatedProduct.price) }}
                </p>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/http'
import { useCartStore } from '../stores/cart.store'
import { useWishlistStore } from '../stores/wishlist.store'
import { useAuthStore } from '../stores/auth.store'
import { getImageUrl } from '../utils/image'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const wishlistStore = useWishlistStore()
const authStore = useAuthStore()

const product = ref<any>(null)
const relatedProducts = ref<any[]>([])
const activeImageIndex = ref(0)
const quantity = ref(1)
const newComment = ref('')
const selectedRating = ref(5)
const togglingWishlist = ref(false)

const placeholder = 'https://placehold.co/600x400?text=No+Image'

// Computed property to check if product is in wishlist
const isInWishlist = computed(() => {
  if (!product.value) return false
  return wishlistStore.isInWishlist(product.value.id)
})

// Computed property for average rating
const averageRating = computed(() => {
  if (!product.value?.ratings || product.value.ratings.length === 0) return 0
  const sum = product.value.ratings.reduce((acc: number, rating: any) => acc + rating.value, 0)
  return Math.round(sum / product.value.ratings.length)
})

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(n)
}

async function load() {
  try {
    const { data } = await api.get(`/api/products/${route.params.id}/`)
    product.value = data

    // Load related products from same category
    if (data.category?.id) {
      const { data: related } = await api.get(`/api/categories/${data.category.id}/products/`, {
        params: { page_size: 4 }
      })
      relatedProducts.value = related.results?.filter((p: any) => p.id !== data.id).slice(0, 4) || []
    }
  } catch (error) {
    console.error('Error loading product:', error)
    router.push('/products')
  }
}

function handleImageError(event: Event) {
  const img = event.target as HTMLImageElement
  img.src = placeholder
}

function increaseQuantity() {
  if (quantity.value < product.value.quantity) {
    quantity.value++
  }
}

function decreaseQuantity() {
  if (quantity.value > 1) {
    quantity.value--
  }
}

async function addToCart() {
  try {
    await cart.add(Number(route.params.id), quantity.value)
    // Show success notification (you can implement a toast/notification system)
    alert(`Added ${quantity.value} item(s) to cart!`)
  } catch (e: any) {
    if (e.response?.status === 401) {
      alert('Please log in to add items to cart')
      router.push('/login')
    } else {
      alert(e.response?.data?.detail || 'Failed to add to cart')
    }
  }
}

async function submitComment() {
  if (!newComment.value.trim()) return

  try {
    await api.post(`/api/products/${route.params.id}/`, {
      action: 'comment',
      content: newComment.value
    })
    newComment.value = ''
    await load()
    alert('Comment posted successfully!')
  } catch (e: any) {
    if (e.response?.status === 401) {
      alert('Please log in to post comments')
      router.push('/login')
    } else {
      alert(e.response?.data?.detail || 'Failed to post comment')
    }
  }
}

async function submitRating() {
  try {
    await api.post(`/api/products/${route.params.id}/`, {
      action: 'rate',
      rating: selectedRating.value
    })
    await load()
    alert('Rating submitted successfully!')
  } catch (e: any) {
    if (e.response?.status === 401) {
      alert('Please log in to rate products')
      router.push('/login')
    } else {
      alert(e.response?.data?.detail || 'Failed to submit rating')
    }
  }
}

// Toggle wishlist
async function handleToggleWishlist() {
  if (!authStore.isAuthenticated) {
    alert('Please log in to add items to your wishlist')
    router.push('/login')
    return
  }

  togglingWishlist.value = true
  try {
    const result = await wishlistStore.toggleWishlist(product.value.id)
    if (result.success) {
      // Show success message (you can replace with a toast notification)
      console.log(result.message)
    } else {
      alert(result.error || 'Failed to update wishlist')
    }
  } catch (error) {
    console.error('Error toggling wishlist:', error)
    alert('Failed to update wishlist')
  } finally {
    togglingWishlist.value = false
  }
}

onMounted(() => {
  load()
  // Load wishlist if user is authenticated
  if (authStore.isAuthenticated) {
    wishlistStore.fetchWishlist()
  }
})
</script>
