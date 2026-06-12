<template>
  <el-container class="admin-layout">
    <el-aside width="220px" class="sidebar">
      <div class="sidebar-header">
        <h2>资源分享站</h2>
        <span>管理后台</span>
      </div>
      <el-menu
        :default-active="route.path"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/">
          <el-icon><Odometer /></el-icon>
          <span>数据统计</span>
        </el-menu-item>
        <el-menu-item index="/resources">
          <el-icon><Files /></el-icon>
          <span>资源管理</span>
        </el-menu-item>
        <el-menu-item index="/categories">
          <el-icon><Menu /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        <el-menu-item index="/users">
          <el-icon><User /></el-icon>
          <span>用户管理</span>
        </el-menu-item>
        <el-menu-item index="/shares">
          <el-icon><Share /></el-icon>
          <span>分享管理</span>
        </el-menu-item>
        <el-menu-item index="/settings">
          <el-icon><Setting /></el-icon>
          <span>系统设置</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header class="admin-header">
        <span class="header-title">{{ routeTitle }}</span>
        <div class="header-right">
          <span>{{ adminStore.admin?.username }}</span>
          <el-button text @click="handleLogout">退出</el-button>
        </div>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Odometer, Files, Menu, User, Share, Setting } from '@element-plus/icons-vue'
import { useAdminStore } from '../../store/admin'

const route = useRoute()
const router = useRouter()
const adminStore = useAdminStore()

const titleMap: Record<string, string> = {
  '/': '数据统计',
  '/resources': '资源管理',
  '/categories': '分类管理',
  '/users': '用户管理',
  '/shares': '分享管理',
  '/settings': '系统设置',
}
const routeTitle = computed(() => titleMap[route.path] || '管理后台')

function handleLogout() {
  adminStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.admin-layout { height: 100vh; }
.sidebar { background: #304156; overflow-y: auto; }
.sidebar-header {
  padding: 20px;
  color: #fff;
  text-align: center;
}
.sidebar-header h2 { font-size: 18px; margin-bottom: 4px; }
.sidebar-header span { font-size: 12px; opacity: 0.7; }
.admin-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
}
.header-title { font-size: 18px; font-weight: 600; }
.header-right { display: flex; align-items: center; gap: 12px; }
</style>
