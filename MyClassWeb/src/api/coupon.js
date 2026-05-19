import api from '@/utils/api'

export function getUserCoupons() {
  return api.get('/user-coupons/')
}

export function collectCoupon(code) {
  return api.post('/user-coupons/collect/', { code })
}

export function getPoints() {
  return api.get('/points/')
}

export function getPointsHistory(params) {
  return api.get('/points/history/', { params })
}
