<template>
  <div class="max-w-5xl mx-auto p-6" v-if="product">
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <img :src="product.images?.[active]?.image_url || placeholder" class="w-full h-80 object-cover rounded" />
        <div class="flex gap-2 mt-2 overflow-x-auto">
          <img v-for="(img, i) in product.images" :key="img.id" :src="img.image_url" class="h-16 w-16 object-cover rounded border cursor-pointer" @click="active = i" />
        </div>
      </div>
      <div>
        <h1 class="text-2xl font-semibold">{{ product.name }}</h1>
        <div class="text-lg text-gray-700 my-2">{{ currency(product.discounted_price ?? product.price) }}</div>
        <p class="text-sm text-gray-600 mb-4">{{ product.details }}</p>
        <div class="flex gap-2">
          <button class="btn" @click="addToCart()">Add to cart</button>
        </div>
      </div>
    </div>

    <div class="mt-10 grid grid-cols-1 md:grid-cols-2 gap-6">
      <div>
        <h2 class="text-lg font-semibold mb-2">Comments</h2>
        <form class="mb-3 flex gap-2" @submit.prevent="submitComment">
          <input class="flex-1 border rounded px-3 py-2" v-model="comment" placeholder="Write a comment" />
          <button class="btn">Send</button>
        </form>
        <div class="space-y-2">
          <div v-for="c in product.comments" :key="c.id" class="border rounded p-3">
            <div class="text-sm text-gray-600">{{ c.author }} • {{ new Date(c.created_at).toLocaleString() }}</div>
            <div>{{ c.content }}</div>
          </div>
        </div>
      </div>
      <div>
        <h2 class="text-lg font-semibold mb-2">Rate</h2>
        <div class="flex items-center gap-2">
          <select class="border rounded px-2 py-1" v-model.number="rating">
            <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
          </select>
          <button class="btn" @click="submitRating">Submit Rating</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../utils/http'
import { useCartStore } from '../stores/cart.store'
import { useAuthStore } from '../stores/auth.store'

const route = useRoute()
const router = useRouter()
const cart = useCartStore()
const auth = useAuthStore()
const product = ref<any>(null)
const active = ref(0)
const comment = ref('')
const rating = ref(5)
const placeholder = 'https://placehold.co/600x400?text=No+Image'

function currency(v: string | number) {
  const n = typeof v === 'number' ? v : parseFloat(v as string)
  return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'IRR', maximumFractionDigits: 0 }).format(n)
}

async function load() {
  const { data } = await api.get(`/api/products/${route.params.id}/`)
  product.value = data
}

async function addToCart() {
  try {
    await cart.add(Number(route.params.id), 1)
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
  if (!comment.value) return
  await api.post(`/api/products/${route.params.id}/`, { action: 'comment', content: comment.value })
  comment.value = ''
  await load()
}

async function submitRating() {
  await api.post(`/api/products/${route.params.id}/`, { action: 'rate', rating: rating.value })
  await load()
}

onMounted(load)
</script>

<style scoped>
.btn { @apply bg-black text-white rounded px-3 py-2; }
</style>


