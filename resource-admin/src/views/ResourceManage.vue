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
      <template v-if="selectedIds.length">
        <el-button type="success" @click="batchAction('published')">批量上架 ({{ selectedIds.length }})</el-button>
        <el-button type="info" @click="batchAction('unpublished')">批量下架 ({{ selectedIds.length }})</el-button>
        <el-button type="danger" @click="batchDelete">批量删除 ({{ selectedIds.length }})</el-button>
      </template>
    </div>
    <el-table :data="resources" stripe v-loading="loading" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="50" />
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="title" label="标题" min-width="180" show-overflow-tooltip />
      <el-table-column prop="category_name" label="分类" width="100" />
      <el-table-column label="上传用户" width="140">
        <template #default="{ row }">
          {{ row.uploader_nickname || row.uploader_name }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="statusType(row.status)">{{ statusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="浏览" width="70" />
      <el-table-column prop="upload_time" label="上传时间" width="160" />
      <el-table-column label="操作" width="320" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="showDetail(row)">详情</el-button>
          <el-button size="small" type="success" @click="changeStatus(row.id, 'published')"
            v-if="row.status === 'pending' || row.status === 'approved' || row.status === 'unpublished'">上架</el-button>
          <el-button size="small" type="warning" @click="changeStatus(row.id, 'approved')"
            v-if="row.status === 'pending'">通过</el-button>
          <el-button size="small" type="danger" @click="changeStatus(row.id, 'rejected')"
            v-if="row.status === 'pending'">拒绝</el-button>
          <el-button size="small" type="info" @click="changeStatus(row.id, 'unpublished')"
            v-if="row.status === 'published'">下架</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row.id)">删除</el-button>
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

    <el-dialog v-model="detailVisible" title="资源详情" width="600px">
      <el-descriptions :column="1" border v-if="detail">
        <el-descriptions-item label="ID">{{ detail.id }}</el-descriptions-item>
        <el-descriptions-item label="标题">{{ detail.title }}</el-descriptions-item>
        <el-descriptions-item label="分类">{{ detail.category_name }}</el-descriptions-item>
        <el-descriptions-item label="状态">
          <el-tag :type="statusType(detail.status)">{{ statusLabel(detail.status) }}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="上传用户">{{ detail.uploader_nickname || detail.uploader_name }}（{{ detail.uploader_name }}）</el-descriptions-item>
        <el-descriptions-item label="标签">{{ detail.tags || '无' }}</el-descriptions-item>
        <el-descriptions-item label="文件大小">{{ formatSize(detail.file_size) }}</el-descriptions-item>
        <el-descriptions-item label="资源描述">{{ detail.summary || '无' }}</el-descriptions-item>
        <el-descriptions-item label="分享链接">
          <a :href="detail.link" target="_blank" class="link-text">{{ detail.link }}</a>
        </el-descriptions-item>
        <el-descriptions-item label="提取码">{{ detail.link_password || '无' }}</el-descriptions-item>
        <el-descriptions-item label="浏览量">{{ detail.view_count }}</el-descriptions-item>
        <el-descriptions-item label="收藏数">{{ detail.favorite_count }}</el-descriptions-item>
        <el-descriptions-item label="上传时间">{{ detail.upload_time }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { resourceApi } from '../api/resource'
import type { Resource } from '../types'

const resources = ref<Resource[]>([])
const loading = ref(false)
const page = ref(1)
const pageSize = 20
const total = ref(0)
const statusFilter = ref('')
const detailVisible = ref(false)
const detail = ref<Resource | null>(null)
const selectedIds = ref<number[]>([])

const statusMap: Record<string, { label: string; type: string }> = {
  pending: { label: '待审核', type: 'warning' },
  approved: { label: '已通过', type: 'success' },
  rejected: { label: '已拒绝', type: 'danger' },
  published: { label: '已上架', type: '' },
  unpublished: { label: '已下架', type: 'info' },
}

function statusLabel(s: string) { return statusMap[s]?.label || s }
function statusType(s: string) { return statusMap[s]?.type || '' }

function formatSize(bytes: number) {
  if (!bytes) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let i = 0
  let size = bytes
  while (size >= 1024 && i < units.length - 1) { size /= 1024; i++ }
  return `${size.toFixed(i === 0 ? 0 : 1)} ${units[i]}`
}

function showDetail(row: Resource) {
  detail.value = row
  detailVisible.value = true
}

async function loadData() {
  loading.value = true
  try {
    const params: { page: number; page_size: number; status?: string } = { page: page.value, page_size: pageSize }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const res = await resourceApi.list(params)
    resources.value = res.data.data?.items || []
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

function handleSelectionChange(rows: Resource[]) {
  selectedIds.value = rows.map(r => r.id)
}

async function batchAction(status: string) {
  try {
    await ElMessageBox.confirm(`确定要批量${status === 'published' ? '上架' : '下架'} ${selectedIds.value.length} 条资源吗？`, '批量操作', { type: 'warning' })
    const res = await resourceApi.batchUpdateStatus(selectedIds.value, status)
    ElMessage.success(`操作成功，影响 ${res.data.data?.affected} 条`)
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error((e as Error).message)
  }
}

async function batchDelete() {
  try {
    await ElMessageBox.confirm(`确定要批量删除 ${selectedIds.value.length} 条资源吗？删除后不可恢复。`, '批量删除', { type: 'warning' })
    const res = await resourceApi.batchDelete(selectedIds.value)
    ElMessage.success(`删除成功，影响 ${res.data.data?.affected} 条`)
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error((e as Error).message)
  }
}

onMounted(() => loadData())

async function handleDelete(id: number) {
  try {
    await ElMessageBox.confirm('确定要删除该资源吗？删除后不可恢复。', '删除确认', { type: 'warning' })
    await resourceApi.delete(id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error((e as Error).message)
  }
}
</script>

<style scoped>
.toolbar { margin-bottom: 16px; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
.link-text { color: #409eff; word-break: break-all; }
</style>
