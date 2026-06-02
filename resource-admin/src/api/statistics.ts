import http from './index'
import type { ApiResponse, Statistics } from '../types'

export const statisticsApi = {
  get: () =>
    http.get<ApiResponse<Statistics>>('/admin/statistics'),
}
