<template>
  <div class="login-page">
    <el-card class="login-card">
      <h2 class="login-title">管理后台登录</h2>
      <el-form :model="form" :rules="rules" ref="formRef" @submit.prevent="handleLogin">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名" size="large" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码" size="large" show-password />
        </el-form-item>
        <el-form-item prop="captcha_code">
          <div class="captcha-row">
            <el-input v-model="form.captcha_code" placeholder="验证码" size="large" autocomplete="off" />
            <img :src="captchaImage" @click="loadCaptcha" class="captcha-img" title="点击刷新" />
          </div>
        </el-form-item>
        <el-button type="primary" size="large" :loading="loading" style="width:100%" native-type="submit">
          登录
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import { authApi } from '../api/auth'
import { useAdminStore } from '../store/admin'
import http from '../api/index'

const router = useRouter()
const adminStore = useAdminStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const captchaImage = ref('')

const form = reactive({ username: '', password: '', captcha_key: '', captcha_code: '' })
const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  captcha_code: [{ required: true, message: '请输入验证码', trigger: 'blur' }],
}

async function loadCaptcha() {
  try {
    const res = await http.get('/auth/captcha')
    captchaImage.value = res.data.data.captcha_image
    form.captcha_key = res.data.data.captcha_key
  } catch { /* ignore */ }
}

async function handleLogin() {
  await formRef.value?.validate()
  loading.value = true
  try {
    const res = await authApi.login(form)
    const tokens = res.data.data!
    adminStore.setToken(tokens.access_token)
    await adminStore.init()
    if (adminStore.admin?.role !== 'admin') {
      adminStore.logout()
      ElMessage.error('需要管理员权限')
      return
    }
    router.push('/')
  } catch (e) {
    ElMessage.error((e as Error).message)
    loadCaptcha()
  } finally {
    loading.value = false
  }
}

onMounted(() => loadCaptcha())
</script>

<style scoped>
.login-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}
.login-card { width: 400px; }
.login-title { text-align: center; margin-bottom: 24px; font-size: 22px; }
.captcha-row { display: flex; gap: 8px; width: 100%; align-items: center; }
.captcha-row .el-input { flex: 1; }
.captcha-img {
  height: 40px;
  border-radius: 4px;
  cursor: pointer;
  flex-shrink: 0;
}
</style>
