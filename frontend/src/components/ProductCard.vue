<template>
  <div class="group bg-white dark:bg-gray-800 rounded-2xl overflow-hidden shadow-md hover:shadow-xl dark:shadow-gray-900/50 transition-all duration-300 flex flex-col h-full">
    <router-link :to="`/products/${product.id}`" class="block flex-1 flex flex-col">
      <div class="relative overflow-hidden bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-800">
        <!-- Image Container with better sizing -->
        <div class="w-full aspect-square flex items-center justify-center bg-white dark:bg-gray-700 p-3 sm:p-4">
          <img
            :src="getImage()"
            class="w-full h-full max-w-full max-h-full object-contain group-hover:scale-110 transition-transform duration-500"
            :alt="product.name"
            @error="handleImageError"
          />
        </div>
        
        <!-- Discount Badge -->
        <div v-if="product.discount_percent > 0" class="absolute top-3 right-3 bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-1.5 rounded-full text-xs sm:text-sm font-bold shadow-lg z-10">
          -{{ product.discount_percent }}%
        </div>
        
        <!-- Wishlist Button -->
        <div class="absolute top-3 left-3 z-10">
          <WishlistButton :product-id="product.id" variant="floating" size="md" />
        </div>
      </div>
      
      <!-- Product Info -->
      <div class="p-4 sm:p-5 bg-white dark:bg-gray-800 flex-1 flex flex-col">
        <!-- Brand -->
        <p v-if="product.brand" class="text-xs text-gray-500 dark:text-gray-400 mb-1 font-medium uppercase tracking-wide">
          {{ getBrandName() }}
        </p>
        
        <!-- Product Name -->
        <h3 class="font-semibold text-sm sm:text-base mb-3 text-gray-900 dark:text-gray-100 line-clamp-2 min-h-[2.5rem] leading-tight">
          {{ product.name }}
        </h3>
        
        <!-- Rating -->
        <div v-if="hasRating(product)" class="flex items-center gap-1 mb-3">
          <div class="flex items-center text-yellow-500 dark:text-yellow-400">
            <svg class="w-4 h-4 fill-current" viewBox="0 0 20 20">
              <path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/>
            </svg>
          </div>
          <span class="text-xs sm:text-sm font-medium text-gray-700 dark:text-gray-300">{{ getRating(product) }}</span>
        </div>
        
        <!-- Price -->
        <div class="mt-auto pt-2">
          <div class="flex items-baseline gap-2 flex-wrap">
            <span class="text-lg sm:text-xl font-bold text-blue-600 dark:text-blue-400">
              {{ currency(product.discounted_price ?? product.price) }}
            </span>
            <span v-if="product.discount_percent > 0" class="text-sm text-gray-400 dark:text-gray-500 line-through">
              {{ currency(product.price) }}
            </span>
          </div>
        </div>
      </div>
    </router-link>
    
    <!-- Add to Cart Button -->
    <div class="p-4 sm:p-5 pt-0">
      <button class="w-full btn" @click.prevent="handleAddToCart">
        <span class="flex items-center justify-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          Add to Cart
        </span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { getProductImageUrl } from '../utils/image'
import WishlistButton from './products/WishlistButton.vue'

const props = defineProps<{
  product: any
}>()

const emit = defineEmits<{
  'add-to-cart': [productId: number]
}>()

const placeholder = 'https://placehold.co/600x400?text=No+Image'

function getImage() {
  return getProductImageUrl(props.product)
}

function getBrandName() {
  if (typeof props.product.brand === 'string') return props.product.brand
  if (props.product.brand && props.product.brand.name) return props.product.brand.name
  return ''
}

function hasRating(product: any): boolean {
  const rating = product.average_rating ?? product.avg_rating
  return rating !== null && rating !== undefined && rating !== 0
}

function getRating(product: any): string | number {
  return product.average_rating ?? product.avg_rating ?? 0
}

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(n)
}

function handleAddToCart() {
  emit('add-to-cart', props.product.id)
}

function handleImageError(event: Event) {
  // Fallback to placeholder if image fails to load
  const img = event.target as HTMLImageElement
  if (img.src !== placeholder) {
    img.src = placeholder
  }
}
</script>

<style scoped>
.btn {
  @apply bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-xl px-4 py-2.5 sm:py-3 hover:from-blue-700 hover:to-blue-800 transition-all duration-200 font-semibold text-sm sm:text-base shadow-md hover:shadow-lg transform hover:scale-[1.02] active:scale-[0.98];
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
