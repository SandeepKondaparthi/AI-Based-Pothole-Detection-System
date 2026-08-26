import { Navigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const ProtectedRoute = ({ children, requireAuth = true, requireAuthority = false }) => {
  const { isAuthenticated, isAuthority, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    )
  }

  // If authentication is required but user is not authenticated
  if (requireAuth && !isAuthenticated) {
    return <Navigate to="/citizen-login" replace />
  }

  // If authority access is required but user is not an authority
  if (requireAuthority && !isAuthority) {
    return <Navigate to="/authority-login" replace />
  }

  return children
}

export default ProtectedRoute
