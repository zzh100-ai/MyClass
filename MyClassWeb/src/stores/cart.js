import { defineStore } from 'pinia'
import { ref } from 'vue'
import * as cartApi from '@/api/cart'

export const useCartStore = defineStore('cart', () => {
  const items = ref([])
  const count = ref(0)
  const loading = ref(false)

  async function fetchCart() {
    loading.value = true
    try {
      const res = await cartApi.getCart()
      items.value = res
    } catch (e) {
      console.error('获取购物车失败:', e.message)
      items.value = []
    } finally {
      loading.value = false
    }
  }

  async function fetchCount() {
    try {
      const res = await cartApi.getCartCount()
      count.value = res.count
    } catch {
      count.value = 0
    }
  }

  async function addCourse(courseId) {
    const res = await cartApi.addToCart(courseId)
    await fetchCount()
    return res
  }

  async function removeCourse(courseId) {
    await cartApi.removeFromCart(courseId)
    items.value = items.value.filter(c => c.id !== courseId)
    await fetchCount()
  }

  async function clearAll() {
    await cartApi.clearCart()
    items.value = []
    count.value = 0
  }

  return { items, count, loading, fetchCart, fetchCount, addCourse, removeCourse, clearAll }
})
