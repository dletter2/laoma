<template>
  <div class="resource-manage">
    <div class="toolbar">
      <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="loadData">
        <el-option label="待审核" value="pending" />
        <el-option label="已通过" value="approved" />
        <el-option label="已拒绝" value="rejected" />
        <el-option label="已上架" value="published" />
        <el-option label="已下架" value="unpublished" />
      </el-select>
    </div>
    <el-table :data="resources" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
      <el-table-column prop="category_name" label="分类" width="100" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="浏览" width="80" />
      <el-table-column prop="upload_time" label="上传时间" width="160" />
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" type="success" @click="changeStatus(row.id, 'published')" v-if="row.status === 'pending' || row.status === 'approved'">上架</el-button>
          <el-button size="small" type="warning" @click="changeStatus(row.id, 'approved')" v-if="row.status === 'pending'">通过</el-button>
          <el-button size="small" type="danger" @click="changeStatus(row.id, 'rejected')" v-if="row.status === 'pending'">拒绝</el-button>
          <el-button size="small" type="info" @click="changeStatus(row.id, 'unpublished')" v-if="row.status === 'published'">下架</el-button>
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
import { resourceApi } from '../api/resource'
import type { Resource } from '../types'

const resources = ref<Resource[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const statusFilter = ref('')

const statusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已通过', type: 'success' },
  rejected: { label: '已拒绝', type: 'danger' },
  published: { label: '已上架', type: '' },
  unpublished: { label: '已下架', type: 'info' },
}

function statusLabel(s: string) { return statusMap[s]?.label || s }
function statusType(s: string) { return statusMap[s]?.type || '' }

async function loadData() {
  loading.value = true
  try {
    const res = await resourceApi.list({ page: page.value, page_size: pageSize })
    let items = res.data.data?.items || []
    if (statusFilter.value) {
      items = items.filter((r) => r.status === statusFilter.value)
    }
    resources.value = items
    total.value = res.data.data?.total || 0
  } finally {
    loading.value = false
  }
}

async function changeStatus(id: number, status: string) {
  try {
    await resourceApi.updateStatus(id, status)
    ElMessage.success('操作成功')
    loadData()
  } catch (e) {
    ElMessage.error((e as Error).message)
  }
}

onMounted(() => loadData())
</script>

<style scoped>
.toolbar { margin-bottom: 16px; }
</style>
