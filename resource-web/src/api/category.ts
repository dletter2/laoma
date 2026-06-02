import http from './index'
import type { ApiResponse, Category } from '../types/api'

export const categoryApi = {
  list: () =>
    http.get<ApiResponse<Category[]>>('/categories'),
}
