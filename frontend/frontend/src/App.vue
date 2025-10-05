<template>
  <Navbar />
  <router-view />
  <CartDrawer />
  
</template>

<script setup lang="ts">
import Navbar from './components/layout/Navbar.vue'
import CartDrawer from './components/cart/CartDrawer.vue'
</script>


