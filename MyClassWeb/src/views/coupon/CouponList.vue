<script setup>
import { ref, onMounted } from 'vue'
import { useCouponStore } from '@/stores/coupon'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const couponStore = useCouponStore()
const code = ref('')
const collecting = ref(false)
const msg = ref('')

onMounted(() => { couponStore.fetchCoupons() })

async function handleCollect() {
  if (!code.value.trim()) return
  collecting.value = true
  msg.value = ''
  try {
    await couponStore.collectCoupon(code.value.trim())
    msg.value = '领取成功'
    code.value = ''
  } catch (e) {
    msg.value = e.message
  } finally {
    collecting.value = false
  }
}

function isExpired(c) {
  return new Date(c.coupon.valid_to) < new Date()
}

function isUsable(c) {
  return c.status === 'unused' && !isExpired(c)
}
</script>

<template>
  <div class="coupon-page">
    <NavBar />
    <main class="main-content">
      <h1 class="page-title">我的优惠券</h1>

      <!-- 领取区 -->
      <div class="collect-box">
        <input v-model="code" placeholder="输入优惠券编码" class="code-input"
          @keyup.enter="handleCollect" />
        <button class="collect-btn" :disabled="collecting" @click="handleCollect">
          {{ collecting ? '领取中...' : '领取' }}
        </button>
      </div>
      <p v-if="msg" class="collect-msg">{{ msg }}</p>

      <!-- 列表 -->
      <div v-if="couponStore.coupons.length === 0" class="state-msg">暂无优惠券</div>
      <div v-else class="coupon-list">
        <div v-for="uc in couponStore.coupons" :key="uc.id" :class="['coupon-card', uc.status]">
          <div class="coupon-left">
            <div class="coupon-value">
              <span class="value-symbol">{{ uc.coupon.discount_type === 'percent' ? '' : '¥' }}</span>
              <span class="value-num">{{ uc.coupon.discount_value }}</span>
              <span v-if="uc.coupon.discount_type === 'percent'" class="value-unit">折</span>
            </div>
            <div class="coupon-condition">
              满 ¥{{ uc.coupon.min_amount }}可用
            </div>
          </div>
          <div class="coupon-body">
            <div class="coupon-name">{{ uc.coupon.name }}</div>
            <div class="coupon-desc">{{ uc.coupon.description || uc.coupon.code }}</div>
            <div class="coupon-date">{{ uc.coupon.valid_to?.slice(0, 10) }} 到期</div>
          </div>
          <div class="coupon-status">
            <span v-if="uc.status === 'used'" class="tag used">已使用</span>
            <span v-else-if="isExpired(uc)" class="tag expired">已过期</span>
            <span v-else class="tag unused">未使用</span>
          </div>
        </div>
      </div>
    </main>
    <PageFooter />
  </div>
</template>

<style scoped>
.coupon-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e, #1e2a4a, #1c2541, #1a1a3e);
  color: rgba(255, 255, 255, 0.94);
}
.main-content {
  max-width: 700px; margin: 0 auto; padding: 40px 48px 80px;
}
.page-title { font-size: 1.5rem; font-weight: 600; margin-bottom: 28px; }
.state-msg { text-align: center; padding: 80px 0; color: rgba(255,255,255,0.4); }

/* 领取区 */
.collect-box {
  display: flex; gap: 12px; margin-bottom: 8px;
}
.code-input {
  flex: 1; padding: 10px 16px; border-radius: 4px;
  border: 1px solid rgba(255,255,255,0.15);
  background: rgba(255,255,255,0.06);
  color: #fff; font-size: 0.9rem; outline: none;
}
.code-input:focus { border-color: #e94560; }
.collect-btn {
  padding: 10px 24px; border: 1px solid #e94560;
  color: #e94560; background: transparent; border-radius: 4px;
  cursor: pointer; font-size: 0.9rem; transition: all 0.2s;
}
.collect-btn:hover:not(:disabled) { background: #e94560; color: #fff; }
.collect-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.collect-msg { font-size: 0.85rem; color: #27ae60; margin-bottom: 16px; }

/* 卡片列表 */
.coupon-list { display: flex; flex-direction: column; gap: 12px; }
.coupon-card {
  display: flex; align-items: center;
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 6px; overflow: hidden;
  transition: border-color 0.2s;
}
.coupon-card.used { opacity: 0.5; }
.coupon-card:hover { border-color: rgba(233,69,96,0.3); }

.coupon-left {
  width: 120px; text-align: center; padding: 16px;
  background: rgba(233,69,96,0.08);
  flex-shrink: 0;
}
.coupon-value { color: #e94560; line-height: 1; }
.value-symbol { font-size: 0.8rem; vertical-align: top; }
.value-num { font-size: 1.8rem; font-weight: 700; }
.value-unit { font-size: 0.9rem; }
.coupon-condition { font-size: 0.72rem; color: rgba(255,255,255,0.4); margin-top: 4px; }

.coupon-body { flex: 1; padding: 14px 16px; min-width: 0; }
.coupon-name { font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
.coupon-desc { font-size: 0.8rem; color: rgba(255,255,255,0.5); margin-bottom: 4px; }
.coupon-date { font-size: 0.75rem; color: rgba(255,255,255,0.35); }

.coupon-status { padding: 14px 16px; flex-shrink: 0; }
.tag {
  font-size: 0.75rem; padding: 2px 10px; border-radius: 3px;
}
.tag.unused { background: rgba(39,174,96,0.2); color: #27ae60; }
.tag.used { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.4); }
.tag.expired { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3); }
</style>
