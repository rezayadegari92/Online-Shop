import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../utils/http'

export interface WishlistItem {
  id: number
  product: {
    id: number
    name: string
    price: string | number
    discounted_price?: string | number
    discount_percent: number
    images?: Array<{ id: number; image_url?: string; image?: string }>
    brand?: { id: number; name: string }
    category?: { id: number; name: string }
    average_rating?: number
  }
  created_at: string
}

export const useWishlistStore = defineStore('wishlist', () => {
  const items = ref<WishlistItem[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const count = computed(() => items.value.length)
  const isEmpty = computed(() => items.value.length === 0)
  const productIds = computed(() => items.value.map((item) => item.product.id))

  // Check if product is in wishlist
  const isInWishlist = (productId: number): boolean => {
    return productIds.value.includes(productId)
  }

  // Fetch wishlist items
  const fetchWishlist = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get('/api/wishlist/')
      items.value = data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to fetch wishlist'
      console.error('Error fetching wishlist:', err)
    } finally {
      loading.value = false
    }
  }

  // Add product to wishlist
  const addToWishlist = async (productId: number) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/wishlist/add/', { product_id: productId })
      // Refresh wishlist
      await fetchWishlist()
      return { success: true, data }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to add to wishlist'
      console.error('Error adding to wishlist:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Remove product from wishlist
  const removeFromWishlist = async (productId: number) => {
    loading.value = true
    error.value = null
    try {
      await api.delete(`/api/wishlist/remove/${productId}/`)
      // Remove from local state
      items.value = items.value.filter((item) => item.product.id !== productId)
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to remove from wishlist'
      console.error('Error removing from wishlist:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Toggle product in wishlist (add if not exists, remove if exists)
  const toggleWishlist = async (productId: number) => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.post('/api/wishlist/toggle/', { product_id: productId })
      // Refresh wishlist
      await fetchWishlist()
      return { success: true, inWishlist: data.in_wishlist, message: data.message }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to toggle wishlist'
      console.error('Error toggling wishlist:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Check if product is in wishlist (API call)
  const checkWishlist = async (productId: number): Promise<boolean> => {
    try {
      const { data } = await api.get(`/api/wishlist/check/${productId}/`)
      return data.in_wishlist
    } catch (err) {
      console.error('Error checking wishlist:', err)
      return false
    }
  }

  // Clear entire wishlist
  const clearWishlist = async () => {
    loading.value = true
    error.value = null
    try {
      await api.delete('/api/wishlist/clear/')
      items.value = []
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Failed to clear wishlist'
      console.error('Error clearing wishlist:', err)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  // Reset store
  const reset = () => {
    items.value = []
    loading.value = false
    error.value = null
  }

  return {
    // State
    items,
    loading,
    error,
    // Computed
    count,
    isEmpty,
    productIds,
    // Actions
    isInWishlist,
    fetchWishlist,
    addToWishlist,
    removeFromWishlist,
    toggleWishlist,
    checkWishlist,
    clearWishlist,
    reset,
  }
})
