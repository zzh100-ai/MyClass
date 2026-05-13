<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  identifier: '',
  password: '',
})
const errorMsg = ref('')

async function handleLogin() {
  errorMsg.value = ''
  if (!form.identifier || !form.password) {
    errorMsg.value = '请填写账号和密码'
    return
  }
  try {
    await authStore.loginAction({
      identifier: form.identifier,
      password: form.password,
    })
    router.push('/')
  } catch (err) {
    errorMsg.value = err.message || '登录失败'
  }
}
</script>

<template>
  <div class="auth-container">
    <div class="auth-card">
      <div class="auth-header">
        <h1>MyClass</h1>
        <p>在线教育平台</p>
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <h2>登录</h2>

        <div v-if="errorMsg" class="form-error">{{ errorMsg }}</div>

        <div class="form-group">
          <label for="identifier">用户名 / 手机号 / 邮箱</label>
          <input
            id="identifier"
            v-model="form.identifier"
            type="text"
            placeholder="请输入用户名、手机号或邮箱"
            autocomplete="username"
          />
        </div>

        <div class="form-group">
          <label for="password">密码</label>
          <input
            id="password"
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            autocomplete="current-password"
          />
        </div>

        <button type="submit" class="btn-primary">登 录</button>

        <p class="form-switch">
          还没有账号？<router-link to="/register">立即注册</router-link>
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.auth-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  padding: 20px;
}

.auth-card {
  width: 100%;
  max-width: 420px;
}

.auth-header {
  text-align: center;
  margin-bottom: 30px;
}

.auth-header h1 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #e94560;
  margin: 0;
  letter-spacing: 2px;
}

.auth-header p {
  color: rgba(255, 255, 255, 0.6);
  margin: 8px 0 0;
  font-size: 0.95rem;
  letter-spacing: 1px;
}

.auth-form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 40px 32px;
}

.auth-form h2 {
  color: #fff;
  font-size: 1.5rem;
  margin: 0 0 24px;
  text-align: center;
}

.form-error {
  background: rgba(233, 69, 96, 0.15);
  border: 1px solid rgba(233, 69, 96, 0.3);
  color: #e94560;
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 0.9rem;
  margin-bottom: 16px;
}

.form-group {
  margin-bottom: 18px;
}

.form-group label {
  display: block;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  margin-bottom: 6px;
}

.form-group input {
  width: 100%;
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  color: #fff;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, background 0.2s;
  box-sizing: border-box;
}

.form-group input::placeholder {
  color: rgba(255, 255, 255, 0.3);
}

.form-group input:focus {
  border-color: #e94560;
  background: rgba(255, 255, 255, 0.12);
}

.btn-primary {
  width: 100%;
  padding: 12px;
  background: linear-gradient(135deg, #e94560, #c23152);
  border: none;
  border-radius: 8px;
  color: #fff;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s, box-shadow 0.15s;
  margin-top: 8px;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(233, 69, 96, 0.35);
}

.btn-primary:active {
  transform: translateY(0);
}

.form-switch {
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  margin-top: 20px;
  font-size: 0.9rem;
}

.form-switch a {
  color: #e94560;
  text-decoration: none;
  font-weight: 500;
}

.form-switch a:hover {
  text-decoration: underline;
}
</style>
