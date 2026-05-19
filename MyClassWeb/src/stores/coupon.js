import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as couponApi from '@/api/coupon'

export const useCouponStore = defineStore('coupon', () => {
  const coupons = ref([])
  const points = ref(0)
  const pointsHistory = ref([])
  const historyTotal = ref(0)
  const loading = ref(false)

  async function fetchCoupons() {
    try {
      const res = await couponApi.getUserCoupons()
      coupons.value = res.results || res
    } catch {
      coupons.value = []
    }
  }

  async function collectCoupon(code) {
    const res = await couponApi.collectCoupon(code)
    await fetchCoupons()
    return res
  }

  async function fetchPoints() {
    try {
      const res = await couponApi.getPoints()
      points.value = res.points
    } catch {
      points.value = 0
    }
  }

  async function fetchHistory(page = 1) {
    loading.value = true
    try {
      const res = await couponApi.getPointsHistory({ page, page_size: 20 })
      pointsHistory.value = res.results
      historyTotal.value = res.total
    } finally {
      loading.value = false
    }
  }

  return {
    coupons, points, pointsHistory, historyTotal, loading,
    fetchCoupons, collectCoupon, fetchPoints, fetchHistory,
  }
})
