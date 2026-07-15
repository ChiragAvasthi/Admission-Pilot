import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add response interceptor for global error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // We can add toast notifications here later
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)
