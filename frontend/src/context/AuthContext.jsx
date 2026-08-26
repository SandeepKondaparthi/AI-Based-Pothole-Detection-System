import { createContext, useContext, useState, useEffect } from 'react'
import StorageUtils from '../utils/storageUtils'
import CONFIG from '../config/config'
import ApiService from '../services/apiService'

const AuthContext = createContext(null)

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [token, setToken] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check for existing session
    const savedUser = StorageUtils.get(CONFIG.USER_KEY)
    const savedToken = StorageUtils.get(CONFIG.TOKEN_KEY)
    
    if (savedUser && savedToken) {
      setUser(savedUser)
      setToken(savedToken)
    }
    
    setLoading(false)
  }, [])

  const login = async (email, password, userType = 'authority') => {
    try {
      const response = await ApiService.auth.login({
        email: email,
        password: password
      })
      
      const { access_token, id, name, email: userEmail, phone, role } = response.data
      const userData = { id, name, email: userEmail, phone, role }
      
      // Validate user role matches login type
      if (userType === 'authority' && role !== 'authority') {
        return { 
          success: false, 
          error: 'This account is not authorized for authority access' 
        }
      }
      
      if (userType === 'citizen' && role === 'authority') {
        return { 
          success: false, 
          error: 'Please use the authority login page' 
        }
      }
      
      // Save to storage
      StorageUtils.set(CONFIG.TOKEN_KEY, access_token)
      StorageUtils.set(CONFIG.USER_KEY, userData)
      
      // Update state
      setToken(access_token)
      setUser(userData)
      
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const register = async (userData) => {
    try {
      const response = await ApiService.auth.register(userData)
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('Registration error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Registration failed' 
      }
    }
  }

  const logout = () => {
    // Clear storage
    StorageUtils.remove(CONFIG.TOKEN_KEY)
    StorageUtils.remove(CONFIG.REFRESH_TOKEN_KEY)
    StorageUtils.remove(CONFIG.USER_KEY)
    
    // Clear state
    setUser(null)
    setToken(null)
  }

  const value = {
    user,
    token,
    login,
    register,
    logout,
    isAuthenticated: !!user,
    isAuthority: user?.role === 'authority',
    isCitizen: user?.role === 'user',
    loading
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
