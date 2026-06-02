<template>
  <div class="home-page">
    <!-- Hero search section -->
    <section class="hero-section">
      <h1 class="hero-title">发现优质资源</h1>
      <p class="hero-desc">搜索并分享各类学习资源、工具和素材</p>
      <SearchBox ref="searchBoxRef" @search="handleSearch" />
    </section>

    <!-- Hot resources -->
    <section class="hot-section container">
      <h2 class="section-title">热门资源</h2>
      <div v-if="loading" class="resource-grid"><SkeletonCard :count="4" /></div>
      <ResourceGrid v-else-if="resources.length" :resources="resources" @cardClick="goDetail" />
      <EmptyState v-else text="暂无热门资源" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SearchBox from '../components/search/SearchBox.vue'
import ResourceGrid from '../components/resource/ResourceGrid.vue'
import SkeletonCard from '../components/common/SkeletonCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { resourceApi } from '../api/resource'
import type { Resource } from '../types/resource'

const router = useRouter()
const searchBoxRef = ref<InstanceType<typeof SearchBox>>()
const resources = ref<Resource[]>([])
const loading = ref(true)

function handleSearch(q: string) {
  router.push({ path: '/category', query: { q } })
}

function goDetail(r: Resource) {
  router.push(`/resource/${r.id}`)
}

onMounted(async () => {
  try {
    const res = await resourceApi.list({ sort: 'hot', page: 1, page_size: 8 })
    resources.value = res.data.data?.items || []
  } finally {
    loading.value = false
  }
})

function focus() {
  searchBoxRef.value?.focus()
}
defineExpose({ focus })
</script>

<style scoped>
.hero-section {
  text-align: center;
  padding: 80px 20px 60px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}
.hero-title { font-size: 36px; font-weight: 700; margin-bottom: 12px; }
.hero-desc { font-size: 16px; opacity: 0.9; margin-bottom: 32px; }
.hero-section :deep(.search-input) {
  border-color: rgba(255,255,255,0.3);
  background: rgba(255,255,255,0.15);
  color: #fff;
}
.hero-section :deep(.search-input::placeholder) { color: rgba(255,255,255,0.7); }
.hero-section :deep(.search-input:focus) { border-color: #fff; background: rgba(255,255,255,0.25); }
.hero-section :deep(.search-btn) { background: #fff; color: #764ba2; }
.hot-section { padding: 40px 20px 0; }
.section-title {
  font-size: 22px;
  font-weight: 600;
  margin-bottom: 24px;
  color: var(--text-primary);
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .hero-section {
    padding: 48px 16px 36px;
  }
  .hero-title { font-size: 24px; margin-bottom: 8px; }
  .hero-desc { font-size: 14px; margin-bottom: 20px; }
  .hero-section :deep(.search-input) { height: 42px; padding: 0 14px; font-size: 14px; }
  .hero-section :deep(.search-btn) { padding: 0 20px; font-size: 14px; }
  .hot-section { padding: 24px 0 0; }
  .section-title { font-size: 18px; margin-bottom: 16px; }
}
</style>
