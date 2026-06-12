<template>
  <div class="category-filter">
    <button
      v-for="cat in categories"
      :key="cat.id"
      class="cat-btn"
      :class="{ active: modelValue === cat.id }"
      @click="$emit('update:modelValue', cat.id)"
    >{{ cat.name }}</button>
  </div>
</template>

<script setup lang="ts">
import type { Category } from '../types/api'

defineProps<{
  categories: Category[]
  modelValue: number | null
}>()
defineEmits<{ 'update:modelValue': [value: number | null] }>()
</script>

<style scoped>
.category-filter {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}
.cat-btn {
  padding: 6px 18px;
  border-radius: 20px;
  font-size: 14px;
  background: var(--bg-white);
  color: var(--text-regular);
  border: 1px solid var(--border-color);
  transition: all 0.2s;
}
.cat-btn:hover { border-color: var(--primary); color: var(--primary); }
.cat-btn.active {
  background: var(--primary);
  color: #fff;
  border-color: var(--primary);
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .category-filter { gap: 6px; }
  .cat-btn { padding: 5px 12px; font-size: 13px; }
}
</style>
