import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const fetchOrganizations = () => api.get('/organizations').then(res => res.data)
export const createOrganization = (data: any) => api.post('/organizations', data).then(res => res.data)

export const fetchProjects = (orgId: string) => api.get(`/projects?organization_id=${orgId}`).then(res => res.data)
export const createProject = (data: any) => api.post('/projects', data).then(res => res.data)

export const startExecution = (projectId: string) => api.post('/execution', { project_id: projectId }).then(res => res.data)
export const fetchExecution = (id: string) => api.get(`/execution/${id}`).then(res => res.data)

export const fetchReports = (projectId: string) => api.get(`/reports?project_id=${projectId}`).then(res => res.data)

