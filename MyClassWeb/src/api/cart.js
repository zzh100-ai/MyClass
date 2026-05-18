import api from '@/utils/api'

export function getCart() {
  return api.get('/cart/')
}

export function addToCart(courseId) {
  return api.post('/cart/', { course_id: courseId })
}

export function removeFromCart(courseId) {
  return api.delete(`/cart/${courseId}/`)
}

export function clearCart() {
  return api.delete('/cart/clear/')
}

export function getCartCount() {
  return api.get('/cart/count/')
}
