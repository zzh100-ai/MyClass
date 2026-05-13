import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import * as authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const accessToken = ref(localStorage.getItem('access_token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')

  const isAuthenticated = computed(() => !!accessToken.value)

  function saveTokens(access, refresh) {
    accessToken.value = access
    localStorage.setItem('access_token', access)
    if (refresh) {
      refreshToken.value = refresh
      localStorage.setItem('refresh_token', refresh)
    }
  }

  function saveUser(userData) {
    user.value = userData
    localStorage.setItem('user', JSON.stringify(userData))
  }

  function clearAuth() {
    user.value = null
    accessToken.value = ''
    refreshToken.value = ''
    localStorage.removeItem('user')
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function loginAction(credentials) {
    const res = await authApi.login(credentials)
    saveTokens(res.data.access, res.data.refresh)
    saveUser(res.data.user)
    return res
  }

  async function registerAction(formData) {
    const res = await authApi.register(formData)
    saveTokens(res.data.access, res.data.refresh)
    saveUser(res.data.user)
    return res
  }

  async function refreshAccessToken() {
    if (!refreshToken.value) {
      throw new Error('无 refresh token')
    }
    const res = await authApi.refreshToken(refreshToken.value)
    saveTokens(res.data.access, res.data.refresh)
    return res
  }

  function logout() {
    clearAuth()
  }

  return {
    user,
    accessToken,
    refreshToken,
    isAuthenticated,
    loginAction,
    registerAction,
    refreshAccessToken,
    logout,
    clearAuth,
  }
})
