<template>
  <div class="share-manage">
    <div class="page-header">
      <h2>分享管理</h2>
      <el-button type="primary" @click="openDialog()">新增分享</el-button>
    </div>

    <el-table :data="shares" v-loading="loading" stripe>
      <el-table-column label="头像" width="80">
        <template #default="{ row }">
          <el-avatar :size="40" :src="row.avatar_url" v-if="row.avatar_url">
            <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%23ddd' width='100' height='100'/><text x='50' y='55' text-anchor='middle' font-size='40' fill='%23999'>?</text></svg>" />
          </el-avatar>
          <el-avatar :size="40" v-else>{{ row.name?.charAt(0) }}</el-avatar>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="名称" min-width="120" />
      <el-table-column prop="url" label="链接" min-width="200" show-overflow-tooltip />
      <el-table-column prop="description" label="介绍" min-width="180" show-overflow-tooltip />
      <el-table-column prop="sort_order" label="排序" width="80" align="center" />
      <el-table-column label="操作" width="160" fixed="right">
        <template #default="{ row }">
          <el-button text type="primary" size="small" @click="openDialog(row)">编辑</el-button>
          <el-button text type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑分享' : '新增分享'" width="520px" destroy-on-close>
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入名称" />
        </el-form-item>
        <el-form-item label="链接" prop="url">
          <el-input v-model="form.url" placeholder="请输入链接地址" />
        </el-form-item>
        <el-form-item label="头像URL">
          <el-input v-model="form.avatar_url" placeholder="请输入头像图片链接" />
        </el-form-item>
        <el-form-item label="介绍">
          <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入介绍" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" :max="9999" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { shareApi, type Share, type ShareForm } from '../api/share'

const shares = ref<Share[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const submitting = ref(false)
const isEdit = ref(false)
const editId = ref<number>(0)
const formRef = ref<FormInstance>()

const form = reactive<ShareForm>({
  name: '',
  url: '',
  avatar_url: '',
  description: '',
  sort_order: 0,
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  url: [{ required: true, message: '请输入链接', trigger: 'blur' }],
}

async function fetchList() {
  loading.value = true
  try {
    const res = await shareApi.list()
    shares.value = res.data.data || []
  } finally {
    loading.value = false
  }
}

function openDialog(row?: Share) {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.name = row.name
    form.url = row.url
    form.avatar_url = row.avatar_url
    form.description = row.description
    form.sort_order = row.sort_order
  } else {
    isEdit.value = false
    editId.value = 0
    form.name = ''
    form.url = ''
    form.avatar_url = ''
    form.description = ''
    form.sort_order = 0
  }
  dialogVisible.value = true
}

async function handleSubmit() {
  await formRef.value?.validate()
  submitting.value = true
  try {
    if (isEdit.value) {
      await shareApi.update(editId.value, form)
      ElMessage.success('更新成功')
    } else {
      await shareApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    await fetchList()
  } finally {
    submitting.value = false
  }
}

async function handleDelete(row: Share) {
  await ElMessageBox.confirm(`确定删除"${row.name}"吗？`, '提示', { type: 'warning' })
  await shareApi.delete(row.id)
  ElMessage.success('删除成功')
  await fetchList()
}

onMounted(fetchList)
</script>

<style scoped>
.share-manage { padding: 20px; }
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.page-header h2 { font-size: 18px; font-weight: 600; margin: 0; }
</style>
