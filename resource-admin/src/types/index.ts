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

export interface Category {
  id: number
  name: string
  sort_order: number
  resource_count: number
  created_at: string | null
}

export interface Resource {
  id: number
  title: string
  summary: string
  category_id: number
  category_name: string
  cover_url: string
  tags: string
  file_size: number
  upload_time: string | null
  is_hot: number
  view_count: number
  favorite_count: number
  uploader_id: number
  status: string
}

export interface User {
  id: number
  username: string
  role: string
  status: string
  created_at: string | null
}

export interface Statistics {
  resource_count: number
  user_count: number
  today_resources: number
  today_users: number
  category_distribution: { id: number; name: string; count: number }[]
}
