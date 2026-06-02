import http from './index'
import type { ApiResponse, PaginatedData, User } from '../types'

export const userApi = {
  list: (params?: { page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<User>>>('/admin/users', { params }),

  updateStatus: (id: number, status: string) =>
    http.put<ApiResponse<null>>(`/admin/users/${id}/status`, { status }),
}
