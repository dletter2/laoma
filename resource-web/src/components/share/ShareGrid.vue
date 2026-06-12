<template>
  <section class="share-section" v-if="shares.length">
    <h2 class="section-title">工具导航</h2>
    <div class="share-grid">
      <a
        v-for="item in shares"
        :key="item.id"
        :href="item.url"
        target="_blank"
        rel="noopener noreferrer"
        class="share-card"
      >
        <el-avatar :size="48" :src="item.avatar_url" v-if="item.avatar_url">
          <img src="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><rect fill='%23ddd' width='100' height='100'/><text x='50' y='55' text-anchor='middle' font-size='40' fill='%23999'>?</text></svg>" />
        </el-avatar>
        <el-avatar :size="48" v-else>{{ item.name?.charAt(0) }}</el-avatar>
        <div class="share-info">
          <div class="share-name">{{ item.name }}</div>
          <div class="share-desc" v-if="item.description">{{ item.description }}</div>
        </div>
      </a>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { shareApi, type Share } from '../../api/share'

const shares = ref<Share[]>([])

onMounted(async () => {
  try {
    const res = await shareApi.list()
    shares.value = res.data.data || []
  } catch {
    // silently ignore
  }
})
</script>

<style scoped>
.share-section { padding: 40px 20px 0; }
.section-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}
.share-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}
.share-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 16px;
  border-radius: 12px;
  background: #fff;
  border: 1px solid #ebeef5;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s, transform 0.2s;
}
.share-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}
.share-info { flex: 1; min-width: 0; }
.share-name {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 4px;
}
.share-desc {
  font-size: 13px;
  color: #909399;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

@media (max-width: 768px) {
  .share-section { padding: 24px 0 0; }
  .section-title { font-size: 18px; margin-bottom: 16px; }
  .share-grid { grid-template-columns: 1fr; }
}
</style>
