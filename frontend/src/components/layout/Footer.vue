<template>
  <footer class="relative bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 text-white overflow-hidden">
    <!-- Decorative Background Elements -->
    <div class="absolute inset-0 opacity-10">
      <div class="absolute top-0 left-0 w-96 h-96 bg-blue-500 rounded-full blur-3xl"></div>
      <div class="absolute bottom-0 right-0 w-96 h-96 bg-purple-500 rounded-full blur-3xl"></div>
    </div>

    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-16">
      <!-- Main Footer Content -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 lg:gap-12 mb-12">
        <!-- Company Info -->
        <div class="space-y-4">
          <div class="flex items-center space-x-2 mb-4">
            <div class="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 11V7a4 4 0 00-8 0v4M5 9h14l1 12H4L5 9z" />
              </svg>
            </div>
            <h3 class="text-2xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
              OnlineShop
            </h3>
          </div>
          <p class="text-gray-300 text-sm leading-relaxed">
            Your one-stop destination for quality products. We offer the best deals and fastest delivery to make your shopping experience exceptional.
          </p>
          <!-- Social Media Links -->
          <div class="flex items-center space-x-4 pt-4">
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-gradient-to-r hover:from-blue-500 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 transform hover:scale-110"
              aria-label="Facebook"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
              </svg>
            </a>
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-gradient-to-r hover:from-blue-500 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 transform hover:scale-110"
              aria-label="Twitter"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M23.953 4.57a10 10 0 01-2.825.775 4.958 4.958 0 002.163-2.723c-.951.555-2.005.959-3.127 1.184a4.92 4.92 0 00-8.384 4.482C7.69 8.095 4.067 6.13 1.64 3.162a4.822 4.822 0 00-.666 2.475c0 1.71.87 3.213 2.188 4.096a4.904 4.904 0 01-2.228-.616v.06a4.923 4.923 0 003.946 4.827 4.996 4.996 0 01-2.212.085 4.936 4.936 0 004.604 3.417 9.867 9.867 0 01-6.102 2.105c-.39 0-.779-.023-1.17-.067a13.995 13.995 0 007.557 2.209c9.053 0 13.998-7.496 13.998-13.985 0-.21 0-.42-.015-.63A9.935 9.935 0 0024 4.59z"/>
              </svg>
            </a>
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-gradient-to-r hover:from-blue-500 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 transform hover:scale-110"
              aria-label="Instagram"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/>
              </svg>
            </a>
            <a 
              href="#" 
              class="w-10 h-10 bg-white/10 hover:bg-gradient-to-r hover:from-blue-500 hover:to-purple-600 rounded-lg flex items-center justify-center transition-all duration-300 transform hover:scale-110"
              aria-label="LinkedIn"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>
              </svg>
            </a>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-lg font-bold mb-4 text-white">Quick Links</h4>
          <ul class="space-y-3">
            <li>
              <router-link to="/" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Home
              </router-link>
            </li>
            <li>
              <router-link to="/products" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Products
              </router-link>
            </li>
            <li>
              <router-link to="/products?discounted=true" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Hot Deals
              </router-link>
            </li>
            <li>
              <router-link v-if="auth.isAuthenticated" to="/wishlist" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Wishlist
              </router-link>
            </li>
            <li>
              <router-link v-if="auth.isAuthenticated" to="/orders" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                My Orders
              </router-link>
            </li>
          </ul>
        </div>

        <!-- Customer Service -->
        <div>
          <h4 class="text-lg font-bold mb-4 text-white">Customer Service</h4>
          <ul class="space-y-3">
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Contact Us
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                FAQ
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Shipping Info
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Returns & Refunds
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Privacy Policy
              </a>
            </li>
            <li>
              <a href="#" class="text-gray-300 hover:text-white transition-colors duration-300 flex items-center group">
                <span class="w-0 group-hover:w-2 h-0.5 bg-gradient-to-r from-blue-400 to-purple-400 transition-all duration-300 mr-0 group-hover:mr-2"></span>
                Terms of Service
              </a>
            </li>
          </ul>
        </div>

        <!-- Newsletter -->
        <div>
          <h4 class="text-lg font-bold mb-4 text-white">Newsletter</h4>
          <p class="text-gray-300 text-sm mb-4">
            Subscribe to get special offers, free giveaways, and exclusive deals delivered to your inbox.
          </p>
          <form @submit.prevent="subscribeNewsletter" class="space-y-3">
            <div class="relative">
              <input
                v-model="newsletterEmail"
                type="email"
                placeholder="Enter your email"
                required
                class="w-full px-4 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300"
              />
            </div>
            <button
              type="submit"
              class="w-full bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white font-semibold py-3 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
            >
              Subscribe
            </button>
          </form>
          <p v-if="newsletterMessage" :class="newsletterMessage.includes('success') ? 'text-green-400' : 'text-red-400'" class="text-sm mt-2">
            {{ newsletterMessage }}
          </p>
        </div>
      </div>

      <!-- Payment Methods & Bottom Bar -->
      <div class="border-t border-white/10 pt-8">
        <!-- Payment Methods -->
        <div class="mb-6">
          <h5 class="text-sm font-semibold text-gray-400 mb-4 text-center">We Accept</h5>
          <div class="flex flex-wrap items-center justify-center gap-4">
            <div class="w-16 h-10 bg-white/10 rounded-lg flex items-center justify-center backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
              <span class="text-xs font-bold text-white">VISA</span>
            </div>
            <div class="w-16 h-10 bg-white/10 rounded-lg flex items-center justify-center backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
              <span class="text-xs font-bold text-white">MC</span>
            </div>
            <div class="w-16 h-10 bg-white/10 rounded-lg flex items-center justify-center backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
              <span class="text-xs font-bold text-white">AMEX</span>
            </div>
            <div class="w-16 h-10 bg-white/10 rounded-lg flex items-center justify-center backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
              <span class="text-xs font-bold text-white">PayPal</span>
            </div>
            <div class="w-16 h-10 bg-white/10 rounded-lg flex items-center justify-center backdrop-blur-sm hover:bg-white/20 transition-all duration-300">
              <span class="text-xs font-bold text-white">Apple</span>
            </div>
          </div>
        </div>

        <!-- Copyright -->
        <div class="flex flex-col md:flex-row items-center justify-between text-sm text-gray-400 space-y-2 md:space-y-0">
          <p>
            © {{ currentYear }} OnlineShop. All rights reserved.
          </p>
          <div class="flex items-center space-x-6">
            <a href="#" class="hover:text-white transition-colors duration-300">Privacy</a>
            <a href="#" class="hover:text-white transition-colors duration-300">Terms</a>
            <a href="#" class="hover:text-white transition-colors duration-300">Sitemap</a>
          </div>
        </div>
      </div>
    </div>

    <!-- Back to Top Button -->
    <button
      v-if="showBackToTop"
      @click="scrollToTop"
      class="fixed bottom-8 right-8 w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 transform hover:scale-110 z-50"
      aria-label="Back to top"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 10l7-7m0 0l7 7m-7-7v18" />
      </svg>
    </button>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useAuthStore } from '../../stores/auth.store'
import { showToast } from '../../utils/toast'

const auth = useAuthStore()
const newsletterEmail = ref('')
const newsletterMessage = ref('')
const showBackToTop = ref(false)

const currentYear = computed(() => new Date().getFullYear())

function subscribeNewsletter() {
  if (!newsletterEmail.value) return
  
  // Simulate newsletter subscription
  newsletterMessage.value = 'Successfully subscribed! Check your email for confirmation.'
  showToast.success('Successfully subscribed to newsletter!')
  newsletterEmail.value = ''
  
  setTimeout(() => {
    newsletterMessage.value = ''
  }, 5000)
}

function handleScroll() {
  showBackToTop.value = window.scrollY > 300
}

function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
/* Additional animations can be added here if needed */
</style>




