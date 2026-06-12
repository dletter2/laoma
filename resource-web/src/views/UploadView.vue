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
        <label>分享链接 <span class="required">*</span></label>
        <input v-model="form.link" type="text" placeholder="请输入网盘分享链接" />
      </div>
      <div class="form-group">
        <label>提取码</label>
        <input v-model="form.link_password" type="text" placeholder="请输入提取码（如有）" class="input-short" />
      </div>
      <div class="form-group">
        <label>文件大小 <span class="required">*</span></label>
        <div class="size-input-row">
          <input v-model.number="form.file_size" type="number" min="0" placeholder="文件大小" />
          <select v-model="sizeUnit" class="size-unit">
            <option value="1">B</option>
            <option value="1024">KB</option>
            <option value="1048576">MB</option>
            <option value="1073741824">GB</option>
          </select>
        </div>
      </div>
      <button class="btn btn-primary submit-btn" :disabled="submitting" @click="handleSubmit">
        {{ submitting ? '提交中...' : '提交资源' }}
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
import { formatDate } from '../utils/format'
import type { Category } from '../types/api'
import type { Resource } from '../types/resource'

const categories = ref<Category[]>([])
const submitting = ref(false)
const myResources = ref<Resource[]>([])
const loadingHistory = ref(false)
const sizeUnit = ref('1048576')

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
  link: '',
  link_password: '',
  file_size: '' as number | string,
})

async function handleSubmit() {
  if (!form.value.title || !form.value.category_id || !form.value.summary || !form.value.link) {
    alert('请填写所有必填字段')
    return
  }
  const fileSizeBytes = Number(form.value.file_size) * Number(sizeUnit.value)
  submitting.value = true
  try {
    await resourceApi.create({
      title: form.value.title,
      summary: form.value.summary,
      category_id: Number(form.value.category_id),
      tags: form.value.tags,
      link: form.value.link,
      link_password: form.value.link_password,
      file_size: fileSizeBytes || 0,
    })
    alert('资源提交成功，等待审核！')
    form.value = { title: '', category_id: '', tags: '', summary: '', link: '', link_password: '', file_size: '' }
    loadHistory()
  } catch (e) {
    alert((e as Error).message)
  } finally {
    submitting.value = false
  }
}

async function loadHistory() {
  loadingHistory.value = true
  try {
    const res = await resourceApi.my({ page: 1, page_size: 20 })
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
.form-group input[type="number"],
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
.input-short { max-width: 200px; }
.size-input-row { display: flex; gap: 8px; align-items: center; }
.size-input-row input { flex: 1; }
.size-input-row .size-unit {
  width: 80px;
  flex-shrink: 0;
  padding: 10px 8px;
  border: 1px solid var(--border-color);
  border-radius: 6px;
  font-size: 14px;
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
  .form-group input[type="number"],
  .form-group select,
  .form-group textarea {
    font-size: 16px;
  }
  .input-short { max-width: 100%; }
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
