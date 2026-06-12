export interface ApiResponse<T> {
  code: number
  message: string
  data: T | null
}

export interface PaginatedData<T> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface TokenData {
  access_token: string
  token_type: string
  refresh_token: string
}

export interface Category {
  id: number
  name: string
  sort_order: number
  resource_count: number
  created_at: string | null
}
