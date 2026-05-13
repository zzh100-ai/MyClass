<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
  password2: '',
  email: '',
  mobile: '',
})
const errorMsg = ref('')

async function handleRegister() {
  errorMsg.value = ''
  if (!form.username || !form.password || !form.password2) {
    errorMsg.value = '请填写必填项'
    return
  }
  if (form.password !== form.password2) {
    errorMsg.value = '两次密码不一致'
    return
  }
  try {
    await authStore.registerAction({
      username: form.username,
      password: form.password,
      password2: form.password2,
      email: form.email || undefined,
      mobile: form.mobile || undefined,
    })
    router.push('/')
  } catch (err) {
    errorMsg.value = err.message || '注册失败'
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

      <form @submit.prevent="handleRegister" class="auth-form">
        <h2>注册</h2>

        <div v-if="errorMsg" class="form-error">{{ errorMsg }}</div>

        <div class="form-group">
          <label for="username">用户名 <span class="required">*</span></label>
          <input
            id="username"
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            autocomplete="username"
          />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="password">密码 <span class="required">*</span></label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              placeholder="至少8位，包含字母和数字"
              autocomplete="new-password"
            />
          </div>
          <div class="form-group">
            <label for="password2">确认密码 <span class="required">*</span></label>
            <input
              id="password2"
              v-model="form.password2"
              type="password"
              placeholder="再次输入密码"
              autocomplete="new-password"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="email">邮箱</label>
          <input
            id="email"
            v-model="form.email"
            type="email"
            placeholder="请输入邮箱（选填）"
            autocomplete="email"
          />
        </div>

        <div class="form-group">
          <label for="mobile">手机号</label>
          <input
            id="mobile"
            v-model="form.mobile"
            type="text"
            placeholder="请输入手机号（选填）"
            autocomplete="tel"
          />
        </div>

        <button type="submit" class="btn-primary">注 册</button>

        <p class="form-switch">
          已有账号？<router-link to="/login">立即登录</router-link>
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
  max-width: 460px;
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

.form-row {
  display: flex;
  gap: 12px;
}

.form-row .form-group {
  flex: 1;
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

.required {
  color: #e94560;
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
