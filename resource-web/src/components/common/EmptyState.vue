<template>
  <div class="empty-state">
    <div class="empty-icon">
      <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#c0c4cc" stroke-width="1.5">
        <path d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4"/>
      </svg>
    </div>
    <p class="empty-text">{{ text }}</p>
    <button v-if="showReset" class="reset-btn" @click="$emit('reset')">重置筛选</button>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ text?: string; showReset?: boolean }>(), {
  text: '暂无符合条件的资源',
  showReset: false,
})
defineEmits<{ reset: [] }>()
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 60px 20px;
}
.empty-icon { margin-bottom: 16px; }
.empty-text { color: var(--text-secondary); font-size: 15px; margin-bottom: 16px; }
.reset-btn {
  padding: 8px 24px;
  background: var(--primary);
  color: #fff;
  border-radius: var(--radius);
  font-size: 14px;
  transition: background 0.2s;
}
.reset-btn:hover { background: var(--primary-dark); }
</style>
