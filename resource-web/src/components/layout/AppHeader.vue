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
          <div class="user-dropdown" ref="dropdownRef">
            <button class="username-btn" @click="dropdownOpen = !dropdownOpen">
              <span>{{ userStore.user?.username }}</span>
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 12 15 18 9"/></svg>
            </button>
            <transition name="fade">
              <div v-if="dropdownOpen" class="dropdown-menu">
                <button class="dropdown-item" @click="openChangePassword">修改密码</button>
                <button class="dropdown-item logout" @click="handleLogout">退出登录</button>
              </div>
            </transition>
          </div>
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
            <button class="mobile-action-btn" @click="openChangePasswordMobile">修改密码</button>
            <button class="mobile-logout" @click="handleLogout">退出登录</button>
          </template>
          <template v-else>
            <router-link to="/login" class="mobile-login" @click="mobileMenuOpen = false">登录 / 注册</router-link>
          </template>
        </div>
      </div>
    </transition>
  </header>

  <!-- Change password dialog -->
  <transition name="fade">
    <div v-if="dialogVisible" class="dialog-overlay" @click.self="dialogVisible = false">
      <div class="dialog-box">
        <div class="dialog-header">
          <h3>修改密码</h3>
          <button class="dialog-close" @click="dialogVisible = false">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
          </button>
        </div>
        <div class="dialog-body">
          <div class="form-item">
            <label>旧密码</label>
            <input v-model="pwdForm.old_password" type="password" placeholder="请输入旧密码" />
          </div>
          <div class="form-item">
            <label>新密码</label>
            <input v-model="pwdForm.new_password" type="password" placeholder="请输入新密码（至少6位）" />
          </div>
          <div class="form-item">
            <label>确认新密码</label>
            <input v-model="pwdForm.confirm_password" type="password" placeholder="请再次输入新密码" />
          </div>
        </div>
        <div class="dialog-footer">
          <button class="btn-cancel" @click="dialogVisible = false">取消</button>
          <button class="btn-confirm" :disabled="pwdLoading" @click="handleChangePassword">
            {{ pwdLoading ? '提交中...' : '确认修改' }}
          </button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup lang="ts">
import { ref, reactive, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '../../store/user'
import { authApi } from '../../api/auth'

defineEmits<{ focusSearch: [] }>()

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()
const mobileMenuOpen = ref(false)

const dropdownOpen = ref(false)
const dropdownRef = ref<HTMLElement>()
const dialogVisible = ref(false)
const pwdLoading = ref(false)
const pwdForm = reactive({ old_password: '', new_password: '', confirm_password: '' })

watch(() => route.path, () => { mobileMenuOpen.value = false; dropdownOpen.value = false })

function handleClickOutside(e: MouseEvent) {
  if (dropdownRef.value && !dropdownRef.value.contains(e.target as Node)) {
    dropdownOpen.value = false
  }
}
onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

function handleLogout() {
  mobileMenuOpen.value = false
  dropdownOpen.value = false
  userStore.logout()
  router.push('/')
}

function openChangePassword() {
  dropdownOpen.value = false
  pwdForm.old_password = ''
  pwdForm.new_password = ''
  pwdForm.confirm_password = ''
  dialogVisible.value = true
}

function openChangePasswordMobile() {
  mobileMenuOpen.value = false
  pwdForm.old_password = ''
  pwdForm.new_password = ''
  pwdForm.confirm_password = ''
  dialogVisible.value = true
}

async function handleChangePassword() {
  if (!pwdForm.old_password) return alert('请输入旧密码')
  if (pwdForm.new_password.length < 6) return alert('新密码至少6位')
  if (pwdForm.new_password !== pwdForm.confirm_password) return alert('两次输入的密码不一致')
  pwdLoading.value = true
  try {
    await authApi.changePassword({ old_password: pwdForm.old_password, new_password: pwdForm.new_password })
    alert('密码修改成功')
    dialogVisible.value = false
  } catch (e) {
    alert((e as Error).message)
  } finally {
    pwdLoading.value = false
  }
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

.user-dropdown { position: relative; }
.username-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  background: none;
  color: var(--text-secondary);
  font-size: 14px;
  padding: 4px 8px;
  border-radius: var(--radius);
  transition: all 0.2s;
}
.username-btn:hover { color: var(--primary); background: var(--bg-page); }
.dropdown-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 4px;
  background: var(--bg-white);
  border-radius: var(--radius);
  box-shadow: var(--shadow-md);
  min-width: 120px;
  overflow: hidden;
  z-index: 200;
}
.dropdown-item {
  display: block;
  width: 100%;
  text-align: left;
  padding: 10px 16px;
  background: none;
  font-size: 14px;
  color: var(--text-regular);
  transition: all 0.15s;
}
.dropdown-item:hover { background: var(--bg-page); color: var(--primary); }
.dropdown-item.logout { color: #f56c6c; }
.dropdown-item.logout:hover { background: #fef0f0; }

/* Dialog */
.dialog-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}
.dialog-box {
  background: var(--bg-white);
  border-radius: var(--radius);
  width: 420px;
  max-width: 90vw;
  box-shadow: var(--shadow-md);
}
.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-color);
}
.dialog-header h3 { font-size: 16px; font-weight: 600; margin: 0; }
.dialog-close { background: none; color: var(--text-secondary); padding: 4px; }
.dialog-close:hover { color: var(--text-primary); }
.dialog-body { padding: 20px; }
.form-item { margin-bottom: 16px; }
.form-item:last-child { margin-bottom: 0; }
.form-item label {
  display: block;
  font-size: 14px;
  color: var(--text-regular);
  margin-bottom: 6px;
}
.form-item input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.form-item input:focus { border-color: var(--primary); }
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 12px 20px;
  border-top: 1px solid var(--border-color);
}
.btn-cancel {
  padding: 8px 20px;
  border: 1px solid var(--border-color);
  border-radius: var(--radius);
  background: var(--bg-white);
  font-size: 14px;
  color: var(--text-regular);
  cursor: pointer;
}
.btn-cancel:hover { color: var(--primary); border-color: var(--primary); }
.btn-confirm {
  padding: 8px 20px;
  border: none;
  border-radius: var(--radius);
  background: var(--primary);
  font-size: 14px;
  color: #fff;
  cursor: pointer;
}
.btn-confirm:hover { background: var(--primary-dark); }
.btn-confirm:disabled { opacity: 0.6; cursor: not-allowed; }

.fade-enter-active, .fade-leave-active { transition: opacity 0.2s; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

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
.mobile-action-btn { background: none; color: var(--text-regular); font-size: 14px; }
.mobile-action-btn:hover { color: var(--primary); }
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
