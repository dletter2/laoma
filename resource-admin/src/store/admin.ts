import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '../api/auth'

export const useAdminStore = defineStore('admin', () => {
  const admin = ref<{ id: number; username: string; role: string } | null>(null)
  const token = ref<string | null>(localStorage.getItem('admin_token'))
  const isLoggedIn = computed(() => !!token.value)

  async function init() {
    if (token.value) {
      try {
        const res = await authApi.me()
        admin.value = res.data.data
        if (admin.value?.role !== 'admin') {
          logout()
        }
      } catch {
        logout()
      }
    }
  }

  function setToken(accessToken: string) {
    token.value = accessToken
    localStorage.setItem('admin_token', accessToken)
  }

  function logout() {
    admin.value = null
    token.value = null
    localStorage.removeItem('admin_token')
  }

  return { admin, token, isLoggedIn, init, setToken, logout }
})
