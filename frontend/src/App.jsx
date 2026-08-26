import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './context/AuthContext'
import { ThemeProvider } from './context/ThemeContext'
import HomePage from './pages/HomePage'
import HowItWorksPage from './pages/HowItWorksPage'
import RecentReportsPage from './pages/RecentReportsPage'
import ContactPage from './pages/ContactPage'
import ReportPotholePage from './pages/ReportPotholePage'
import CitizenLoginPage from './pages/CitizenLoginPage'
import CitizenSignupPage from './pages/CitizenSignupPage'
import AuthorityLoginPage from './pages/AuthorityLoginPage'
import AuthorityDashboardPage from './pages/AuthorityDashboardPage'
import ComplaintDetailPage from './pages/ComplaintDetailPage'
import ProtectedRoute from './components/ProtectedRoute'

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router
          future={{
            v7_startTransition: true,
            v7_relativeSplatPath: true
          }}
        >
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/how-it-works" element={<HowItWorksPage />} />
            <Route 
              path="/recent-reports" 
              element={
                <ProtectedRoute requireAuth={true}>
                  <RecentReportsPage />
                </ProtectedRoute>
              } 
            />
            <Route path="/contact" element={<ContactPage />} />
            <Route path="/citizen-login" element={<CitizenLoginPage />} />
            <Route path="/citizen-signup" element={<CitizenSignupPage />} />
            <Route path="/authority-login" element={<AuthorityLoginPage />} />
            <Route 
              path="/report-pothole" 
              element={
                <ProtectedRoute requireAuth={true}>
                  <ReportPotholePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/authority-dashboard" 
              element={
                <ProtectedRoute requireAuth={true} requireAuthority={true}>
                  <AuthorityDashboardPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/complaint/:id" 
              element={
                <ProtectedRoute requireAuth={true} requireAuthority={true}>
                  <ComplaintDetailPage />
                </ProtectedRoute>
              } 
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  )
}

export default App
