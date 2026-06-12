import http from './index'
import type { ApiResponse } from '../types/api'

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

export const shareApi = {
  list: () =>
    http.get<ApiResponse<Share[]>>('/shares'),
}
