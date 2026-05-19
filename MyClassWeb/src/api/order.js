import api from '@/utils/api'

export function createOrder(courseIds, options = {}) {
  return api.post('/orders/', { course_ids: courseIds, ...options })
}

export function getOrders() {
  return api.get('/orders/')
}

export function getOrder(id) {
  return api.get(`/orders/${id}/`)
}

export function payOrder(id) {
  return api.post(`/orders/${id}/pay/`)
}
