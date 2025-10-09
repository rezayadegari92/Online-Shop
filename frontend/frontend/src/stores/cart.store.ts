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
        
        // Handle authenticated users (data has items array)
        if (data.items && Array.isArray(data.items)) {
          this.items = data.items.map((it: any) => ({
            product_id: it.product.id,
            quantity: it.quantity,
            name: it.product.name,
            price: it.product.discounted_price ?? it.product.price,
            image: it.product.image_url,
          }))
        } 
        // Handle anonymous users (data is a dictionary of product_id: quantity)
        else if (typeof data === 'object' && !Array.isArray(data) && !data.items) {
          // For anonymous users, we need to fetch product details
          const productIds = Object.keys(data).filter(key => key !== 'discount_code')
          if (productIds.length > 0) {
            const productPromises = productIds.map(async (pid) => {
              try {
                const { data: product } = await api.get(`/api/products/${pid}/`)
                return {
                  product_id: parseInt(pid),
                  quantity: data[pid],
                  name: product.name,
                  price: product.discounted_price ?? product.price,
                  image: product.images?.[0]?.image_url
                }
              } catch (e) {
                console.error(`Failed to fetch product ${pid}:`, e)
                return null
              }
            })
            const products = await Promise.all(productPromises)
            this.items = products.filter(p => p !== null) as CartItem[]
          } else {
            this.items = []
          }
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
        const response = await api.post('/api/cart/', { product_id, quantity })
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
