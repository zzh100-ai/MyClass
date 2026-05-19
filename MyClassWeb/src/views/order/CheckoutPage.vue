<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useOrderStore } from '@/stores/order'
import { useCouponStore } from '@/stores/coupon'
import { ElMessage } from 'element-plus'
import NavBar from '@/components/NavBar.vue'
import PageFooter from '@/components/PageFooter.vue'

const router = useRouter()
const cartStore = useCartStore()
const orderStore = useOrderStore()
const couponStore = useCouponStore()

const submitting = ref(false)
const selectedCouponId = ref(null)
const submitError = ref('')
const pointsToUse = ref(0)

onMounted(async () => {
  cartStore.fetchCart()
  couponStore.fetchCoupons()
  couponStore.fetchPoints()
})

const paidCourses = computed(() => cartStore.items.filter(c => !c.is_free))
const freeCourses = computed(() => cartStore.items.filter(c => c.is_free))
const totalPrice = computed(() => paidCourses.value.reduce((s, c) => s + parseFloat(c.price || 0), 0).toFixed(2))

const usableCoupons = computed(() =>
  couponStore.coupons.filter(
    uc => uc.status === 'unused'
      && new Date(uc.coupon.valid_to) > new Date()
      && parseFloat(uc.coupon.min_amount) <= parseFloat(totalPrice.value)
  )
)

const maxPoints = computed(() => {
  const total = parseFloat(totalPrice.value)
  // 最多抵扣总价，每100积分=¥1
  return Math.min(couponStore.points, Math.floor(total * 100))
})

async function handleSubmit() {
  if (cartStore.items.length === 0) return
  submitting.value = true
  submitError.value = ''

  try {
    const courseIds = cartStore.items.map(c => c.id)
    const order = await orderStore.createOrder(courseIds, {
      coupon_id: selectedCouponId.value,
      points: pointsToUse.value,
    })
    cartStore.items = []
    cartStore.count = 0
    router.push(`/orders/${order.id}`)
  } catch (e) {
    const msg = e.message || '创建订单失败'
    submitError.value = msg
    ElMessage.error(msg)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="checkout-page">
    <NavBar />
    <main class="main-content">
      <h1 class="page-title">确认订单</h1>

      <!-- 错误提示 -->
      <p v-if="submitError" class="error-msg">{{ submitError }}</p>

      <div v-if="cartStore.loading" class="state-msg">加载中...</div>
      <div v-else-if="cartStore.items.length === 0" class="state-msg">
        <p>购物车是空的</p>
        <button class="link-btn" @click="router.push('/courses')">去选课</button>
      </div>

      <template v-else>
        <div v-if="freeCourses.length" class="info-bar">
          ⚡ 包含 {{ freeCourses.length }} 门免费课程，支付后自动获得
        </div>

        <!-- 课程清单 -->
        <div class="section">
          <h3 class="section-title">课程清单</h3>
          <div class="order-items">
            <div v-for="course in cartStore.items" :key="course.id" class="order-item">
              <div class="item-info">
                <span class="item-title">{{ course.title }}</span>
                <span class="item-teacher">{{ course.teacher_name }}</span>
              </div>
              <span class="item-price">{{ course.is_free ? '免费' : `¥${course.price}` }}</span>
            </div>
          </div>
        </div>

        <!-- 优惠券 -->
        <div class="section">
          <h3 class="section-title">优惠券</h3>
          <div class="coupon-options">
            <label class="coupon-option" :class="{ selected: selectedCouponId === null }">
              <input type="radio" :value="null" v-model="selectedCouponId" />
              <span class="coupon-label">不使用优惠券</span>
            </label>
            <label v-for="uc in usableCoupons" :key="uc.id" class="coupon-option"
              :class="{ selected: selectedCouponId === uc.id }">
              <input type="radio" :value="uc.id" v-model="selectedCouponId" />
              <span class="coupon-label">
                {{ uc.coupon.name }} —
                <strong>{{ uc.coupon.discount_type === 'percent' ? `${uc.coupon.discount_value}折` : `减¥${uc.coupon.discount_value}` }}</strong>
              </span>
            </label>
          </div>
        </div>

        <!-- 积分 -->
        <div class="section">
          <h3 class="section-title">积分抵扣</h3>
          <div class="points-row">
            <span class="points-label">当前积分 {{ couponStore.points }}，最多可抵 ¥{{ (maxPoints * 0.01).toFixed(2) }}</span>
          </div>
          <div class="points-input-row">
            <input type="number" v-model.number="pointsToUse" :max="maxPoints" min="0"
              class="points-input" placeholder="输入使用的积分数" />
            <button class="max-btn" @click="pointsToUse = maxPoints">全部使用</button>
          </div>
        </div>

        <!-- 底部 -->
        <div class="checkout-footer">
          <div class="footer-total">
            <span class="total-label">合计：</span>
            <span class="total-price">¥{{ totalPrice }}</span>
          </div>
          <button class="submit-btn" :disabled="submitting" @click="handleSubmit">
            {{ submitting ? '提交中...' : '提交订单' }}
          </button>
        </div>

      </template>
    </main>
    <PageFooter />
  </div>
</template>

<style scoped>
.checkout-page {
  min-height: 100vh;
  background: linear-gradient(160deg, #1a1a3e, #1e2a4a, #1c2541, #1a1a3e);
  color: rgba(255, 255, 255, 0.94);
}
.main-content { max-width: 700px; margin: 0 auto; padding: 40px 48px 80px; }
.page-title { font-size: 1.5rem; font-weight: 600; margin-bottom: 28px; }
.state-msg { text-align: center; padding: 80px 0; color: rgba(255,255,255,0.4); }
.link-btn { margin-top: 16px; background: transparent; border: 1px solid #e94560; color: #e94560; padding: 8px 24px; border-radius: 4px; cursor: pointer; }
.info-bar { background: rgba(39,174,96,0.1); border: 1px solid rgba(39,174,96,0.3); border-radius: 6px; padding: 12px 16px; font-size: 0.85rem; color: #27ae60; margin-bottom: 20px; }

.section { margin-bottom: 24px; }
.section-title { font-size: 1rem; font-weight: 600; margin-bottom: 12px; }

.order-items { border: 1px solid rgba(255,255,255,0.1); border-radius: 6px; overflow: hidden; }
.order-item { display: flex; justify-content: space-between; align-items: center; padding: 14px 16px; border-bottom: 1px solid rgba(255,255,255,0.06); }
.order-item:last-child { border-bottom: none; }
.item-info { display: flex; flex-direction: column; gap: 4px; }
.item-title { font-size: 0.95rem; font-weight: 500; }
.item-teacher { font-size: 0.8rem; color: rgba(255,255,255,0.45); }
.item-price { font-size: 1rem; font-weight: 600; color: #e94560; flex-shrink: 0; }

.no-data { font-size: 0.85rem; color: rgba(255,255,255,0.35); padding: 8px 0; }

.coupon-options { display: flex; flex-direction: column; gap: 8px; }
.coupon-option { display: flex; align-items: center; gap: 10px; padding: 10px 14px; border: 1px solid rgba(255,255,255,0.1); border-radius: 4px; cursor: pointer; transition: border-color 0.2s; }
.coupon-option:hover { border-color: rgba(233,69,96,0.3); }
.coupon-option.selected { border-color: #e94560; background: rgba(233,69,96,0.06); }
.coupon-option input { accent-color: #e94560; }
.coupon-label { font-size: 0.85rem; }
.coupon-label strong { color: #e94560; }

.points-row { font-size: 0.85rem; color: rgba(255,255,255,0.5); margin-bottom: 8px; }
.points-input-row { display: flex; gap: 10px; }
.points-input { flex: 1; padding: 10px 14px; border: 1px solid rgba(255,255,255,0.15); border-radius: 4px; background: rgba(255,255,255,0.06); color: #fff; font-size: 0.9rem; outline: none; }
.points-input:focus { border-color: #e94560; }
.max-btn { padding: 10px 16px; border: 1px solid rgba(255,255,255,0.15); background: transparent; color: rgba(255,255,255,0.6); border-radius: 4px; cursor: pointer; font-size: 0.8rem; transition: all 0.2s; }
.max-btn:hover { border-color: #e94560; color: #e94560; }

.checkout-footer { display: flex; justify-content: flex-end; align-items: center; gap: 24px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.08); }
.footer-total { display: flex; align-items: baseline; gap: 4px; }
.total-label { font-size: 0.9rem; color: rgba(255,255,255,0.6); }
.total-price { font-size: 1.4rem; font-weight: 700; color: #e94560; }
.submit-btn { background: #e94560; border: none; color: #fff; padding: 12px 40px; border-radius: 4px; font-size: 1rem; cursor: pointer; letter-spacing: 1px; transition: background 0.2s; }
.submit-btn:hover:not(:disabled) { background: #d63850; }
.submit-btn:disabled { opacity: 0.5; cursor: not-allowed; }
.error-msg { text-align: center; color: #e94560; font-size: 0.85rem; margin-top: 16px; padding: 10px; background: rgba(233,69,96,0.1); border-radius: 4px; }
</style>
