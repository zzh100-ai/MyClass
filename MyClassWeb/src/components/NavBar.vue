<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

const showMenu = ref(false)
const menuRef = ref(null)

onMounted(() => {
  if (authStore.isAuthenticated) {
    cartStore.fetchCount()
  }
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

function handleClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    showMenu.value = false
  }
}

function toggleMenu() {
  showMenu.value = !showMenu.value
}

function goTo(path) {
  showMenu.value = false
  if (path === 'logout') {
    authStore.logout()
    router.push('/login')
  } else {
    router.push(path)
  }
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
    <div class="nav-right" ref="menuRef">
      <span class="nav-user-dropdown" @click="toggleMenu">
        {{ authStore.user?.username || '用户' }}
      </span>
      <transition name="fade">
        <div v-if="showMenu" class="dropdown-menu">
          <div class="dropdown-item" @click="goTo('/orders')">我的订单</div>
          <div class="dropdown-item" @click="goTo('/coupons')">优惠券</div>
          <div class="dropdown-item" @click="goTo('/points')">积分</div>
          <div class="dropdown-divider"></div>
          <div class="dropdown-item logout" @click="goTo('logout')">退出登录</div>
        </div>
      </transition>
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
  position: relative;
  display: flex;
  align-items: center;
}

.nav-user-dropdown {
  color: rgba(255, 255, 255, 0.72);
  font-size: 0.9rem;
  cursor: pointer;
  padding: 6px 12px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  transition: all 0.2s;
  letter-spacing: 1px;
  user-select: none;
}

.nav-user-dropdown:hover {
  color: #e94560;
  border-color: #e94560;
}

.dropdown-menu {
  position: absolute;
  top: calc(100% + 8px);
  right: 0;
  min-width: 140px;
  background: #1e2a4a;
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 6px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  overflow: hidden;
}

.dropdown-item {
  padding: 10px 16px;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.75);
  cursor: pointer;
  transition: all 0.15s;
  letter-spacing: 1px;
}

.dropdown-item:hover {
  background: rgba(233, 69, 96, 0.12);
  color: #e94560;
}

.dropdown-item.logout {
  color: rgba(255, 255, 255, 0.45);
}

.dropdown-item.logout:hover {
  color: #e94560;
}

.dropdown-divider {
  height: 1px;
  background: rgba(255, 255, 255, 0.08);
  margin: 4px 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease, transform 0.15s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
