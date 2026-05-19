<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const router = useRouter()
const cartStore = useCartStore()
const showConfirm = ref(false)

onMounted(() => {
  cartStore.fetchCart()
})

const totalPrice = computed(() => {
  return cartStore.items
    .filter(c => !c.is_free)
    .reduce((sum, c) => sum + parseFloat(c.price || 0), 0)
    .toFixed(2)
})

async function handleRemove(courseId) {
  try {
    await cartStore.removeCourse(courseId)
    ElMessage.success('已移除')
  } catch (e) {
    ElMessage.error(e.message || '移除失败')
  }
}

function handleClear() {
  showConfirm.value = true
}

async function confirmClear() {
  await cartStore.clearAll()
  showConfirm.value = false
}

function goCheckout() {
  router.push('/checkout')
}
</script>

<template>
  <div class="cart-page">
    <NavBar />

    <main class="main-content">
      <div class="page-header">
        <h1 class="page-title">购物车</h1>
        <p class="page-desc" v-if="cartStore.items.length">
          共 {{ cartStore.items.length }} 门课程
        </p>
        <button
          v-if="cartStore.items.length"
          class="clear-btn"
          @click="handleClear"
        >清空购物车</button>
      </div>

      <!-- 加载中 -->
      <div v-if="cartStore.loading" class="state-msg">加载中...</div>

      <!-- 空购物车 -->
      <div v-else-if="cartStore.items.length === 0" class="empty-cart">
        <div class="empty-icon">🛒</div>
        <p class="empty-text">购物车还是空的</p>
        <button class="go-shop" @click="router.push('/courses')">去选课</button>
      </div>

      <!-- 购物车列表 -->
      <div v-else class="cart-list">
        <div v-for="course in cartStore.items" :key="course.id" class="cart-item">
          <div class="item-image" @click="router.push(`/courses/${course.id}`)">
            <img
              v-if="course.cover_image"
              :src="course.cover_image"
              :alt="course.title"
            />
            <div v-else class="item-placeholder">{{ course.title?.[0] }}</div>
          </div>

          <div class="item-info" @click="router.push(`/courses/${course.id}`)">
            <h3 class="item-title">{{ course.title }}</h3>
            <p class="item-teacher">{{ course.teacher_name }}</p>
          </div>

          <div class="item-action">
            <span v-if="course.is_free" class="item-price free">免费</span>
            <span v-else class="item-price">¥{{ course.price }}</span>
            <button class="remove-btn" @click="handleRemove(course.id)">移除</button>
          </div>
        </div>

        <!-- 底部结算 -->
        <div class="cart-footer">
          <div class="footer-total">
            <span class="total-label">合计：</span>
            <span class="total-price">¥{{ totalPrice }}</span>
          </div>
          <button class="checkout-btn" @click="goCheckout">去结算</button>
        </div>
      </div>
    </main>

    <!-- 确认清空弹窗 -->
    <div v-if="showConfirm" class="modal-overlay" @click.self="showConfirm = false">
      <div class="modal-box">
        <p>确认清空购物车？</p>
        <div class="modal-actions">
          <button class="modal-cancel" @click="showConfirm = false">取消</button>
          <button class="modal-confirm" @click="confirmClear">确认</button>
        </div>
      </div>
    </div>

    <PageFooter />
  </div>
</template>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e 0%, #1e2a4a 30%, #1c2541 60%, #1a1a3e 100%);
  color: rgba(255, 255, 255, 0.94);
}

.main-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}

.page-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 36px;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 600;
}

.page-desc {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.5);
  flex: 1;
}

.clear-btn {
  background: transparent;
  border: 1px solid rgba(255, 255, 255, 0.15);
  color: rgba(255, 255, 255, 0.5);
  padding: 6px 16px;
  font-size: 0.8rem;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.clear-btn:hover {
  border-color: #e94560;
  color: #e94560;
}

/* 空状态 */
.empty-cart {
  text-align: center;
  padding: 80px 0;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 16px;
}

.empty-text {
  color: rgba(255, 255, 255, 0.5);
  margin-bottom: 24px;
}

.go-shop {
  background: transparent;
  border: 1px solid #e94560;
  color: #e94560;
  padding: 10px 32px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.go-shop:hover {
  background: #e94560;
  color: #fff;
}

/* 列表 */
.cart-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.cart-item {
  display: flex;
  align-items: center;
  gap: 16px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 16px;
  transition: border-color 0.2s;
}

.cart-item:hover {
  border-color: rgba(255, 255, 255, 0.15);
}

.item-image {
  width: 120px;
  height: 68px;
  border-radius: 4px;
  overflow: hidden;
  flex-shrink: 0;
  cursor: pointer;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.15);
  background: rgba(255, 255, 255, 0.04);
}

.item-info {
  flex: 1;
  min-width: 0;
  cursor: pointer;
}

.item-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-teacher {
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.45);
}

.item-action {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 8px;
  flex-shrink: 0;
}

.item-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #e94560;
}

.item-price.free { color: #27ae60; }

.remove-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.35);
  font-size: 0.78rem;
  cursor: pointer;
  padding: 2px 8px;
  transition: color 0.2s;
}

.remove-btn:hover {
  color: #e94560;
}

/* 底部结算 */
.cart-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 24px;
  padding-top: 20px;
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  margin-top: 8px;
}

.footer-total {
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.total-label {
  font-size: 0.9rem;
  color: rgba(255, 255, 255, 0.6);
}

.total-price {
  font-size: 1.4rem;
  font-weight: 700;
  color: #e94560;
}

.checkout-btn {
  background: #e94560;
  border: none;
  color: #fff;
  padding: 12px 36px;
  border-radius: 4px;
  font-size: 0.95rem;
  cursor: pointer;
  letter-spacing: 1px;
  transition: background 0.2s;
}

.checkout-btn:hover {
  background: #d63850;
}

/* 弹窗 */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
}

.modal-box {
  background: #1e2a4a;
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  padding: 32px;
  text-align: center;
}

.modal-box p {
  margin-bottom: 24px;
  font-size: 1rem;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.modal-cancel,
.modal-confirm {
  padding: 8px 24px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s;
}

.modal-cancel {
  background: transparent;
  color: rgba(255, 255, 255, 0.7);
}

.modal-confirm {
  background: #e94560;
  border-color: #e94560;
  color: #fff;
}

.modal-cancel:hover {
  border-color: rgba(255, 255, 255, 0.4);
}

.modal-confirm:hover {
  background: #d63850;
}
</style>
