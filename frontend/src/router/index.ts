import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth.store'

const routes = [
  { path: '/', redirect: '/products' },
  { path: '/products', component: () => import('../views/ProductsView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/signup', component: () => import('../views/SignupView.vue') },
  { path: '/verify-otp', component: () => import('../views/VerifyOtpView.vue') },
  { path: '/profile', component: () => import('../views/ProfileView.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (!auth.isBootstrapped) await auth.bootstrap()
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
})

export default router


