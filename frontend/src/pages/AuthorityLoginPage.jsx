import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Header from '../components/Header'
import Toast from '../components/Toast'
import LoadingSpinner from '../components/LoadingSpinner'

const AuthorityLoginPage = () => {
  const navigate = useNavigate()
  const { login } = useAuth()
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  })
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const result = await login(formData.email, formData.password)
      
      if (result.success) {
        setToast({ message: 'Login successful!', type: 'success' })
        setTimeout(() => {
          navigate('/authority-dashboard')
        }, 1000)
      } else {
        setToast({ message: result.error, type: 'error' })
      }
    } catch (error) {
      setToast({ message: 'Login failed. Please try again.', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen">
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      
      <div className="relative flex min-h-screen w-full flex-col">
        <Header showAuthButtons={false} />

        <main className="flex-1 flex items-center justify-center py-12 px-4">
          <div className="w-full max-w-md">
            <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-xl border border-gray-200 dark:border-gray-800 p-8">
              <div className="flex flex-col gap-6">
                {/* Header */}
                <div className="flex flex-col gap-2 text-center">
                  <div className="flex justify-center mb-4">
                    <div className="bg-primary/10 p-4 rounded-full">
                      <span className="material-symbols-outlined text-primary text-5xl">admin_panel_settings</span>
                    </div>
                  </div>
                  <h1 className="text-[#111418] dark:text-white text-3xl font-black tracking-tight">
                    Authority Login
                  </h1>
                  <p className="text-[#617589] dark:text-gray-400 text-sm">
                    Access the dashboard to manage road maintenance reports
                  </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="flex flex-col gap-6">
                  {/* Email */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-sm font-semibold">
                      Email Address
                    </label>
                    <input
                      type="email"
                      required
                      value={formData.email}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                      data-testid="authority-email"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="authority@city.gov"
                    />
                  </div>

                  {/* Password */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-sm font-semibold">
                      Password
                    </label>
                    <input
                      type="password"
                      required
                      value={formData.password}
                      onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                      data-testid="authority-password"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="••••••••"
                    />
                  </div>

                  {/* Remember & Forgot */}
                  <div className="flex items-center justify-between">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        className="form-checkbox rounded text-primary focus:ring-primary"
                      />
                      <span className="text-sm text-[#617589] dark:text-gray-400">Remember me</span>
                    </label>
                    <a href="#" className="text-sm text-primary hover:underline font-medium">
                      Forgot password?
                    </a>
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={loading}
                    data-testid="authority-login-submit"
                    className="w-full flex items-center justify-center rounded-xl h-12 bg-primary text-white font-bold shadow-lg hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? <LoadingSpinner size="small" /> : 'Sign In'}
                  </button>
                </form>

                {/* Divider */}
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-200 dark:border-gray-700"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white dark:bg-gray-900 text-[#617589] dark:text-gray-400">
                      Need access?
                    </span>
                  </div>
                </div>

                {/* Contact */}
                <p className="text-center text-sm text-[#617589] dark:text-gray-400">
                  Contact your system administrator to request credentials
                </p>
              </div>
            </div>

            {/* Info Card */}
            <div className="mt-6 bg-primary/5 dark:bg-primary/10 rounded-xl p-4 border border-primary/20">
              <div className="flex items-start gap-3">
                <span className="material-symbols-outlined text-primary mt-0.5">info</span>
                <div className="flex-1">
                  <p className="text-sm text-[#111418] dark:text-white font-semibold mb-1">
                    For Authorized Personnel Only
                  </p>
                  <p className="text-xs text-[#617589] dark:text-gray-400">
                    This portal is restricted to city maintenance authorities and road management officials.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default AuthorityLoginPage
