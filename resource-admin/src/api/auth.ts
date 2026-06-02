import http from './index'
import type { ApiResponse } from '../types'

export const authApi = {
  login: (data: { username: string; password: string }) =>
    http.post<ApiResponse<{ access_token: string; refresh_token: string }>>('/auth/login', data),

  me: () =>
    http.get<ApiResponse<{ id: number; username: string; role: string }>>('/auth/me'),
}
