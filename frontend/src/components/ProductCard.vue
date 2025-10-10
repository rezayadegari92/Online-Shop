<template>
  <div class="group bg-white rounded-xl overflow-hidden shadow-md hover:shadow-2xl transition-all duration-300">
    <router-link :to="`/products/${product.id}`" class="block">
      <div class="relative overflow-hidden bg-white">
        <!-- Fixed size container for consistent image display -->
        <div class="w-full h-64 flex items-center justify-center bg-gray-50 p-2">
          <img 
            :src="getImage()" 
            class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300" 
            :alt="product.name"
            @error="handleImageError"
          />
        </div>
        <div v-if="product.discount_percent > 0" class="absolute top-3 right-3 bg-red-500 text-white px-3 py-1.5 rounded-full text-sm font-bold shadow-lg">
          -{{ product.discount_percent }}%
        </div>
      </div>
      <div class="p-4 bg-white">
        <h3 class="font-bold text-base mb-2 text-gray-900 overflow-hidden" style="display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; min-height: 3rem;">{{ product.name }}</h3>
        <div class="flex items-center gap-2 mb-2">
          <span class="text-xl font-bold text-gray-900">{{ currency(product.discounted_price ?? product.price) }}</span>
          <span v-if="product.discount_percent > 0" class="text-sm text-gray-400 line-through">{{ currency(product.price) }}</span>
        </div>
        <div class="flex items-center gap-1 text-yellow-500 text-sm">
          <span>★</span>
          <span>{{ product.average_rating || product.avg_rating || 'N/A' }}</span>
        </div>
        <p v-if="product.brand" class="text-xs text-gray-500 mt-1">{{ getBrandName() }}</p>
      </div>
    </router-link>
    <div class="p-4 pt-0">
      <button class="w-full btn" @click.prevent="handleAddToCart">
        Add to Cart
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  product: any
}>()

const emit = defineEmits<{
  'add-to-cart': [productId: number]
}>()

const placeholder = 'https://placehold.co/600x400?text=No+Image'

function getImage() {
  if (props.product.image) return props.product.image
  if (props.product.images && props.product.images.length > 0) {
    return props.product.images[0].image_url || props.product.images[0].image
  }
  return placeholder
}

function getBrandName() {
  if (typeof props.product.brand === 'string') return props.product.brand
  if (props.product.brand && props.product.brand.name) return props.product.brand.name
  return ''
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
  @apply bg-gradient-to-r from-blue-600 to-blue-700 text-white rounded-lg px-4 py-2 hover:from-blue-700 hover:to-blue-800 transition font-semibold shadow-sm hover:shadow-md;
}
</style>
