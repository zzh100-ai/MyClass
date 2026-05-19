<script setup>
import { ref, onMounted } from 'vue'
import { useCouponStore } from '@/stores/coupon'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const couponStore = useCouponStore()
const page = ref(1)

onMounted(() => {
  couponStore.fetchPoints()
  couponStore.fetchHistory()
})

function loadMore() {
  page.value++
  couponStore.fetchHistory(page.value)
}

const typeMap = {
  register: '注册赠送', purchase: '购买获赠',
  redeem: '积分抵扣', refund: '退款退回', expire: '积分过期',
}
</script>

<template>
  <div class="points-page">
    <NavBar />
    <main class="main-content">
      <!-- 积分余额 -->
      <div class="points-balance">
        <div class="balance-num">{{ couponStore.points }}</div>
        <div class="balance-label">当前积分</div>
      </div>

      <!-- 流水 -->
      <h2 class="section-title">积分明细</h2>
      <div v-if="couponStore.pointsHistory.length === 0" class="state-msg">暂无记录</div>
      <div v-else class="history-list">
        <div v-for="item in couponStore.pointsHistory" :key="item.id" class="history-item">
          <div class="history-info">
            <span class="history-type">{{ typeMap[item.type] || item.type }}</span>
            <span class="history-desc">{{ item.description }}</span>
          </div>
          <div class="history-time">{{ item.created_at?.slice(0, 16) }}</div>
          <div :class="['history-amount', item.amount > 0 ? 'positive' : 'negative']">
            {{ item.amount > 0 ? '+' : '' }}{{ item.amount }}
          </div>
        </div>
      </div>
    </main>
    <PageFooter />
  </div>
</template>

<style scoped>
.points-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e, #1e2a4a, #1c2541, #1a1a3e);
  color: rgba(255,255,255,0.94);
}
.main-content { max-width: 600px; margin: 0 auto; padding: 40px 48px 80px; }
.state-msg { text-align: center; padding: 60px 0; color: rgba(255,255,255,0.4); }

.points-balance {
  text-align: center; padding: 48px 0;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.08);
  border-radius: 8px; margin-bottom: 36px;
}
.balance-num {
  font-size: 3.5rem; font-weight: 700; color: #e94560; line-height: 1;
}
.balance-label { font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-top: 8px; }
.section-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 16px; }

.history-list { display: flex; flex-direction: column; gap: 8px; }
.history-item {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 16px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 4px;
}
.history-info { flex: 1; min-width: 0; }
.history-type { font-size: 0.9rem; font-weight: 500; display: block; }
.history-desc { font-size: 0.78rem; color: rgba(255,255,255,0.45); }
.history-time { font-size: 0.75rem; color: rgba(255,255,255,0.35); flex-shrink: 0; }
.history-amount {
  font-size: 1rem; font-weight: 700; flex-shrink: 0;
}
.history-amount.positive { color: #27ae60; }
.history-amount.negative { color: #e94560; }
</style>
