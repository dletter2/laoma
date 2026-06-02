import http from './index'
import type { ApiResponse, Category } from '../types'

export const categoryApi = {
  list: () =>
    http.get<ApiResponse<Category[]>>('/categories'),

  create: (data: { name: string; sort_order: number }) =>
    http.post<ApiResponse<Category>>('/categories', data),

  update: (id: number, data: { name?: string; sort_order?: number }) =>
    http.put<ApiResponse<Category>>(`/categories/${id}`, data),

  delete: (id: number) =>
    http.delete<ApiResponse<null>>(`/categories/${id}`),
}
