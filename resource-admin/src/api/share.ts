import http from './index'
import type { ApiResponse } from '../types'

export interface Share {
  id: number
  name: string
  url: string
  avatar_url: string
  description: string
  sort_order: number
  created_at: string | null
  updated_at: string | null
}

export interface ShareForm {
  name: string
  url: string
  avatar_url?: string
  description?: string
  sort_order?: number
}

export const shareApi = {
  list: () =>
    http.get<ApiResponse<Share[]>>('/admin/shares'),

  create: (data: ShareForm) =>
    http.post<ApiResponse<Share>>('/admin/shares', data),

  update: (id: number, data: Partial<ShareForm>) =>
    http.put<ApiResponse<Share>>(`/admin/shares/${id}`, data),

  delete: (id: number) =>
    http.delete<ApiResponse<null>>(`/admin/shares/${id}`),
}
