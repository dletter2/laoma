<template>
  <div class="resource-grid">
    <ResourceCard
      v-for="r in resources"
      :key="r.id"
      :resource="r"
      @click="$emit('cardClick', r)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Resource } from '../../types/resource'
import ResourceCard from './ResourceCard.vue'

defineProps<{ resources: Resource[] }>()
defineEmits<{ cardClick: [resource: Resource] }>()
</script>

<style scoped>
.resource-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}
@media (max-width: 1024px) {
  .resource-grid { grid-template-columns: repeat(3, 1fr); }
}
@media (max-width: 768px) {
  .resource-grid { grid-template-columns: repeat(2, 1fr); gap: 12px; }
}
@media (max-width: 480px) {
  .resource-grid { grid-template-columns: 1fr; gap: 12px; }
}
</style>
