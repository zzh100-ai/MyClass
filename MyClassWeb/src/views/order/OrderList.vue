<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useOrderStore } from '@/stores/order'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const router = useRouter()
const orderStore = useOrderStore()

onMounted(() => {
  orderStore.fetchOrders()
})

const statusMap = { pending: '待支付', paid: '已支付', cancelled: '已取消', refunded: '已退款' }
</script>

<template>
  <div class="order-list-page">
    <NavBar />

    <main class="main-content">
      <h1 class="page-title">我的订单</h1>

      <div v-if="orderStore.loading" class="state-msg">加载中...</div>

      <div v-else-if="orderStore.orders.length === 0" class="state-msg">
        <p>暂无订单</p>
        <button class="link-btn" @click="router.push('/courses')">去选课</button>
      </div>

      <div v-else class="order-list">
        <div
          v-for="order in orderStore.orders"
          :key="order.id"
          class="order-card"
          @click="router.push(`/orders/${order.id}`)"
        >
          <div class="order-header">
            <span class="order-no">订单号：{{ order.order_no }}</span>
            <span :class="['order-status', order.status]">{{ statusMap[order.status] }}</span>
          </div>
          <div class="order-body">
            <div v-for="item in order.items.slice(0, 3)" :key="item.id" class="order-course">
              {{ item.course_title }} × ¥{{ item.price }}
            </div>
            <div v-if="order.items.length > 3" class="order-more">
              等 {{ order.items.length }} 门课程
            </div>
          </div>
          <div class="order-footer">
            <span class="order-total">合计：¥{{ order.total_amount }}</span>
            <span class="order-time">{{ order.created_at?.slice(0, 16) }}</span>
          </div>
        </div>
      </div>
    </main>

    <PageFooter />
  </div>
</template>

<style scoped>
.order-list-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e 0%, #1e2a4a 30%, #1c2541 60%, #1a1a3e 100%);
  color: rgba(255, 255, 255, 0.94);
}

.main-content {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 48px 80px;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 28px;
}

.state-msg {
  text-align: center;
  padding: 80px 0;
  color: rgba(255, 255, 255, 0.4);
}

.link-btn {
  margin-top: 16px;
  background: transparent;
  border: 1px solid #e94560;
  color: #e94560;
  padding: 8px 24px;
  border-radius: 4px;
  cursor: pointer;
}

.order-card {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 6px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.order-card:hover { border-color: rgba(233, 69, 96, 0.3); }

.order-header {
  display: flex;
  justify-content: space-between;
  padding: 12px 16px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.85rem;
}

.order-no { color: rgba(255, 255, 255, 0.5); }

.order-status { font-weight: 600; }
.order-status.pending { color: #f39c12; }
.order-status.paid { color: #27ae60; }
.order-status.cancelled { color: rgba(255, 255, 255, 0.4); }

.order-body {
  padding: 12px 16px;
  font-size: 0.9rem;
  line-height: 1.8;
  color: rgba(255, 255, 255, 0.7);
}

.order-more { color: rgba(255, 255, 255, 0.4); font-size: 0.85rem; }

.order-footer {
  display: flex;
  justify-content: space-between;
  padding: 10px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  font-size: 0.85rem;
}

.order-total { color: #e94560; font-weight: 600; }
.order-time { color: rgba(255, 255, 255, 0.4); }
</style>
