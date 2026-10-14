export interface Token {
  access_token: string
  token_type: string
}

export interface UserPublic {
  id: string
  username: string
  full_name: string | null
  is_active: boolean
  is_superuser: boolean
  created_at: string | null
}

export interface LoginInput {
  username: string
  password: string
}

export interface RegisterInput extends LoginInput {
  full_name?: string | null
}

export interface Message {
  message: string
}
