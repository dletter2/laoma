import http from './index'
import type { ApiResponse, PaginatedData, Category } from '../types/api'
import type { Resource, ResourceCreate } from '../types/resource'

export const resourceApi = {
  list: (params: { sort?: string; category_id?: number; page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/resources', { params }),

  search: (params: { q: string; page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/resources/search', { params }),

  get: (id: number) =>
    http.get<ApiResponse<Resource>>(`/resources/${id}`),

  create: (data: ResourceCreate) =>
    http.post<ApiResponse<Resource>>('/resources', data),

  favorite: (id: number) =>
    http.post<ApiResponse<{ favorited: boolean }>>(`/resources/${id}/favorite`),

  unfavorite: (id: number) =>
    http.delete<ApiResponse<{ favorited: boolean }>>(`/resources/${id}/favorite`),

  favorites: (params?: { page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/users/me/favorites', { params }),

  upload: (file: File, onProgress?: (percent: number) => void) => {
    const form = new FormData()
    form.append('file', file)
    return http.post<ApiResponse<{ url: string; size: number; filename: string }>>('/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        if (e.total && onProgress) onProgress(Math.round((e.loaded * 100) / e.total))
      },
    })
  },
}
