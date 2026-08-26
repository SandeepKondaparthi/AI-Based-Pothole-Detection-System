/**
 * Application Configuration
 * Environment-specific settings for the frontend
 */

const CONFIG = {
  // API Configuration
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  API_VERSION: '/api',
  
  // Authentication
  TOKEN_KEY: 'roadcare_access_token',
  REFRESH_TOKEN_KEY: 'roadcare_refresh_token',
  USER_KEY: 'roadcare_user',
  
  // Token Expiry (in milliseconds)
  TOKEN_EXPIRY: 30 * 60 * 1000, // 30 minutes
  
  // File Upload
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_IMAGE_TYPES: ['image/jpeg', 'image/jpg', 'image/png'],
  
  // Pagination
  DEFAULT_PAGE_SIZE: 20,
  MAX_PAGE_SIZE: 100,
  
  // Map Settings
  DEFAULT_LATITUDE: 34.0522,
  DEFAULT_LONGITUDE: -118.2437,
  
  // UI Settings
  TOAST_DURATION: 5000, // 5 seconds
  LOADING_MIN_DURATION: 500, // Minimum loading spinner duration
  
  // Get full API endpoint URL
  getApiUrl: (endpoint) => {
    const cleanEndpoint = endpoint.startsWith('/') ? endpoint.substring(1) : endpoint
    return `${CONFIG.API_BASE_URL}${CONFIG.API_VERSION}/${cleanEndpoint}`
  }
}

export default CONFIG
