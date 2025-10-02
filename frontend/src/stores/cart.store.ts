import { defineStore } from 'pinia'
import api from '../utils/http'

interface CartItem { 
  product_id: number
  quantity: number
  name?: string
  price?: number
  image?: string
}

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as CartItem[],
    isOpen: false,
  }),
  actions: {
    toggle(open?: boolean) { this.isOpen = open ?? !this.isOpen },
    async load() {
      try {
        const { data } = await api.get('/api/cart/')
        // Normalize cart items from backend
        if (data.items && Array.isArray(data.items)) {
          this.items = data.items.map((it: any) => ({
            product_id: it.product.id,
            quantity: it.quantity,
            name: it.product.name,
            price: it.product.discounted_price ?? it.product.price,
            image: it.product.image_url,
          }))
        } else {
          this.items = []
        }
      } catch (e) {
        console.error('Failed to load cart:', e)
        this.items = []
      }
    },
    async add(product_id: number, quantity = 1) {
      try {
        await api.post('/api/cart/', { product_id, quantity })
        await this.load()
        this.isOpen = true
      } catch (e) {
        throw e
      }
    },
    async update(product_id: number, quantity: number) {
      try {
        if (quantity === 0) {
          await this.remove(product_id)
        } else {
          await api.put('/api/cart/', { product_id, quantity })
          await this.load()
        }
      } catch (e) {
        throw e
      }
    },
    async remove(product_id: number) {
      try {
        await api.delete('/api/cart/', { data: { product_id } })
        await this.load()
      } catch (e) {
        throw e
      }
    },
    async checkout() {
      const { data } = await api.post('/api/cart/checkout/')
      await this.load()
      return data
    },
  }
})
