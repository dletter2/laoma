<template>
  <AppHeader ref="headerRef" @focusSearch="handleFocusSearch" />
  <main class="main-content">
    <router-view />
  </main>
  <AppFooter />
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import { useUserStore } from './store/user'

const userStore = useUserStore()
const headerRef = ref<InstanceType<typeof AppHeader>>()

function handleFocusSearch() {
  headerRef.value?.focus()
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
  min-height: calc(100vh - 64px - 80px);
}
</style>
