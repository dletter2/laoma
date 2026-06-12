<template>
  <div class="user-manage">
    <el-table :data="users" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column prop="role" label="角色" width="100">
        <template #default="{ row }">
          <el-tag :type="row.role === 'admin' ? 'danger' : ''">{{ row.role === 'admin' ? '管理员' : '用户' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">{{ row.status === 'active' ? '正常' : '已禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="注册时间" width="180" />
      <el-table-column label="操作" width="120">
        <template #default="{ row }">
          <el-button
            v-if="row.role !== 'admin'"
            size="small"
            :type="row.status === 'active' ? 'danger' : 'success'"
            @click="toggleStatus(row)"
          >{{ row.status === 'active' ? '禁用' : '启用' }}</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
      v-model:current-page="page"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      @current-change="loadData"
      style="margin-top:16px; justify-content: center;"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { userApi } from '../api/user'
import type { User } from '../types'

const users = ref<User[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)

async function loadData() {
  loading.value = true
  try {
    const res = await userApi.list({ page: page.value, page_size: pageSize })
    users.value = res.data.data?.items || []
    total.value = res.data.data?.total || 0
  } finally {
    loading.value = false
  }
}

async function toggleStatus(user: User) {
  const newStatus = user.status === 'active' ? 'disabled' : 'active'
  try {
    await userApi.updateStatus(user.id, newStatus)
    ElMessage.success('操作成功')
    loadData()
  } catch (e) {
    ElMessage.error((e as Error).message)
  }
}

onMounted(() => loadData())
</script>
