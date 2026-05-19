import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as orderApi from '@/api/order'

export const useOrderStore = defineStore('order', () => {
  const orders = ref([])
  const currentOrder = ref(null)
  const loading = ref(false)
  const paying = ref(false)

  async function fetchOrders() {
    loading.value = true
    try {
      const res = await orderApi.getOrders()
      // DRF 分页返回 {count, results}，提取 results
      orders.value = res.results || res
    } catch (e) {
      console.error('获取订单列表失败:', e.message)
    } finally {
      loading.value = false
    }
  }

  async function fetchOrder(id) {
    currentOrder.value = null
    try {
      currentOrder.value = await orderApi.getOrder(id)
    } catch (e) {
      console.error('获取订单详情失败:', e.message)
    }
  }

  async function createOrder(courseIds, options = {}) {
    const res = await orderApi.createOrder(courseIds, options)
    return res
  }

  async function payOrder(id) {
    paying.value = true
    try {
      const res = await orderApi.payOrder(id)
      // 重新加载订单详情获取最新状态
      await fetchOrder(id)
      return res
    } finally {
      paying.value = false
    }
  }

  return { orders, currentOrder, loading, paying, fetchOrders, fetchOrder, createOrder, payOrder }
})
