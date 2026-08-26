import axios from 'axios'
import CONFIG from '../config/config'
import StorageUtils from '../utils/storageUtils'

/**
 * API Client using Axios
 */

// Create axios instance
const apiClient = axios.create({
  baseURL: CONFIG.API_BASE_URL + CONFIG.API_VERSION,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Request interceptor to add auth token
apiClient.interceptors.request.use(
  (config) => {
    const token = StorageUtils.get(CONFIG.TOKEN_KEY)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - clear tokens and redirect to login
      StorageUtils.remove(CONFIG.TOKEN_KEY)
      StorageUtils.remove(CONFIG.REFRESH_TOKEN_KEY)
      StorageUtils.remove(CONFIG.USER_KEY)
      
      if (!window.location.pathname.includes('login')) {
        window.location.href = '/authority-login'
      }
    }
    return Promise.reject(error)
  }
)

/**
 * API Service Methods
 */
const ApiService = {
  // Auth endpoints
  auth: {
    login: (credentials) => apiClient.post('/auth/login', credentials),
    register: (data) => apiClient.post('/auth/register', data),
    logout: () => apiClient.post('/auth/logout'),
  },

  // Reports endpoints
  reports: {
    getAll: (params) => apiClient.get('/reports', { params }),
    getById: (id) => apiClient.get(`/reports/${id}`),
    create: (data) => apiClient.post('/reports', data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    }),
    update: (id, data) => apiClient.put(`/reports/${id}/status`, data),
    delete: (id) => apiClient.delete(`/reports/${id}`),
    verify: (id, data) => apiClient.post(`/reports/${id}/verify`, data),
  },

  // Repairs endpoints
  repairs: {
    getAll: (params) => apiClient.get('/repairs', { params }),
    getById: (id) => apiClient.get(`/repairs/${id}`),
    create: (data) => apiClient.post('/repairs', data),
    update: (id, data) => apiClient.put(`/repairs/${id}`, data),
    delete: (id) => apiClient.delete(`/repairs/${id}`),
  },

  // Zones endpoints
  zones: {
    getAll: (params) => apiClient.get('/zones', { params }),
    getById: (id) => apiClient.get(`/zones/${id}`),
    getRiskZones: () => apiClient.get('/zones'),
  },
}

export default ApiService
export { apiClient }
