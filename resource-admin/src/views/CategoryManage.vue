<template>
  <div class="category-manage">
    <div class="toolbar">
      <el-button type="primary" @click="openDialog()">新增分类</el-button>
    </div>
    <el-table :data="categories" stripe v-loading="loading">
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="name" label="分类名称" />
      <el-table-column prop="sort_order" label="排序" width="80" />
      <el-table-column prop="resource_count" label="资源数" width="100" />
      <el-table-column label="操作" width="160">
        <template #default="{ row }">
          <el-button size="small" @click="openDialog(row)">编辑</el-button>
          <el-popconfirm title="确定删除此分类？" @confirm="handleDelete(row.id)">
            <template #reference>
              <el-button size="small" type="danger">删除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑分类' : '新增分类'" width="400px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="名称">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="排序">
          <el-input-number v-model="form.sort_order" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { categoryApi } from '../api/category'
import type { Category } from '../types'

const categories = ref<Category[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const editingId = ref<number | null>(null)
const form = reactive({ name: '', sort_order: 0 })

async function loadData() {
  loading.value = true
  try {
    const res = await categoryApi.list()
    categories.value = res.data.data || []
  } finally {
    loading.value = false
  }
}

function openDialog(cat?: Category) {
  if (cat) {
    editingId.value = cat.id
    form.name = cat.name
    form.sort_order = cat.sort_order
  } else {
    editingId.value = null
    form.name = ''
    form.sort_order = 0
  }
  dialogVisible.value = true
}

async function handleSave() {
  try {
    if (editingId.value) {
      await categoryApi.update(editingId.value, { name: form.name, sort_order: form.sort_order })
    } else {
      await categoryApi.create({ name: form.name, sort_order: form.sort_order })
    }
    ElMessage.success('保存成功')
    dialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error((e as Error).message)
  }
}

async function handleDelete(id: number) {
  try {
    await categoryApi.delete(id)
    ElMessage.success('删除成功')
    loadData()
  } catch (e) {
    ElMessage.error((e as Error).message)
  }
}

onMounted(() => loadData())
</script>
