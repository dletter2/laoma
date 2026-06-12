<template>
  <div class="settings-page">
    <el-card>
      <template #header><span>钉钉通知配置</span></template>
      <el-form label-width="140px">
        <el-form-item label="Webhook 地址">
          <el-input v-model="webhookUrl" placeholder="请输入钉钉机器人 Webhook 地址" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="saveWebhook" :loading="saving">保存</el-button>
          <el-button @click="testWebhook" :loading="testing" :disabled="!webhookUrl">测试通知</el-button>
        </el-form-item>
      </el-form>
      <el-alert
        v-if="webhookUrl"
        title="配置后，用户在 C 端提交新资源时将自动通过钉钉机器人发送通知"
        type="info"
        :closable="false"
        show-icon
        style="margin-top: 12px;"
      />
    </el-card>

    <el-card style="margin-top: 20px;">
      <template #header><span>修改密码</span></template>
      <el-form :model="pwdForm" :rules="pwdRules" ref="pwdFormRef" label-width="140px" style="max-width: 480px;">
        <el-form-item label="旧密码" prop="old_password">
          <el-input v-model="pwdForm.old_password" type="password" placeholder="请输入旧密码" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="pwdForm.new_password" type="password" placeholder="请输入新密码（至少6位）" show-password />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirm_password">
          <el-input v-model="pwdForm.confirm_password" type="password" placeholder="请再次输入新密码" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleChangePassword" :loading="pwdLoading">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import type { FormInstance } from 'element-plus'
import http from '../api'
import { authApi } from '../api/auth'

const webhookUrl = ref('')
const saving = ref(false)
const testing = ref(false)

const pwdFormRef = ref<FormInstance>()
const pwdLoading = ref(false)
const pwdForm = reactive({ old_password: '', new_password: '', confirm_password: '' })

const pwdRules = {
  old_password: [{ required: true, message: '请输入旧密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
  confirm_password: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    {
      validator: (_rule: unknown, value: string, callback: (err?: Error) => void) => {
        if (value !== pwdForm.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur',
    },
  ],
}

onMounted(async () => {
  try {
    const res = await http.get('/admin/settings/dingtalk_webhook')
    webhookUrl.value = res.data.data?.value || ''
  } catch { /* ignore */ }
})

async function saveWebhook() {
  saving.value = true
  try {
    await http.put('/admin/settings/dingtalk_webhook', null, { params: { value: webhookUrl.value } })
    ElMessage.success('保存成功')
  } catch (e) {
    ElMessage.error((e as Error).message)
  } finally {
    saving.value = false
  }
}

async function testWebhook() {
  testing.value = true
  try {
    await http.post('/admin/settings/test-webhook')
    ElMessage.success('测试通知已发送，请检查钉钉群')
  } catch (e) {
    ElMessage.error('发送失败: ' + (e as Error).message)
  } finally {
    testing.value = false
  }
}

async function handleChangePassword() {
  await pwdFormRef.value?.validate()
  pwdLoading.value = true
  try {
    await authApi.changePassword({ old_password: pwdForm.old_password, new_password: pwdForm.new_password })
    ElMessage.success('密码修改成功')
    pwdForm.old_password = ''
    pwdForm.new_password = ''
    pwdForm.confirm_password = ''
    pwdFormRef.value?.resetFields()
  } catch (e) {
    ElMessage.error((e as Error).message)
  } finally {
    pwdLoading.value = false
  }
}
</script>
