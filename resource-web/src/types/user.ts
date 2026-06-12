export interface User {
  id: number
  username: string
  nickname: string
  role: string
  created_at: string | null
}

export interface LoginData {
  username: string
  password: string
}

export interface RegisterData {
  username: string
  password: string
  nickname?: string
  captcha_key?: string
  captcha_code?: string
}

export interface TokenData {
  access_token: string
  refresh_token: string
  token_type: string
}
