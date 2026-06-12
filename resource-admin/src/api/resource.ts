import http from './index'
import type { ApiResponse, PaginatedData, Resource } from '../types'

export const resourceApi = {
  list: (params: { page?: number; page_size?: number; status?: string }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/admin/resources', { params }),

  updateStatus: (id: number, status: string) =>
    http.put<ApiResponse<null>>(`/admin/resources/${id}/status`, { status }),

  delete: (id: number) =>
    http.delete<ApiResponse<null>>(`/admin/resources/${id}`),

  batchUpdateStatus: (ids: number[], status: string) =>
    http.put<ApiResponse<{ affected: number }>>('/admin/resources/batch/status', { ids, status }),

  batchDelete: (ids: number[]) =>
    http.post<ApiResponse<{ affected: number }>>('/admin/resources/batch/delete', { ids }),
}
