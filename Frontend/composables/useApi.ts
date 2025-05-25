import axios from 'axios'
import { useRuntimeConfig } from 'nuxt/app'

export default function useApi() {
  const config = useRuntimeConfig()
  const api = axios.create({
    baseURL: config.public.apiBase,
  })

  return { api }
}
