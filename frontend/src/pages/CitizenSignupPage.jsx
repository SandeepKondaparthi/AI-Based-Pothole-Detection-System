import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import Header from '../components/Header'
import Toast from '../components/Toast'
import LoadingSpinner from '../components/LoadingSpinner'

const CitizenSignupPage = () => {
  const navigate = useNavigate()
  const { register } = useAuth()
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
  })
  const [loading, setLoading] = useState(false)
  const [toast, setToast] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()

    // Validation
    if (formData.password !== formData.confirmPassword) {
      setToast({ message: 'Passwords do not match', type: 'error' })
      return
    }

    if (formData.password.length < 6) {
      setToast({ message: 'Password must be at least 6 characters', type: 'error' })
      return
    }

    setLoading(true)

    try {
      const result = await register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
        phone: formData.phone,
        role: 'user'
      })
      
      if (result.success) {
        setToast({ message: 'Account created successfully!', type: 'success' })
        setTimeout(() => {
          navigate('/citizen-login')
        }, 1500)
      } else {
        setToast({ message: result.error, type: 'error' })
      }
    } catch (error) {
      setToast({ message: 'Registration failed. Please try again.', type: 'error' })
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
                      <span className="material-symbols-outlined text-primary text-5xl">person_add</span>
                    </div>
                  </div>
                  <h1 className="text-[#111418] dark:text-white text-3xl font-black tracking-tight">
                    Create Account
                  </h1>
                  <p className="text-[#617589] dark:text-gray-400 text-sm">
                    Join RoadCare and help improve our city's roads
                  </p>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                  {/* Name */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-sm font-semibold">
                      Full Name
                    </label>
                    <input
                      type="text"
                      required
                      value={formData.name}
                      onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                      data-testid="signup-name"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="John Doe"
                    />
                  </div>

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
                      data-testid="signup-email"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="your.email@example.com"
                    />
                  </div>

                  {/* Phone */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-sm font-semibold">
                      Phone Number (Optional)
                    </label>
                    <input
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                      data-testid="signup-phone"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="+1 (555) 000-0000"
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
                      data-testid="signup-password"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="••••••••"
                    />
                  </div>

                  {/* Confirm Password */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-sm font-semibold">
                      Confirm Password
                    </label>
                    <input
                      type="password"
                      required
                      value={formData.confirmPassword}
                      onChange={(e) => setFormData({ ...formData, confirmPassword: e.target.value })}
                      data-testid="signup-confirm-password"
                      className="form-input w-full rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary h-12 px-4"
                      placeholder="••••••••"
                    />
                  </div>

                  {/* Submit Button */}
                  <button
                    type="submit"
                    disabled={loading}
                    data-testid="signup-submit"
                    className="w-full flex items-center justify-center rounded-xl h-12 bg-primary text-white font-bold shadow-lg hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed mt-2"
                  >
                    {loading ? <LoadingSpinner size="small" /> : 'Create Account'}
                  </button>
                </form>

                {/* Divider */}
                <div className="relative">
                  <div className="absolute inset-0 flex items-center">
                    <div className="w-full border-t border-gray-200 dark:border-gray-700"></div>
                  </div>
                  <div className="relative flex justify-center text-sm">
                    <span className="px-2 bg-white dark:bg-gray-900 text-[#617589] dark:text-gray-400">
                      Already have an account?
                    </span>
                  </div>
                </div>

                {/* Sign In Link */}
                <Link
                  to="/citizen-login"
                  className="w-full flex items-center justify-center rounded-xl h-12 border-2 border-primary text-primary font-bold hover:bg-primary/5 transition-all"
                >
                  Sign In
                </Link>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default CitizenSignupPage
