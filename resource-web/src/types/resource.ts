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

export interface ResourceCreate {
  title: string
  summary?: string
  category_id: number
  cover_url?: string
  tags?: string
  file_size?: number
  file_path?: string
}
