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
    {
      path: '/courses',
      name: 'CourseList',
      component: () => import('@/views/courses/CourseList.vue'),
    },
    {
      path: '/courses/:id',
      name: 'CourseDetail',
      component: () => import('@/views/courses/CourseDetail.vue'),
    },
    {
      path: '/cart',
      name: 'Cart',
      component: () => import('@/views/cart/CartPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/checkout',
      name: 'Checkout',
      component: () => import('@/views/order/CheckoutPage.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/orders',
      name: 'OrderList',
      component: () => import('@/views/order/OrderList.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/orders/:id',
      name: 'OrderDetail',
      component: () => import('@/views/order/OrderDetail.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/coupons',
      name: 'CouponList',
      component: () => import('@/views/coupon/CouponList.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/points',
      name: 'Points',
      component: () => import('@/views/points/PointsPage.vue'),
      meta: { requiresAuth: true },
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
