<template>
  <div class="category-page container">
    <!-- Search -->
    <div class="search-section">
      <SearchBox @search="handleSearch" />
    </div>

    <!-- Filter tabs -->
    <div class="filter-tabs">
      <button
        v-for="tab in tabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeTab === tab.key }"
        @click="switchTab(tab.key)"
      >{{ tab.label }}</button>
    </div>

    <!-- Category selector -->
    <CategoryFilter
      v-if="activeTab === 'category'"
      v-model="selectedCategory"
      :categories="categories"
    />

    <!-- Resource list -->
    <div v-if="loading" class="resource-grid"><SkeletonCard :count="8" /></div>
    <template v-else>
      <ResourceGrid v-if="resources.length" :resources="resources" @cardClick="goDetail" />
      <EmptyState v-else :showReset="true" @reset="resetFilter" />
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
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import SearchBox from '../components/search/SearchBox.vue'
import ResourceGrid from '../components/resource/ResourceGrid.vue'
import SkeletonCard from '../components/common/SkeletonCard.vue'
import EmptyState from '../components/common/EmptyState.vue'
import Pagination from '../components/common/Pagination.vue'
import CategoryFilter from '../components/CategoryFilter.vue'
import { resourceApi } from '../api/resource'
import { categoryApi } from '../api/category'
import type { Resource } from '../types/resource'
import type { Category } from '../types/api'

const route = useRoute()
const router = useRouter()

const tabs = [
  { key: 'hot', label: '热门资源' },
  { key: 'latest', label: '最新上传' },
  { key: 'category', label: '分类筛选' },
]

const resources = ref<Resource[]>([])
const categories = ref<Category[]>([])
const loading = ref(true)
const activeTab = ref('hot')
const selectedCategory = ref<number | null>(null)
const page = ref(1)
const pageSize = 12
const total = ref(0)
const searchQuery = ref('')

function switchTab(key: string) {
  activeTab.value = key
  page.value = 1
  if (key !== 'category') selectedCategory.value = null
  loadData()
}

function handleSearch(q: string) {
  searchQuery.value = q
  page.value = 1
  loadData()
}

function resetFilter() {
  searchQuery.value = ''
  selectedCategory.value = null
  activeTab.value = 'hot'
  loadData()
}

function changePage(p: number) {
  page.value = p
  loadData()
}

function goDetail(r: Resource) {
  router.push(`/resource/${r.id}`)
}

async function loadData() {
  loading.value = true
  try {
    const params: Record<string, unknown> = { page: page.value, page_size: pageSize }
    if (searchQuery.value) {
      const res = await resourceApi.search({ q: searchQuery.value, ...params })
      resources.value = res.data.data?.items || []
      total.value = res.data.data?.total || 0
    } else {
      params.sort = activeTab.value === 'latest' ? 'latest' : 'hot'
      if (activeTab.value === 'category' && selectedCategory.value) {
        params.category_id = selectedCategory.value
      }
      const res = await resourceApi.list(params)
      resources.value = res.data.data?.items || []
      total.value = res.data.data?.total || 0
    }
  } finally {
    loading.value = false
  }
}

watch(selectedCategory, () => {
  page.value = 1
  loadData()
})

onMounted(async () => {
  if (route.query.q) {
    searchQuery.value = route.query.q as string
  }
  const catRes = await categoryApi.list()
  categories.value = catRes.data.data || []
  await loadData()
})
</script>

<style scoped>
.category-page { padding: 30px 20px; }
.search-section { max-width: 640px; margin: 0 auto 24px; }
.filter-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  border-bottom: 2px solid var(--border-color);
}
.tab-btn {
  padding: 10px 24px;
  font-size: 15px;
  background: none;
  color: var(--text-regular);
  border-bottom: 2px solid transparent;
  margin-bottom: -2px;
  transition: all 0.2s;
}
.tab-btn:hover { color: var(--primary); }
.tab-btn.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
  font-weight: 600;
}

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .category-page { padding: 16px 0; }
  .search-section { margin: 0 0 16px; }
  .filter-tabs { gap: 0; }
  .tab-btn {
    flex: 1;
    padding: 10px 8px;
    font-size: 14px;
    text-align: center;
  }
}
</style>
