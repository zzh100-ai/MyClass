import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/views/HomeView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/views/LoginView.vue'),
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/views/RegisterView.vue'),
    },
  ],
})

// 路由守卫
router.beforeEach((to) => {
  const token = localStorage.getItem('access_token')
  // 未登录 → 访问需认证页面 → 重定向到登录页
  if (to.meta.requiresAuth && !token) {
    return '/login'
  }
  // 已登录 → 访问登录/注册页 → 重定向到首页
  if (token && (to.path === '/login' || to.path === '/register')) {
    return '/'
  }
})

export default router
