<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

onMounted(() => {
  if (authStore.isAuthenticated) {
    cartStore.fetchCount()
  }
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <div class="nav-left">
      <span class="nav-brand" @click="router.push('/')">MyClass</span>
      <div class="nav-links">
        <router-link to="/courses" class="nav-link">全部课程</router-link>
        <router-link to="/cart" class="nav-link cart-link">
          购物车
          <span v-if="cartStore.count" class="cart-badge">{{ cartStore.count }}</span>
        </router-link>
      </div>
    </div>
    <div class="nav-right">
      <span class="nav-user">{{ authStore.user?.username }}</span>
      <button class="nav-logout" @click="handleLogout">退出</button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 24px 48px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.nav-left {
  display: flex;
  align-items: center;
  gap: 32px;
}

.nav-brand {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 4px;
  color: #e94560;
  font-family: 'Georgia', serif;
  cursor: pointer;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
}

.nav-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  font-size: 0.9rem;
  letter-spacing: 1px;
  transition: color 0.2s;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  position: relative;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: #e94560;
}

.cart-link {
  display: flex;
  align-items: center;
  gap: 4px;
}

.cart-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  border-radius: 9px;
  background: #e94560;
  color: #fff;
  font-size: 0.7rem;
  font-weight: 600;
  line-height: 1;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-user {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.72);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}

.nav-logout {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: rgba(255, 255, 255, 0.72);
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.2s;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  letter-spacing: 1px;
}

.nav-logout:hover {
  color: #e94560;
  border-color: #e94560;
}
</style>
