<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="auth-title">登录</h2>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名" required />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码" required />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="auth-switch">
        还没有账号？<router-link to="/register">立即注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { authApi } from '../api/auth'
import { useUserStore } from '../store/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const form = ref({ username: '', password: '' })
const error = ref('')
const submitting = ref(false)

async function handleLogin() {
  error.value = ''
  submitting.value = true
  try {
    const res = await authApi.login(form.value)
    const tokens = res.data.data!
    userStore.setTokens(tokens.access_token, tokens.refresh_token)
    await userStore.init()
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e) {
    error.value = (e as Error).message
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 40px 20px;
}
.auth-card {
  width: 400px;
  background: var(--bg-white);
  border-radius: var(--radius);
  padding: 32px;
  box-shadow: var(--shadow-md);
}
.auth-title { text-align: center; font-size: 24px; margin-bottom: 24px; }
.form-group { margin-bottom: 16px; }
.form-group label { display: block; font-size: 14px; margin-bottom: 6px; }
.form-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
}
.form-group input:focus { border-color: var(--primary); }
.error { color: #f56c6c; font-size: 13px; margin-bottom: 12px; }
.btn {
  width: 100%;
  padding: 12px;
  border-radius: var(--radius);
  font-size: 16px;
}
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary-dark); }
.btn-primary:disabled { opacity: 0.6; }
.auth-switch { text-align: center; margin-top: 16px; font-size: 14px; color: var(--text-secondary); }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .auth-page { padding: 24px 16px; align-items: flex-start; padding-top: 48px; }
  .auth-card { width: 100%; padding: 24px 20px; box-shadow: none; border-radius: 12px; }
  .auth-title { font-size: 22px; }
  .form-group input { font-size: 16px; /* prevent iOS zoom */ }
}
</style>
