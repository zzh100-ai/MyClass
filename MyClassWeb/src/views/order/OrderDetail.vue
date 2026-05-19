<script setup>
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useOrderStore } from '@/stores/order'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const route = useRoute()
const router = useRouter()
const orderStore = useOrderStore()

const order = computed(() => orderStore.currentOrder)

onMounted(() => {
  const id = route.params.id
  if (id) orderStore.fetchOrder(id)
})

async function handlePay() {
  try {
    await orderStore.payOrder(order.value.id)
    alert('支付成功！')
  } catch (e) {
    alert(e.message || '支付失败')
  }
}

const statusMap = { pending: '待支付', paid: '已支付', cancelled: '已取消', refunded: '已退款' }
</script>

<template>
  <div class="order-detail-page">
    <NavBar />

    <main class="main-content">
      <button class="back-btn" @click="router.push('/orders')">← 返回订单列表</button>

      <div v-if="!order" class="state-msg">加载中...</div>

      <template v-else>
        <!-- 状态 -->
        <div class="status-bar">
          <span :class="['status-badge', order.status]">
            {{ statusMap[order.status] }}
          </span>
          <span class="order-no">订单号：{{ order.order_no }}</span>
        </div>

        <!-- 课程清单 -->
        <div class="order-items">
          <h3>课程清单</h3>
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <span class="item-title">{{ item.course_title }}</span>
            <span class="item-price">¥{{ item.price }}</span>
          </div>
        </div>

        <!-- 金额 -->
        <div class="order-total">
          <span class="total-label">订单金额</span>
          <span class="total-price">¥{{ order.total_amount }}</span>
        </div>

        <!-- 时间 -->
        <div class="order-time">
          <p>创建时间：{{ order.created_at?.slice(0, 19) }}</p>
          <p v-if="order.paid_at">支付时间：{{ order.paid_at?.slice(0, 19) }}</p>
        </div>

        <!-- 操作 -->
        <div class="order-actions">
          <button
            v-if="order.status === 'pending'"
            class="pay-btn"
            :disabled="orderStore.paying"
            @click="handlePay"
          >{{ orderStore.paying ? '支付中...' : '立即支付' }}</button>
        </div>
      </template>
    </main>

    <PageFooter />
  </div>
</template>

<style scoped>
.order-detail-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e 0%, #1e2a4a 30%, #1c2541 60%, #1a1a3e 100%);
  color: rgba(255, 255, 255, 0.94);
}

.main-content {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}

.back-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.5);
  cursor: pointer;
  font-size: 0.85rem;
  margin-bottom: 24px;
  padding: 0;
}

.back-btn:hover { color: #e94560; }

.state-msg { text-align: center; padding: 80px 0; color: rgba(255, 255, 255, 0.4); }

.status-bar {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 28px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
}

.status-badge {
  padding: 4px 14px;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-badge.pending { background: rgba(243, 156, 18, 0.2); color: #f39c12; }
.status-badge.paid { background: rgba(39, 174, 96, 0.2); color: #27ae60; }
.status-badge.cancelled { background: rgba(255, 255, 255, 0.1); color: rgba(255, 255, 255, 0.4); }

.order-no { font-size: 0.85rem; color: rgba(255, 255, 255, 0.4); }

.order-items {
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  padding: 20px;
  margin-bottom: 16px;
}

.order-items h3 { font-size: 1rem; margin-bottom: 16px; }

.order-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.9rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.order-item:last-child { border-bottom: none; }

.item-price { color: #e94560; font-weight: 600; }

.order-total {
  display: flex;
  justify-content: space-between;
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 6px;
  margin-bottom: 16px;
}

.total-price { font-size: 1.2rem; font-weight: 700; color: #e94560; }

.order-time {
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.4);
  line-height: 1.8;
  margin-bottom: 28px;
}

.order-actions { text-align: center; }

.pay-btn {
  background: #e94560;
  border: none;
  color: #fff;
  padding: 14px 60px;
  border-radius: 4px;
  font-size: 1.1rem;
  cursor: pointer;
  letter-spacing: 2px;
  transition: background 0.2s;
}

.pay-btn:hover:not(:disabled) { background: #d63850; }
.pay-btn:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
