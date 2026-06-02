<template>
  <div class="favorites-page container">
    <h1 class="page-title">我的收藏</h1>
    <div v-if="loading" class="resource-grid"><SkeletonCard :count="4" /></div>
    <template v-else>
      <ResourceGrid v-if="resources.length" :resources="resources" @cardClick="goDetail" />
      <EmptyState v-else text="暂无收藏资源">
        <template #action>
          <router-link to="/category" class="browse-link">去浏览资源</router-link>
        </template>
      </EmptyState>
    </template>
    <Pagination
      v-if="total > pageSize"
      :total="total"
      :page="page"
      :pageSize="pageSize"
      @change="changePage"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ResourceGrid from '../components/resource/ResourceGrid.vue'
import SkeletonCard from '../components/common/SkeletonCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import Pagination from '../components/common/Pagination.vue'
import { resourceApi } from '../api/resource'
import type { Resource } from '../types/resource'

const router = useRouter()
const resources = ref<Resource[]>([])
const loading = ref(true)
const page = ref(1)
const pageSize = 12
const total = ref(0)

function goDetail(r: Resource) { router.push(`/resource/${r.id}`) }

function changePage(p: number) { page.value = p; loadFavorites() }

async function loadFavorites() {
  loading.value = true
  try {
    const res = await resourceApi.favorites({ page: page.value, page_size: pageSize })
    resources.value = res.data.data?.items || []
    total.value = res.data.data?.total || 0
  } finally {
    loading.value = false
  }
}

onMounted(() => loadFavorites())
</script>

<style scoped>
.favorites-page { padding: 30px 20px; }
.browse-link {
  display: inline-block;
  margin-top: 12px;
  padding: 8px 24px;
  background: var(--primary);
  color: #fff;
  border-radius: var(--radius);
}
.browse-link:hover { background: var(--primary-dark); color: #fff; }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .favorites-page { padding: 16px 0; }
}
</style>
