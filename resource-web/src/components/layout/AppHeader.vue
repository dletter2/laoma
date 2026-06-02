<template>
  <header class="app-header">
    <div class="header-inner container">
      <router-link to="/" class="logo">
        <span class="logo-text">资源分享站</span>
      </router-link>

      <!-- Desktop nav -->
      <nav class="nav-links">
        <router-link to="/" :class="{ active: route.path === '/' }">首页</router-link>
        <router-link to="/category" :class="{ active: route.path === '/category' }">资源分类</router-link>
        <router-link to="/upload" :class="{ active: route.path === '/upload' }">上传中心</router-link>
        <router-link to="/favorites" :class="{ active: route.path === '/favorites' }">我的收藏</router-link>
      </nav>

      <!-- Desktop right -->
      <div class="header-right">
        <button class="search-btn" @click="$emit('focusSearch')" title="搜索">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        </button>
        <template v-if="userStore.isLoggedIn">
          <span class="username">{{ userStore.user?.username }}</span>
          <button class="logout-btn" @click="handleLogout">退出</button>
        </template>
        <template v-else>
          <router-link to="/login" class="login-link">登录</router-link>
        </template>
      </div>

      <!-- Mobile hamburger -->
      <button class="hamburger-btn" @click="mobileMenuOpen = !mobileMenuOpen" :class="{ open: mobileMenuOpen }">
        <span></span><span></span><span></span>
      </button>
    </div>

    <!-- Mobile dropdown menu -->
    <transition name="slide">
      <div v-if="mobileMenuOpen" class="mobile-menu container">
        <nav class="mobile-nav">
          <router-link to="/" @click="mobileMenuOpen = false">首页</router-link>
          <router-link to="/category" @click="mobileMenuOpen = false">资源分类</router-link>
          <router-link to="/upload" @click="mobileMenuOpen = false">上传中心</router-link>
          <router-link to="/favorites" @click="mobileMenuOpen = false">我的收藏</router-link>
        </nav>
        <div class="mobile-actions">
          <button class="mobile-search-btn" @click="$emit('focusSearch'); mobileMenuOpen = false">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
            搜索
          </button>
          <template v-if="userStore.isLoggedIn">
            <span class="mobile-username">{{ userStore.user?.username }}</span>
            <button class="mobile-logout" @click="handleLogout">退出登录</button>
          </template>
          <template v-else>
            <router-link to="/login" class="mobile-login" @click="mobileMenuOpen = false">登录 / 注册</router-link>
          </template>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../store/user'

defineEmits<{ focusSearch: [] }>()

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const mobileMenuOpen = ref(false)

// Close mobile menu on route change
watch(() => route.path, () => { mobileMenuOpen.value = false })

function handleLogout() {
  mobileMenuOpen.value = false
  userStore.logout()
  router.push('/')
}
</script>

<style scoped>
.app-header {
  background: var(--bg-white);
  box-shadow: var(--shadow-sm);
  position: sticky;
  top: 0;
  z-index: 100;
}
.header-inner {
  display: flex;
  align-items: center;
  height: 64px;
  gap: 32px;
}
.logo { display: flex; align-items: center; }
.logo-text { font-size: 20px; font-weight: 700; color: var(--primary); }
.nav-links { display: flex; gap: 24px; flex: 1; }
.nav-links a {
  color: var(--text-regular);
  font-size: 15px;
  padding: 4px 0;
  border-bottom: 2px solid transparent;
  transition: all 0.2s;
}
.nav-links a:hover, .nav-links a.active {
  color: var(--primary);
  border-bottom-color: var(--primary);
}
.header-right { display: flex; align-items: center; gap: 16px; }
.search-btn {
  background: none;
  color: var(--text-regular);
  padding: 6px;
  border-radius: 50%;
  transition: background 0.2s;
}
.search-btn:hover { background: var(--bg-page); }
.username { font-size: 14px; color: var(--text-secondary); }
.logout-btn { background: none; color: var(--text-secondary); font-size: 14px; }
.logout-btn:hover { color: var(--primary); }
.login-link { font-size: 14px; }

/* Hamburger - hidden on desktop */
.hamburger-btn {
  display: none;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  background: none;
  padding: 8px;
  margin-left: auto;
}
.hamburger-btn span {
  display: block;
  width: 22px;
  height: 2px;
  background: var(--text-primary);
  border-radius: 2px;
  transition: all 0.3s;
}
.hamburger-btn.open span:nth-child(1) { transform: rotate(45deg) translate(5px, 5px); }
.hamburger-btn.open span:nth-child(2) { opacity: 0; }
.hamburger-btn.open span:nth-child(3) { transform: rotate(-45deg) translate(5px, -5px); }

/* Mobile menu - hidden on desktop */
.mobile-menu {
  display: none;
  padding-bottom: 16px;
  border-top: 1px solid var(--border-color);
}
.mobile-nav {
  display: flex;
  flex-direction: column;
}
.mobile-nav a {
  padding: 12px 0;
  color: var(--text-regular);
  font-size: 15px;
  border-bottom: 1px solid var(--bg-page);
  transition: color 0.2s;
}
.mobile-nav a:hover { color: var(--primary); }
.mobile-actions {
  display: flex;
  align-items: center;
  gap: 16px;
  padding-top: 12px;
  flex-wrap: wrap;
}
.mobile-search-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  background: none;
  color: var(--text-regular);
  font-size: 14px;
  padding: 6px 12px;
  border-radius: var(--radius);
}
.mobile-search-btn:hover { background: var(--bg-page); }
.mobile-username { font-size: 14px; color: var(--text-secondary); }
.mobile-logout { background: none; color: var(--text-secondary); font-size: 14px; }
.mobile-login {
  font-size: 14px;
  padding: 6px 16px;
  background: var(--primary);
  color: #fff;
  border-radius: var(--radius);
}

/* Slide transition */
.slide-enter-active, .slide-leave-active { transition: all 0.25s ease; }
.slide-enter-from, .slide-leave-to { opacity: 0; transform: translateY(-8px); }

/* ========== Mobile ========== */
@media (max-width: 768px) {
  .header-inner {
    height: 56px;
    gap: 0;
  }
  .logo-text { font-size: 17px; }
  .nav-links, .header-right { display: none; }
  .hamburger-btn { display: flex; }
  .mobile-menu { display: block; }
}
</style>
