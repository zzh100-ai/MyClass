<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <span class="nav-brand">MyClass</span>
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

.nav-brand {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 4px;
  color: #e94560;
  font-family: 'Georgia', serif;
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
