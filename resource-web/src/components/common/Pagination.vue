<template>
  <div class="pagination" v-if="total > 0">
    <button class="page-btn" :disabled="page <= 1" @click="$emit('change', page - 1)">上一页</button>
    <template v-for="p in displayedPages" :key="p">
      <span v-if="p === '...'" class="page-ellipsis">...</span>
      <button v-else class="page-btn" :class="{ active: p === page }" @click="$emit('change', p as number)">{{ p }}</button>
    </template>
    <button class="page-btn" :disabled="page >= totalPages" @click="$emit('change', page + 1)">下一页</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{ total: number; page: number; pageSize: number }>()
defineEmits<{ change: [page: number] }>()

const totalPages = computed(() => Math.ceil(props.total / props.pageSize))

const displayedPages = computed(() => {
  const pages: (number | string)[] = []
  const tp = totalPages.value
  const cp = props.page
  if (tp <= 7) {
    for (let i = 1; i <= tp; i++) pages.push(i)
  } else {
    pages.push(1)
    if (cp > 3) pages.push('...')
    const start = Math.max(2, cp - 1)
    const end = Math.min(tp - 1, cp + 1)
    for (let i = start; i <= end; i++) pages.push(i)
    if (cp < tp - 2) pages.push('...')
    pages.push(tp)
  }
  return pages
})
</script>

<style scoped>
.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  margin-top: 32px;
}
.page-btn {
  min-width: 36px;
  height: 36px;
  padding: 0 10px;
  border-radius: 6px;
  font-size: 14px;
  background: var(--bg-white);
  color: var(--text-regular);
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}
.page-btn:hover:not(:disabled) { color: var(--primary); border-color: var(--primary); }
.page-btn.active { background: var(--primary); color: #fff; border-color: var(--primary); }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
.page-ellipsis { padding: 0 4px; color: var(--text-secondary); }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .pagination { gap: 4px; margin-top: 24px; flex-wrap: wrap; }
  .page-btn {
    min-width: 32px;
    height: 32px;
    padding: 0 6px;
    font-size: 13px;
  }
}
</style>
