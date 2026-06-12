<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="auth-title">注册</h2>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>用户名</label>
          <input v-model="form.username" type="text" placeholder="请输入用户名（至少2个字符）" required />
        </div>
        <div class="form-group">
          <label>昵称（选填）</label>
          <input v-model="form.nickname" type="text" placeholder="不填将自动生成" />
        </div>
        <div class="form-group">
          <label>密码</label>
          <input v-model="form.password" type="password" placeholder="请输入密码（至少6位）" required />
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input v-model="form.confirmPassword" type="password" placeholder="再次输入密码" required />
        </div>
        <div class="form-group">
          <label>验证码</label>
          <div class="captcha-row">
            <input v-model="form.captcha_code" type="text" placeholder="请输入验证码" required autocomplete="off" />
            <img :src="captchaImage" @click="loadCaptcha" class="captcha-img" title="点击刷新" />
          </div>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn btn-primary" :disabled="submitting">
          {{ submitting ? '注册中...' : '注册' }}
        </button>
      </form>
      <p class="auth-switch">
        已有账号？<router-link to="/login">立即登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '../api/auth'
import http from '../api/index'

const router = useRouter()
const form = ref({ username: '', password: '', confirmPassword: '', nickname: '', captcha_key: '', captcha_code: '' })
const captchaImage = ref('')
const error = ref('')
const submitting = ref(false)

async function loadCaptcha() {
  try {
    const res = await http.get('/auth/captcha')
    captchaImage.value = res.data.data.captcha_image
    form.value.captcha_key = res.data.data.captcha_key
  } catch { /* ignore */ }
}

async function handleRegister() {
  error.value = ''
  if (form.value.username.length < 2) { error.value = '用户名至少2个字符'; return }
  if (form.value.password.length < 6) { error.value = '密码至少6位'; return }
  if (form.value.password !== form.value.confirmPassword) { error.value = '两次密码不一致'; return }
  submitting.value = true
  try {
    await authApi.register({
      username: form.value.username,
      password: form.value.password,
      nickname: form.value.nickname || undefined,
      captcha_key: form.value.captcha_key,
      captcha_code: form.value.captcha_code,
    })
    alert('注册成功，请登录')
    router.push('/login')
  } catch (e) {
    error.value = (e as Error).message
    loadCaptcha()
  } finally {
    submitting.value = false
  }
}

onMounted(() => loadCaptcha())
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
.captcha-row { display: flex; gap: 8px; align-items: center; }
.captcha-row input { flex: 1; }
.captcha-img {
  height: 40px;
  border-radius: 6px;
  cursor: pointer;
  flex-shrink: 0;
}
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
