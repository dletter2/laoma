<template>
  <div class="search-box" ref="boxRef">
    <input
      ref="inputRef"
      v-model="keyword"
      class="search-input"
      :placeholder="placeholder"
      @keyup.enter="handleSearch"
      @focus="showHistory = true"
    />
    <button class="search-btn" @click="handleSearch">搜索</button>
    <div v-if="showHistory && history.length" class="search-history">
      <div class="history-header">
        <span>搜索历史</span>
        <button @click="clearHistory">清空</button>
      </div>
      <div
        v-for="h in history"
        :key="h"
        class="history-item"
        @click="selectHistory(h)"
      >{{ h }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { getSearchHistory, addSearchHistory, clearSearchHistory } from '../../utils/storage'

const props = withDefaults(defineProps<{ placeholder?: string }>(), { placeholder: '输入资源名称或关键词搜索' })
const emit = defineEmits<{ search: [keyword: string] }>()

const keyword = ref('')
const history = ref<string[]>([])
const showHistory = ref(false)
const inputRef = ref<HTMLInputElement>()
const boxRef = ref<HTMLElement>()

function handleSearch() {
  const q = keyword.value.trim()
  if (!q) return
  addSearchHistory(q)
  history.value = getSearchHistory()
  showHistory.value = false
  emit('search', q)
}

function selectHistory(h: string) {
  keyword.value = h
  handleSearch()
}

function clearHistory() {
  clearSearchHistory()
  history.value = []
}

function handleClickOutside(e: MouseEvent) {
  if (boxRef.value && !boxRef.value.contains(e.target as Node)) {
    showHistory.value = false
  }
}

function focus() {
  inputRef.value?.focus()
}

defineExpose({ focus })

onMounted(() => {
  history.value = getSearchHistory()
  document.addEventListener('click', handleClickOutside)
})
onUnmounted(() => document.removeEventListener('click', handleClickOutside))
</script>

<style scoped>
.search-box {
  position: relative;
  display: flex;
  max-width: 640px;
  margin: 0 auto;
}
.search-input {
  flex: 1;
  height: 48px;
  padding: 0 20px;
  font-size: 16px;
  border: 2px solid var(--border-color);
  border-right: none;
  border-radius: var(--radius) 0 0 var(--radius);
  transition: border-color 0.2s;
}
.search-input:focus { border-color: var(--primary); }
.search-btn {
  padding: 0 32px;
  background: var(--primary);
  color: #fff;
  font-size: 16px;
  border-radius: 0 var(--radius) var(--radius) 0;
  transition: background 0.2s;
}
.search-btn:hover { background: var(--primary-dark); }
.search-history {
  position: absolute;
  top: 52px;
  left: 0;
  right: 0;
  background: var(--bg-white);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  z-index: 10;
  padding: 8px 0;
}
.history-header {
  display: flex;
  justify-content: space-between;
  padding: 8px 16px;
  font-size: 13px;
  color: var(--text-secondary);
}
.history-header button { background: none; color: var(--text-secondary); font-size: 13px; }
.history-item {
  padding: 8px 16px;
  cursor: pointer;
  font-size: 14px;
  color: var(--text-regular);
  transition: background 0.15s;
}
.history-item:hover { background: var(--bg-page); }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .search-input {
    height: 42px;
    padding: 0 14px;
    font-size: 14px;
  }
  .search-btn {
    padding: 0 20px;
    font-size: 14px;
  }
  .search-history {
    left: -12px;
    right: -12px;
    top: 46px;
    border-radius: 0 0 var(--radius) var(--radius);
  }
}
</style>
