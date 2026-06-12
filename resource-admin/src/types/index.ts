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
  tags: string
  link: string
  link_password: string
  file_size: number
  upload_time: string | null
  is_hot: number
  view_count: number
  favorite_count: number
  uploader_id: number
  uploader_name: string
  uploader_nickname: string
  status: string
}

export interface User {
  id: number
  username: string
  nickname: string
  role: string
  status: string
  created_at: string | null
}

export interface Statistics {
  resource_count: number
  user_count: number
  today_resources: number
  today_users: number
  pending_count: number
  published_count: number
  status_counts: Record<string, number>
  category_distribution: { id: number; name: string; count: number }[]
}
