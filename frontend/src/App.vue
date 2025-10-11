<template>
  <Navbar />
  <router-view />
  <CartDrawer />
  
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import Navbar from './components/layout/Navbar.vue'
import CartDrawer from './components/cart/CartDrawer.vue'
import { useThemeStore } from './stores/theme.store'

const theme = useThemeStore()

// Initialize theme on app load
onMounted(() => {
  theme.initTheme()
})
</script>


