<template>
  <div class="skeleton-card" v-for="n in count" :key="n">
    <div class="sk-cover"></div>
    <div class="sk-body">
      <div class="sk-line sk-title"></div>
      <div class="sk-line sk-text"></div>
      <div class="sk-line sk-text short"></div>
    </div>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ count?: number }>(), { count: 4 })
</script>

<style scoped>
.skeleton-card {
  background: var(--bg-white);
  border-radius: var(--radius);
  overflow: hidden;
  border: 1px solid var(--border-color);
}
.sk-cover {
  width: 100%;
  height: 160px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.sk-body { padding: 12px 16px; }
.sk-line {
  height: 14px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e8e8e8 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 8px;
}
.sk-title { width: 70%; height: 16px; }
.sk-text { width: 100%; }
.sk-text.short { width: 50%; }
@keyframes shimmer { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .sk-cover { height: 120px; }
  .sk-body { padding: 10px 12px; }
}
</style>
