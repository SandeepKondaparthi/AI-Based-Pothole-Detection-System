import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useTheme } from '../context/ThemeContext'
import ApiService from '../services/apiService'
import LoadingSpinner from '../components/LoadingSpinner'

const AuthorityDashboardPage = () => {
  const { user, logout } = useAuth()
  const { toggleTheme, isDark } = useTheme()
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)
  const [stats, setStats] = useState({
    pending: 0,
    verified: 0,
    repaired: 0,
  })

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const response = await ApiService.reports.getAll()
      if (Array.isArray(response.data)) {
        setReports(response.data)
        
        // Calculate stats
        const pending = response.data.filter(r => r.status === 'pending').length
        const verified = response.data.filter(r => r.status === 'verified').length
        const repaired = response.data.filter(r => r.status === 'repaired').length
        
        setStats({ pending, verified, repaired })
      } else {
        setReports([])
      }
    } catch (error) {
      console.error('Error fetching reports:', error)
    } finally {
      setLoading(false)
    }
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400',
      verified: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400',
      repaired: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400',
    }
    return colors[status] || colors.pending
  }

  const getSeverityColor = (severity) => {
    const colors = {
      low: 'text-green-600',
      medium: 'text-yellow-600',
      high: 'text-orange-600',
      critical: 'text-red-600',
    }
    return colors[severity] || colors.medium
  }

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  return (
    <div className="bg-background-light dark:bg-background-dark text-[#111418] dark:text-white min-h-screen flex flex-col">
      {/* Top Navigation Bar */}
      <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-[#dbe0e6] dark:border-[#2a3540] bg-white dark:bg-[#1a2632] px-10 py-3 sticky top-0 z-50">
        <div className="flex items-center gap-8">
          <div className="flex items-center gap-4 text-primary">
            <span className="material-symbols-outlined text-3xl">edit_road</span>
            <h2 className="text-[#111418] dark:text-white text-lg font-bold leading-tight tracking-[-0.015em]">
              RoadCare Authority
            </h2>
          </div>
          <nav className="flex items-center gap-9">
            <a href="#dashboard" className="text-primary text-sm font-bold leading-normal hover:text-primary transition-colors">
              Dashboard
            </a>
            <a href="#reports" className="text-sm font-medium leading-normal hover:text-primary transition-colors">
              Reports
            </a>
            <a href="#analytics" className="text-sm font-medium leading-normal hover:text-primary transition-colors">
              Analytics
            </a>
          </nav>
        </div>
        <div className="flex gap-2 items-center">
          <button
            onClick={toggleTheme}
            data-testid="authority-theme-toggle"
            className="flex items-center justify-center rounded-lg h-10 w-10 bg-[#f0f2f4] dark:bg-gray-800 text-[#111418] dark:text-white hover:bg-gray-200 transition-colors"
          >
            <span className="material-symbols-outlined">{isDark ? 'light_mode' : 'dark_mode'}</span>
          </button>
          <button
            onClick={logout}
            data-testid="authority-logout"
            className="flex items-center justify-center rounded-lg h-10 px-4 bg-red-500 text-white hover:bg-red-600 transition-colors"
          >
            <span className="material-symbols-outlined mr-2">logout</span>
            Logout
          </button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 px-10 py-8">
        {/* Welcome Section */}
        <div className="mb-8" id="dashboard">
          <h1 className="text-3xl font-bold mb-2">Welcome back</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Here's an overview of road damage reports
          </p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8" id="analytics">
          <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
            <div className="flex items-center justify-between mb-4">
              <span className="material-symbols-outlined text-yellow-500 text-4xl">pending</span>
              <span className="text-3xl font-bold">{stats.pending}</span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase">Pending Reports</h3>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
            <div className="flex items-center justify-between mb-4">
              <span className="material-symbols-outlined text-blue-500 text-4xl">verified</span>
              <span className="text-3xl font-bold">{stats.verified}</span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase">Verified Reports</h3>
          </div>
          <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
            <div className="flex items-center justify-between mb-4">
              <span className="material-symbols-outlined text-green-500 text-4xl">task_alt</span>
              <span className="text-3xl font-bold">{stats.repaired}</span>
            </div>
            <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase">Repaired</h3>
          </div>
        </div>

        {/* Reports Table */}
        <div id="reports" data-testid="authority-reports-table" className="bg-white dark:bg-gray-900 rounded-xl border border-gray-200 dark:border-gray-800 overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-800">
            <h2 className="text-xl font-bold">Recent Reports</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-800/50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Location
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    AI Verification
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Status
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Date
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-800">
                {reports.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                      No reports found
                    </td>
                  </tr>
                ) : (
                  reports.map((report) => (
                    <tr key={report._id || report.id} className="hover:bg-gray-50 dark:hover:bg-gray-800/50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                        #{(report._id || report.id)?.substring(0, 8)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {report.location?.latitude?.toFixed(4)}, {report.location?.longitude?.toFixed(4)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        {(report.ai_confidence != null) ? (
                          <div className="flex flex-col gap-1">
                            <div className="flex items-center gap-2">
                              <span className={`material-symbols-outlined text-sm ${report.ai_verified ? 'text-green-500' : 'text-red-500'}`}>
                                {report.ai_verified ? 'check_circle' : 'cancel'}
                              </span>
                              <span className="font-semibold">{report.ai_confidence.toFixed(1)}%</span>
                            </div>
                            <span className="text-xs text-gray-500 dark:text-gray-400">
                              {report.ai_verified ? 'Pothole detected' : 'Not detected'}
                            </span>
                          </div>
                        ) : (
                          <span className="text-gray-400">N/A</span>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(report.status)}`}>
                          {report.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                        {report.report_date ? new Date(report.report_date).toLocaleDateString() : 'N/A'}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <Link
                          to={`/complaint/${report._id || report.id}`}
                          className="text-primary hover:underline font-medium"
                        >
                          View Details
                        </Link>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      </main>
    </div>
  )
}

export default AuthorityDashboardPage
