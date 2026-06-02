import http from './index'
import type { ApiResponse, PaginatedData, Resource } from '../types'

export const resourceApi = {
  list: (params: { page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/resources', { params }),

  updateStatus: (id: number, status: string) =>
    http.put<ApiResponse<null>>(`/admin/resources/${id}/status`, { status }),
}
