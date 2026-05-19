import axios from 'axios'

const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
})

// 请求拦截器：自动附加 access token
service.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error),
)

// 响应拦截器：统一错误处理 + 401 自动刷新 token
service.interceptors.response.use(
  (response) => {
    return response.data
  },
  async (error) => {
    const { response, config } = error

    // 网络错误或无响应
    if (!response) {
      return Promise.reject(new Error('网络连接失败，请检查后端服务是否启动'))
    }

    const { status, data } = response
    // 提取错误信息
    let msg = ''
    if (data) {
      if (typeof data === 'string') {
        msg = data
      } else if (data.msg || data.detail) {
        msg = data.msg || data.detail
      } else if (Array.isArray(data)) {
        msg = data[0] || ''
      } else if (typeof data === 'object') {
        const firstErr = Object.values(data).find(v => Array.isArray(v) && v.length > 0)
        if (firstErr) msg = firstErr[0]
      }
    }
    msg = msg || '请求失败'

    // 401 且非刷新请求本身 → 尝试用 refresh token 刷新
    if (status === 401 && !config.url?.includes('/auth/refresh/')) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (refreshToken) {
        try {
          const res = await axios.post(
            `${config.baseURL}/auth/refresh/`,
            { refresh: refreshToken },
          )
          const { access, refresh } = res.data.data || res.data
          localStorage.setItem('access_token', access)
          if (refresh) {
            localStorage.setItem('refresh_token', refresh)
          }
          // 用新 token 重试原请求
          config.headers.Authorization = `Bearer ${access}`
          return service(config)
        } catch {
          // 刷新失败，清除登录态
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          localStorage.removeItem('user')
        }
      }
    }

    return Promise.reject(new Error(msg))
  },
)

export default service
