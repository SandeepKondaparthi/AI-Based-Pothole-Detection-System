import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import ApiService from '../services/apiService'
import LoadingSpinner from '../components/LoadingSpinner'
import Toast from '../components/Toast'

const ComplaintDetailPage = () => {
  const { id } = useParams()
  const navigate = useNavigate()
  const { logout } = useAuth()
  const [report, setReport] = useState(null)
  const [loading, setLoading] = useState(true)
  const [toast, setToast] = useState(null)

  useEffect(() => {
    fetchReport()
  }, [id])

  const fetchReport = async () => {
    try {
      const response = await ApiService.reports.getById(id)
      setReport(response.data)
    } catch (error) {
      console.error('Error fetching report:', error)
      setToast({ message: 'Failed to load report details', type: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const handleStatusUpdate = async (newStatus) => {
    try {
      await ApiService.reports.update(id, { status: newStatus })
      setReport({ ...report, status: newStatus })
      setToast({ message: 'Status updated successfully', type: 'success' })
    } catch (error) {
      console.error('Error updating status:', error)
      setToast({ message: 'Failed to update status', type: 'error' })
    }
  }

  if (loading) {
    return <LoadingSpinner fullScreen />
  }

  if (!report) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Report not found</h2>
          <Link to="/authority-dashboard" className="text-primary hover:underline">
            Back to Dashboard
          </Link>
        </div>
      </div>
    )
  }

  const getStatusColor = (status) => {
    const colors = {
      pending: 'bg-yellow-100 text-yellow-800',
      verified: 'bg-blue-100 text-blue-800',
      repaired: 'bg-green-100 text-green-800',
    }
    return colors[status] || colors.pending
  }

  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen">
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      
      {/* Header */}
      <header className="flex items-center justify-between border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-background-dark px-10 py-3 sticky top-0 z-50">
        <div className="flex items-center gap-4">
          <Link to="/authority-dashboard" className="text-primary hover:opacity-80">
            <span className="material-symbols-outlined">arrow_back</span>
          </Link>
          <h2 className="text-lg font-bold">Report Details</h2>
        </div>
        <button
          onClick={logout}
          className="flex items-center gap-2 px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
        >
          <span className="material-symbols-outlined">logout</span>
          Logout
        </button>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Report Header */}
        <div className="bg-white dark:bg-gray-900 rounded-xl p-6 mb-6 border border-gray-200 dark:border-gray-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-3xl font-bold mb-2">Report #{(report._id || report.id)?.substring(0, 8)}</h1>
              <p className="text-gray-600 dark:text-gray-400">
                Submitted on {new Date(report.created_at).toLocaleString()}
              </p>
            </div>
            <span className={`px-4 py-2 rounded-full font-semibold ${getStatusColor(report.status)}`}>
              {report.status?.toUpperCase()}
            </span>
          </div>

          {/* Quick Actions */}
          <div className="flex gap-3 pt-4 border-t border-gray-200 dark:border-gray-800">
            {report.status === 'pending' && (
              <button
                onClick={() => handleStatusUpdate('verified')}
                className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                Mark as Verified
              </button>
            )}
            {report.status === 'verified' && (
              <button
                onClick={() => handleStatusUpdate('repaired')}
                className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
              >
                Mark as Repaired
              </button>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Image */}
          <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
            <h3 className="font-bold mb-4">Evidence Photo</h3>
            {report.image_url ? (
              <img
                src={report.image_url}
                alt="Pothole evidence"
                className="w-full rounded-lg"
              />
            ) : (
              <div className="aspect-video bg-gray-200 dark:bg-gray-800 rounded-lg flex items-center justify-center">
                <span className="text-gray-400">No image available</span>
              </div>
            )}
          </div>

          {/* Details */}
          <div className="space-y-6">
            {/* Location */}
            <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
              <h3 className="font-bold mb-4">Location</h3>
              <div className="space-y-4">
                <div className="flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">location_on</span>
                  <span className="font-mono">
                    {report.location?.latitude?.toFixed(6)}°, {report.location?.longitude?.toFixed(6)}°
                  </span>
                </div>
                {report.h3_index && (
                  <div className="flex items-center gap-2 text-sm text-gray-500">
                    <span className="material-symbols-outlined text-xs">grid_view</span>
                    <span>H3 Index: <code className="bg-gray-100 dark:bg-gray-800 px-1 rounded">{report.h3_index}</code></span>
                  </div>
                )}
                {report.description && (
                  <p className="text-gray-600 dark:text-gray-400 text-sm">
                    {report.description}
                  </p>
                )}
              </div>
            </div>

            {/* AI Analysis */}
            {report.ai_verified && (
              <div className="bg-white dark:bg-gray-900 rounded-xl p-6 border border-gray-200 dark:border-gray-800">
                <h3 className="font-bold mb-4">AI Analysis</h3>
                <div className="space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Damage Type</span>
                    <span className="font-semibold">{report.damage_type || 'Pothole'}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">Severity</span>
                    <span className="font-semibold">{report.severity || 'Medium'}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">AI Verified</span>
                    <span className="text-green-500 font-semibold">Yes</span>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}

export default ComplaintDetailPage
