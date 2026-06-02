<template>
  <div class="upload-page container">
    <h1 class="page-title">上传中心</h1>

    <!-- Upload form -->
    <div class="upload-form card">
      <div class="form-group">
        <label>资源标题 <span class="required">*</span></label>
        <input v-model="form.title" type="text" placeholder="请输入资源标题" />
      </div>
      <div class="form-group">
        <label>资源分类 <span class="required">*</span></label>
        <select v-model="form.category_id">
          <option value="">请选择分类</option>
          <option v-for="c in categories" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div class="form-group">
        <label>标签（逗号分隔）</label>
        <input v-model="form.tags" type="text" placeholder="如：教程,入门,Python" />
      </div>
      <div class="form-group">
        <label>资源描述 <span class="required">*</span></label>
        <textarea v-model="form.summary" rows="4" placeholder="请描述资源内容"></textarea>
      </div>
      <div class="form-group">
        <label>资源文件 <span class="required">*</span></label>
        <div class="file-upload">
          <input type="file" ref="fileInput" @change="handleFile" />
          <div v-if="selectedFile" class="file-info">
            <span>{{ selectedFile.name }} ({{ formatSize(selectedFile.size) }})</span>
            <button class="btn-text" @click="removeFile">移除</button>
          </div>
          <p v-if="fileError" class="error">{{ fileError }}</p>
        </div>
      </div>
      <div class="form-group">
        <label>封面图</label>
        <input type="file" accept="image/*" @change="handleCover" />
        <div v-if="coverPreview" class="cover-preview">
          <img :src="coverPreview" alt="封面预览" />
        </div>
      </div>
      <div v-if="uploading" class="progress-bar">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        <span class="progress-text">{{ progress }}%</span>
      </div>
      <button class="btn btn-primary submit-btn" :disabled="uploading" @click="handleSubmit">
        {{ uploading ? '上传中...' : '提交资源' }}
      </button>
    </div>

    <!-- Upload history -->
    <div class="history-section">
      <h2 class="section-title">我的上传</h2>
      <div v-if="loadingHistory" style="text-align:center;padding:20px;">加载中...</div>
      <div v-else-if="myResources.length === 0" style="text-align:center;padding:20px;color:var(--text-secondary);">暂无上传记录</div>
      <div v-else class="history-list">
        <div v-for="r in myResources" :key="r.id" class="history-item">
          <div class="item-info">
            <span class="item-title">{{ r.title }}</span>
            <span class="item-time">{{ formatDate(r.upload_time) }}</span>
          </div>
          <span class="item-status" :class="r.status">{{ statusMap[r.status] || r.status }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { categoryApi } from '../api/category'
import { resourceApi } from '../api/resource'
import { useUserStore } from '../store/user'
import { formatSize, formatDate } from '../utils/format'
import type { Category } from '../types/api'
import type { Resource } from '../types/resource'

const userStore = useUserStore()
const categories = ref<Category[]>([])
const selectedFile = ref<File | null>(null)
const coverPreview = ref('')
const coverUrl = ref('')
const fileError = ref('')
const uploading = ref(false)
const progress = ref(0)
const myResources = ref<Resource[]>([])
const loadingHistory = ref(false)

const statusMap: Record<string, string> = {
  pending: '审核中',
  approved: '已通过',
  rejected: '已拒绝',
  published: '已上架',
  unpublished: '已下架',
}

const form = ref({
  title: '',
  category_id: '' as number | string,
  tags: '',
  summary: '',
})

function handleFile(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  if (file.size > 200 * 1024 * 1024) {
    fileError.value = '文件大小不能超过200MB'
    return
  }
  fileError.value = ''
  selectedFile.value = file
}

function removeFile() {
  selectedFile.value = null
}

function handleCover(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (file) {
    coverPreview.value = URL.createObjectURL(file)
    resourceApi.upload(file).then((res) => {
      coverUrl.value = res.data.data?.url || ''
    })
  }
}

async function handleSubmit() {
  if (!form.value.title || !form.value.category_id || !form.value.summary) {
    alert('请填写所有必填字段')
    return
  }
  if (!selectedFile.value) {
    alert('请选择资源文件')
    return
  }
  uploading.value = true
  progress.value = 0
  try {
    // Upload file first
    const uploadRes = await resourceApi.upload(selectedFile.value, (p) => { progress.value = p })
    const fileData = uploadRes.data.data
    // Create resource
    await resourceApi.create({
      title: form.value.title,
      summary: form.value.summary,
      category_id: Number(form.value.category_id),
      tags: form.value.tags,
      file_size: fileData?.size || 0,
      file_path: fileData?.url || '',
      cover_url: coverUrl.value,
    })
    alert('资源上传成功，等待审核！')
    form.value = { title: '', category_id: '', tags: '', summary: '' }
    selectedFile.value = null
    coverUrl.value = ''
    coverPreview.value = ''
    loadHistory()
  } catch (e) {
    alert((e as Error).message)
  } finally {
    uploading.value = false
  }
}

async function loadHistory() {
  loadingHistory.value = true
  try {
    // Using resource list as upload history (filter by uploader would need backend support)
    const res = await resourceApi.list({ sort: 'latest', page: 1, page_size: 20 })
    myResources.value = res.data.data?.items || []
  } finally {
    loadingHistory.value = false
  }
}

onMounted(async () => {
  const catRes = await categoryApi.list()
  categories.value = catRes.data.data || []
  loadHistory()
})
</script>

<style scoped>
.upload-page { padding: 30px 20px; }
.card {
  background: var(--bg-white);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}
.form-group { margin-bottom: 20px; }
.form-group label {
  display: block;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 6px;
  color: var(--text-primary);
}
.required { color: #f56c6c; }
.form-group input[type="text"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
  transition: border-color 0.2s;
}
.form-group input:focus, .form-group select:focus, .form-group textarea:focus {
  border-color: var(--primary);
}
.file-info { display: flex; align-items: center; gap: 12px; margin-top: 8px; font-size: 14px; }
.btn-text { background: none; color: var(--primary); font-size: 13px; }
.error { color: #f56c6c; font-size: 13px; margin-top: 4px; }
.cover-preview { margin-top: 8px; }
.cover-preview img { max-width: 200px; max-height: 150px; border-radius: 6px; }
.progress-bar {
  position: relative;
  height: 24px;
  background: var(--bg-page);
  border-radius: 12px;
  overflow: hidden;
  margin-bottom: 16px;
}
.progress-fill {
  height: 100%;
  background: var(--primary);
  border-radius: 12px;
  transition: width 0.3s;
}
.progress-text {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 12px;
  color: var(--text-primary);
}
.submit-btn { padding: 12px 40px; }
.btn-primary { background: var(--primary); color: #fff; border-radius: var(--radius); }
.btn-primary:hover { background: var(--primary-dark); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }
.history-section { margin-top: 40px; }
.section-title { font-size: 18px; font-weight: 600; margin-bottom: 16px; }
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: var(--bg-white);
  border-radius: 6px;
  margin-bottom: 8px;
  box-shadow: var(--shadow-sm);
}
.item-info { display: flex; gap: 16px; }
.item-title { font-weight: 500; }
.item-time { color: var(--text-secondary); font-size: 13px; }
.item-status { font-size: 13px; padding: 2px 10px; border-radius: 4px; }
.item-status.pending { background: #fdf6ec; color: #e6a23c; }
.item-status.published { background: #f0f9eb; color: #67c23a; }
.item-status.rejected { background: #fef0f0; color: #f56c6c; }
.item-status.unpublished { background: #f4f4f5; color: #909399; }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .upload-page { padding: 16px 0; }
  .card { padding: 16px; border-radius: 6px; }
  .form-group input[type="text"],
  .form-group select,
  .form-group textarea {
    font-size: 16px; /* prevent iOS zoom */
  }
  .cover-preview img { max-width: 100%; }
  .submit-btn { width: 100%; }
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 6px;
    padding: 10px 12px;
  }
  .item-info { gap: 8px; flex-wrap: wrap; }
}
</style>
