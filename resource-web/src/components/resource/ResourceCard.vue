<template>
  <div class="resource-card" @click="$emit('click')">
    <div class="card-body">
      <h3 class="card-title">{{ resource.title }}</h3>
      <p class="card-summary">{{ resource.summary }}</p>
      <div class="card-meta">
        <span v-if="resource.category_name" class="meta-category">{{ resource.category_name }}</span>
        <span class="meta-size">{{ formatSize(resource.file_size) }}</span>
        <span v-if="resource.uploader_nickname" class="meta-uploader">{{ resource.uploader_nickname }}</span>
        <span class="meta-time">{{ timeAgo(resource.upload_time) }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Resource } from '../../types/resource'
import { formatSize, timeAgo } from '../../utils/format'

defineProps<{ resource: Resource }>()
defineEmits<{ click: [] }>()
</script>

<style scoped>
.resource-card {
  background: var(--bg-white);
  border-radius: var(--radius);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  border: 1px solid var(--border-color);
}
.resource-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
}
.card-body { padding: 16px; }
.card-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 6px;
}
.card-summary {
  font-size: 13px;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  margin-bottom: 8px;
}
.card-meta {
  display: flex;
  gap: 12px;
  font-size: 12px;
  color: var(--text-secondary);
}
.meta-category {
  color: var(--primary);
  background: rgba(64, 158, 255, 0.1);
  padding: 1px 6px;
  border-radius: 3px;
}
.meta-uploader {
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .resource-card {
    border-radius: 6px;
  }
  .card-body { padding: 12px; }
  .card-title { font-size: 14px; margin-bottom: 4px; }
  .card-summary { font-size: 12px; margin-bottom: 6px; }
  .card-meta { gap: 8px; font-size: 11px; }
}
</style>
