import api from '@/utils/api'

export function register(data) {
  return api.post('/auth/register/', data)
}

export function login(data) {
  return api.post('/auth/login/', data)
}

export function refreshToken(refresh) {
  return api.post('/auth/refresh/', { refresh })
}
