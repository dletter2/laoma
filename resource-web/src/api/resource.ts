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

  my: (params?: { page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/resources/my', { params }),

  favorite: (id: number) =>
    http.post<ApiResponse<{ favorited: boolean }>>(`/resources/${id}/favorite`),

  unfavorite: (id: number) =>
    http.delete<ApiResponse<{ favorited: boolean }>>(`/resources/${id}/favorite`),

  favorites: (params?: { page?: number; page_size?: number }) =>
    http.get<ApiResponse<PaginatedData<Resource>>>('/users/me/favorites', { params }),
}
