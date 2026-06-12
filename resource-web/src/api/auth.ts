import http from './index'
import type { ApiResponse, TokenData } from '../types/api'
import type { User, LoginData, RegisterData } from '../types/user'

export const authApi = {
  login: (data: LoginData) =>
    http.post<ApiResponse<TokenData>>('/auth/login', data),

  register: (data: RegisterData) =>
    http.post<ApiResponse<User>>('/auth/register', data),

  me: () =>
    http.get<ApiResponse<User>>('/auth/me'),

  changePassword: (data: { old_password: string; new_password: string }) =>
    http.put<ApiResponse<null>>('/auth/password', data),
}
