import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/store/user'
import { isMobile } from '@/utils/device'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    redirect: '/customers'
  },
  {
    path: '/customers',
    name: 'Customers',
    component: () => isMobile() 
      ? import('@/views/mobile/CustomerList.vue')
      : import('@/views/pc/CustomerList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/customers/create',
    name: 'CustomerCreate',
    component: () => isMobile()
      ? import('@/views/mobile/CustomerForm.vue')
      : import('@/views/pc/CustomerForm.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/customers/:id',
    name: 'CustomerDetail',
    component: () => isMobile()
      ? import('@/views/mobile/CustomerDetail.vue')
      : import('@/views/pc/CustomerDetail.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/customers/:id/edit',
    name: 'CustomerEdit',
    component: () => isMobile()
      ? import('@/views/mobile/CustomerForm.vue')
      : import('@/views/pc/CustomerForm.vue'),
    meta: { requiresAuth: true }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  
  if (to.meta.requiresAuth && !userStore.isLoggedIn) {
    next('/login')
  } else if (to.path === '/login' && userStore.isLoggedIn) {
    next('/customers')
  } else {
    next()
  }
})

export default router

