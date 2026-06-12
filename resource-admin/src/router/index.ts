import { createRouter, createWebHistory } from 'vue-router'
import { useAdminStore } from '../store/admin'

const router = createRouter({
  history: createWebHistory('/admin/'),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue'),
    },
    {
      path: '/',
      component: () => import('../components/layout/AdminLayout.vue'),
      meta: { requiresAuth: true },
      children: [
        { path: '', name: 'dashboard', component: () => import('../views/DashboardView.vue') },
        { path: 'resources', name: 'resources', component: () => import('../views/ResourceManage.vue') },
        { path: 'categories', name: 'categories', component: () => import('../views/CategoryManage.vue') },
        { path: 'users', name: 'users', component: () => import('../views/UserManage.vue') },
        { path: 'shares', name: 'shares', component: () => import('../views/ShareManage.vue') },
        { path: 'settings', name: 'settings', component: () => import('../views/SettingsView.vue') },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const store = useAdminStore()
  if (to.meta.requiresAuth && !store.isLoggedIn) {
    return { name: 'login' }
  }
})

export default router
