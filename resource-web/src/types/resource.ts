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
  uploader_nickname: string
  status: string
}

export interface ResourceCreate {
  title: string
  summary?: string
  category_id: number
  tags?: string
  link: string
  link_password?: string
  file_size?: number
}
