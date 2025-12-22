<template>
  <Navbar />
  <router-view />
  <CartDrawer />
  <Footer />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Navbar from './components/layout/Navbar.vue'
import CartDrawer from './components/cart/CartDrawer.vue'
import Footer from './components/layout/Footer.vue'
import { useThemeStore } from './stores/theme.store'

const theme = useThemeStore()

// Initialize theme on app load
onMounted(() => {
  theme.initTheme()
})
</script>


