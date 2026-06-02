import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '../types/user'
import { authApi } from '../api/auth'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('access_token'))

  const isLoggedIn = computed(() => !!token.value)

  async function init() {
    if (token.value) {
      try {
        const res = await authApi.me()
        user.value = res.data.data
      } catch {
        logout()
      }
    }
  }

  function setTokens(accessToken: string, _refreshToken: string) {
    token.value = accessToken
    localStorage.setItem('access_token', accessToken)
    localStorage.setItem('refresh_token', _refreshToken)
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, token, isLoggedIn, init, setTokens, logout }
})
