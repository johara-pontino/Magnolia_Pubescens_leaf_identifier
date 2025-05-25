// utils/api.ts
import axios from 'axios'

const api = axios.create({
  baseURL: 'https://magnolia-pubescens-leaf-identifier.onrender.com', // your FastAPI Render backend
})

export default api
