<template>
  <AppHeader @focusSearch="handleFocusSearch" />
  <main class="main-content">
    <router-view />
  </main>
  <AppFooter />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import { useUserStore } from './store/user'

const userStore = useUserStore()
const router = useRouter()

function handleFocusSearch() {
  router.push({ path: '/', query: { focusSearch: '1' } })
}

onMounted(() => {
  userStore.init()
})
</script>

<style>
@import './assets/styles/global.css';
</style>

<style scoped>
.main-content {
  min-height: calc(100vh - 64px - 260px);
}
</style>
