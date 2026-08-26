import { useEffect, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import ApiService from '../services/apiService'
import Header from '../components/Header'
import Footer from '../components/Footer'
import LoadingSpinner from '../components/LoadingSpinner'

const RecentReportsPage = () => {
  const { isAuthenticated } = useAuth()
  const [reports, setReports] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchReports = async () => {
      try {
        setLoading(true)
        let url = '/reports'
        if (isAuthenticated) {
          url += '?status_filter=verified&limit=20'
        }
        const response = await ApiService.reports.getAll(isAuthenticated ? { status_filter: 'verified', limit: 20 } : {})
        setReports(response.data || [])
      } catch (error) {
        console.error('Error fetching reports:', error)
        setReports([])
      } finally {
        setLoading(false)
      }
    }

    fetchReports()
  }, [isAuthenticated])

  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen text-[#111418] dark:text-white">
      <Header showAuthButtons={true} />
      
      <main className="flex-1 flex justify-center py-16 px-4">
        <div className="layout-content-container flex flex-col max-w-[1000px] w-full gap-8">
          {/* Page Heading */}
          <div className="flex flex-col gap-3">
            <h1 className="text-[#111418] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              Recent Reports
            </h1>
            <p className="text-[#617589] dark:text-gray-400 text-lg font-normal leading-normal">
              View verified pothole reports in your area
            </p>
          </div>

          {loading ? (
            <LoadingSpinner />
          ) : reports.length === 0 ? (
            <div className="bg-white dark:bg-gray-900 rounded-xl border border-[#dbe0e6] dark:border-gray-800 p-12 text-center">
              <span className="material-symbols-outlined text-5xl text-gray-400 block mb-4">inbox</span>
              <h3 className="text-xl font-semibold mb-2">No Reports Available</h3>
              <p className="text-gray-600 dark:text-gray-400">
                There are no recent verified reports yet. Be the first to report a pothole!
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {reports.map((report) => (
                <div key={report._id || report.id} className="bg-white dark:bg-gray-900 rounded-xl border border-[#dbe0e6] dark:border-gray-800 p-6 hover:shadow-md transition-shadow">
                  <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                    <div className="flex-1">
                      <h3 className="font-bold text-lg mb-2">
                        Pothole Report #{(report._id || report.id)?.substring(0, 8)}
                      </h3>
                      <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Location</span>
                          <p className="font-semibold">
                            {report.location?.latitude?.toFixed(4)}, {report.location?.longitude?.toFixed(4)}
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Status</span>
                          <p className="font-semibold">
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                              report.status === 'verified' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' :
                              report.status === 'pending' ? 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400' :
                              'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                            }`}>
                              {report.status}
                            </span>
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">AI Confidence</span>
                          <p className="font-semibold">
                            {report.ai_confidence != null ? `${report.ai_confidence.toFixed(1)}%` : 'N/A'}
                          </p>
                        </div>
                        <div>
                          <span className="text-gray-500 dark:text-gray-400">Date</span>
                          <p className="font-semibold">
                            {new Date(report.report_date).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                      {report.description && (
                        <p className="text-gray-600 dark:text-gray-400 mt-3">
                          {report.description}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default RecentReportsPage
