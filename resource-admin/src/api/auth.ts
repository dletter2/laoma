import http from './index'
import type { ApiResponse } from '../types'

export const authApi = {
  login: (data: { username: string; password: string; captcha_key: string; captcha_code: string }) =>
    http.post<ApiResponse<{ access_token: string; refresh_token: string }>>('/auth/login', data),

  me: () =>
    http.get<ApiResponse<{ id: number; username: string; role: string }>>('/auth/me'),

  changePassword: (data: { old_password: string; new_password: string }) =>
    http.put<ApiResponse<null>>('/auth/password', data),
}
