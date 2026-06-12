<template>
  <div class="detail-page container" v-if="resource">
    <div class="detail-header">
      <div class="detail-info">
        <span class="detail-category">{{ resource.category_name }}</span>
        <h1 class="detail-title">{{ resource.title }}</h1>
        <p class="detail-summary">{{ resource.summary }}</p>
        <div class="detail-meta">
          <span>文件大小: {{ formatSize(resource.file_size) }}</span>
          <span>上传时间: {{ formatDate(resource.upload_time) }}</span>
          <span>浏览: {{ resource.view_count }}</span>
          <span>收藏: {{ resource.favorite_count }}</span>
        </div>
        <div class="detail-tags" v-if="resource.tags">
          <span class="tag" v-for="tag in resource.tags.split(',')" :key="tag">{{ tag.trim() }}</span>
        </div>
        <div class="detail-link-section">
          <div class="link-row" v-if="resource.link">
            <label>下载链接：</label>
            <a :href="resource.link" target="_blank" rel="noopener noreferrer" class="link-url">{{ resource.link }}</a>
          </div>
          <div class="link-row" v-if="resource.link_password">
            <label>提取码：</label>
            <span class="link-password">{{ resource.link_password }}</span>
            <button class="btn-copy" @click="copyPassword">复制</button>
          </div>
        </div>
        <div class="detail-actions">
          <a
            v-if="resource.link"
            :href="resource.link"
            target="_blank"
            rel="noopener noreferrer"
            class="btn btn-primary"
          >前往下载</a>
          <button
            class="btn"
            :class="isFavorited ? 'btn-favorited' : 'btn-outline'"
            @click="toggleFavorite"
          >{{ isFavorited ? '已收藏' : '收藏' }}</button>
        </div>
      </div>
    </div>

    <section class="related-section" v-if="related.length">
      <h2 class="section-title">相关资源</h2>
      <ResourceGrid :resources="related" @cardClick="goDetail" />
    </section>
  </div>
  <div v-else class="container" style="padding:60px 20px; text-align:center;">
    <EmptyState text="资源不存在或已下架" />
    <router-link to="/">返回首页</router-link>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ResourceGrid from '../components/resource/ResourceGrid.vue'
import EmptyState from '../components/common/EmptyState.vue'
import { resourceApi } from '../api/resource'
import { useUserStore } from '../store/user'
import { formatSize, formatDate } from '../utils/format'
import type { Resource } from '../types/resource'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const resource = ref<Resource | null>(null)
const related = ref<Resource[]>([])
const isFavorited = ref(false)

function goDetail(r: Resource) {
  router.push(`/resource/${r.id}`)
}

function copyPassword() {
  if (resource.value?.link_password) {
    navigator.clipboard.writeText(resource.value.link_password)
  }
}

async function toggleFavorite() {
  if (!userStore.isLoggedIn) {
    router.push({ name: 'login', query: { redirect: route.fullPath } })
    return
  }
  if (!resource.value) return
  try {
    const fn = isFavorited.value ? resourceApi.unfavorite : resourceApi.favorite
    await fn(resource.value.id)
    isFavorited.value = !isFavorited.value
    resource.value.favorite_count += isFavorited.value ? 1 : -1
  } catch (e) {
    alert((e as Error).message)
  }
}

onMounted(async () => {
  const id = Number(route.params.id)
  try {
    const res = await resourceApi.get(id)
    resource.value = res.data.data
    if (resource.value) {
      const relRes = await resourceApi.list({ category_id: resource.value.category_id, page: 1, page_size: 6 })
      related.value = (relRes.data.data?.items || []).filter((r) => r.id !== id)
    }
  } catch {
    resource.value = null
  }
})
</script>

<style scoped>
.detail-page { padding: 30px 20px; }
.detail-header {
  display: flex;
  gap: 32px;
  background: var(--bg-white);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow-sm);
}
.detail-info { flex: 1; }
.detail-category {
  display: inline-block;
  padding: 2px 10px;
  background: rgba(64,158,255,0.1);
  color: var(--primary);
  border-radius: 4px;
  font-size: 13px;
  margin-bottom: 12px;
}
.detail-title { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
.detail-summary { color: var(--text-regular); line-height: 1.8; margin-bottom: 16px; }
.detail-meta {
  display: flex;
  gap: 20px;
  font-size: 13px;
  color: var(--text-secondary);
  margin-bottom: 16px;
}
.detail-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.tag {
  padding: 2px 10px;
  background: var(--bg-page);
  border-radius: 4px;
  font-size: 12px;
  color: var(--text-secondary);
}
.detail-link-section {
  background: var(--bg-page);
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}
.link-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.link-row:last-child { margin-bottom: 0; }
.link-row label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  white-space: nowrap;
}
.link-url {
  color: var(--primary);
  word-break: break-all;
  font-size: 14px;
}
.link-password {
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
  color: var(--text-primary);
}
.btn-copy {
  padding: 2px 10px;
  font-size: 13px;
  background: var(--primary);
  color: #fff;
  border-radius: 4px;
}
.btn-copy:hover { opacity: 0.9; }
.detail-actions { display: flex; gap: 12px; }
.btn {
  padding: 10px 28px;
  border-radius: var(--radius);
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
  text-align: center;
  text-decoration: none;
}
.btn-primary { background: var(--primary); color: #fff; }
.btn-primary:hover { background: var(--primary-dark); }
.btn-outline { border: 1px solid var(--primary); color: var(--primary); background: var(--bg-white); }
.btn-outline:hover { background: rgba(64,158,255,0.05); }
.btn-favorited { background: #f56c6c; color: #fff; }
.btn-favorited:hover { background: #e45656; }
.related-section { margin-top: 48px; }
.section-title { font-size: 20px; font-weight: 600; margin-bottom: 20px; }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .detail-page { padding: 16px 0; }
  .detail-header {
    flex-direction: column;
    gap: 16px;
    padding: 16px;
  }
  .detail-title { font-size: 20px; margin-bottom: 8px; }
  .detail-meta {
    flex-wrap: wrap;
    gap: 8px 16px;
  }
  .detail-actions {
    flex-direction: column;
  }
  .btn { width: 100%; }
  .related-section { margin-top: 32px; }
  .section-title { font-size: 17px; }
  .link-row { flex-wrap: wrap; }
}
</style>
