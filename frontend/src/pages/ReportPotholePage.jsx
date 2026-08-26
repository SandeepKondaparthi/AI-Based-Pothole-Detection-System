import { useState, useEffect } from 'react'
import { useAuth } from '../context/AuthContext'
import Header from '../components/Header'
import Footer from '../components/Footer'
import Toast from '../components/Toast'
import LoadingSpinner from '../components/LoadingSpinner'
import ApiService from '../services/apiService'

const ReportPotholePage = () => {
  const { user } = useAuth()
  const [formData, setFormData] = useState({
    image: null,
    description: '',
    latitude: 34.0522,
    longitude: -118.2437,
  })
  const [imagePreview, setImagePreview] = useState(null)
  const [loading, setLoading] = useState(false)
  const [submitted, setSubmitted] = useState(false)
  const [reportId, setReportId] = useState(null)
  const [toast, setToast] = useState(null)
  const [locationLoading, setLocationLoading] = useState(true)
  const [locationDetected, setLocationDetected] = useState(false)

  // Detect location on page load
  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setFormData(prev => ({
            ...prev,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          }))
          setLocationDetected(true)
          setLocationLoading(false)
          setToast({ message: 'Location detected successfully!', type: 'success' })
        },
        (error) => {
          console.error('Error getting location:', error)
          setLocationLoading(false)
          setToast({ 
            message: 'Could not detect location. Using default coordinates.', 
            type: 'warning' 
          })
        }
      )
    } else {
      setLocationLoading(false)
      setToast({ 
        message: 'Geolocation is not supported by your browser.', 
        type: 'warning' 
      })
    }
  }, [])

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setFormData({ ...formData, image: file })
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!formData.image) {
      setToast({ message: 'Please upload an image', type: 'error' })
      return
    }

    setLoading(true)

    try {
      const submitData = new FormData()
      submitData.append('image', formData.image)
      submitData.append('latitude', formData.latitude)
      submitData.append('longitude', formData.longitude)
      if (formData.description) {
        submitData.append('description', formData.description)
      }

      const response = await ApiService.reports.create(submitData)
      
      setSubmitted(true)
      setReportId(response.data.id)
      
      // Show AI verification results
      const aiConfidence = response.data.ai_confidence || 0
      const status = response.data.status
      
      let message = 'Report submitted successfully!'
      if (status === 'verified') {
        message = `✅ Report verified! AI detected a pothole with ${aiConfidence.toFixed(1)}% confidence.`
      } else if (status === 'rejected') {
        message = `⚠️ Report submitted but AI could not confirm a pothole (${aiConfidence.toFixed(1)}% confidence). Authorities will review manually.`
      } else {
        message = `Report submitted! AI confidence: ${aiConfidence.toFixed(1)}%. Pending authority review.`
      }
      
      setToast({ message, type: status === 'verified' ? 'success' : 'warning' })
      
      // Reset form
      setTimeout(() => {
        setFormData({
          image: null,
          description: '',
          latitude: 34.0522,
          longitude: -118.2437,
        })
        setImagePreview(null)
        setSubmitted(false)
      }, 5000)
    } catch (error) {
      console.error('Error submitting report:', error)
      setToast({ 
        message: error.response?.data?.detail || 'Failed to submit report. Please try again.', 
        type: 'error' 
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen text-[#111418] dark:text-white">
      {toast && <Toast {...toast} onClose={() => setToast(null)} />}
      
      <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden">
        <div className="layout-container flex h-full grow flex-col">
          <Header showAuthButtons={false} />

          <main className="flex-1 flex justify-center py-10 px-4">
            <div className="layout-content-container flex flex-col max-w-[800px] w-full gap-8">
              {/* Page Heading */}
              <div className="flex flex-col gap-3">
                <h1 className="text-[#111418] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
                  Report a Pothole
                </h1>
                <p className="text-[#617589] dark:text-gray-400 text-lg font-normal leading-normal">
                  Help us keep our roads safe. Upload a photo and our AI will automatically detect the damage and location.
                </p>
                {user && (
                  <div className="flex items-center gap-2 text-sm">
                    <span className="material-symbols-outlined text-primary">person</span>
                    <span className="text-gray-600 dark:text-gray-400">
                      Reporting as: <span className="font-semibold text-[#111418] dark:text-white">{user.name || user.email}</span>
                    </span>
                  </div>
                )}
              </div>

              {/* Submission Form Card */}
              <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-8">
                {/* Upload Section */}
                <div className="flex flex-col gap-4">
                  <label htmlFor="file-upload" className="flex flex-col items-center gap-6 rounded-xl border-2 border-dashed border-[#dbe0e6] dark:border-gray-700 bg-background-light/50 dark:bg-background-dark/30 px-6 py-14 hover:border-primary transition-colors cursor-pointer group">
                    <div className="flex flex-col items-center gap-4 text-center">
                      <div className="bg-primary/10 text-primary p-4 rounded-full group-hover:bg-primary group-hover:text-white transition-all">
                        <span className="material-symbols-outlined !text-4xl">photo_camera</span>
                      </div>
                      <div className="flex max-w-[480px] flex-col items-center gap-2">
                        <p className="text-[#111418] dark:text-white text-xl font-bold leading-tight">
                          {imagePreview ? 'Image Selected' : 'Upload Image'}
                        </p>
                        <p className="text-[#617589] dark:text-gray-400 text-sm font-normal leading-normal">
                          {imagePreview ? 'Click to change image' : 'Drag and drop your photo here, or click to browse. JPEG, PNG supported.'}
                        </p>
                      </div>
                    </div>
                    {imagePreview && (
                      <img src={imagePreview} alt="Preview" className="max-h-48 rounded-lg" />
                    )}
                  </label>
                  <input
                    id="file-upload"
                    type="file"
                    accept="image/jpeg,image/jpg,image/png"
                    onChange={handleFileChange}
                    data-testid="report-image-input"
                    className="hidden"
                  />
                </div>

                {/* Form Fields */}
                <div className="grid grid-cols-1 gap-6">
                  {/* GPS Coordinates (Read Only) */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-base font-semibold leading-normal flex items-center gap-2">
                      Auto-Detected GPS Coordinates
                      {locationLoading && (
                        <span className="text-xs text-gray-500 flex items-center gap-1">
                          <LoadingSpinner size="small" />
                          Detecting...
                        </span>
                      )}
                      {locationDetected && !locationLoading && (
                        <span className="text-xs text-green-600 dark:text-green-400 flex items-center gap-1">
                          <span className="material-symbols-outlined text-sm">check_circle</span>
                          Detected
                        </span>
                      )}
                    </label>
                    <div className="flex w-full items-stretch rounded-lg shadow-sm">
                      <input
                        className="form-input flex w-full min-w-0 flex-1 rounded-l-lg text-[#111418] dark:text-white bg-gray-50 dark:bg-gray-800 border border-[#dbe0e6] dark:border-gray-700 h-14 p-[15px] text-base font-mono cursor-not-allowed focus:ring-0"
                        readOnly
                        value={locationLoading ? 'Detecting location...' : `${formData.latitude.toFixed(4)}° N, ${formData.longitude.toFixed(4)}° W`}
                      />
                      <div className={`flex border border-[#dbe0e6] dark:border-gray-700 bg-gray-50 dark:bg-gray-800 items-center justify-center px-4 rounded-r-lg border-l-0 ${locationDetected ? 'text-green-600' : 'text-[#617589] dark:text-gray-400'}`}>
                        <span className="material-symbols-outlined">location_on</span>
                      </div>
                    </div>
                    <p className="text-xs text-[#617589] dark:text-gray-500 italic px-1">
                      Location is automatically detected from your browser&apos;s geolocation API.
                    </p>
                  </div>

                  {/* Landmarks/Description */}
                  <div className="flex flex-col gap-2">
                    <label className="text-[#111418] dark:text-white text-base font-semibold leading-normal">
                      Landmarks or Description (Optional)
                    </label>
                    <textarea
                      value={formData.description}
                      onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                      data-testid="report-description"
                      className="form-input flex w-full min-w-0 flex-1 resize-none rounded-lg text-[#111418] dark:text-white border border-[#dbe0e6] dark:border-gray-700 bg-white dark:bg-gray-800 focus:border-primary focus:ring-1 focus:ring-primary min-h-32 p-[15px] text-base font-normal placeholder:text-[#617589] dark:placeholder:text-gray-500"
                      placeholder="e.g., Near the corner of 5th and Main, outside the city park entrance."
                    />
                  </div>
                </div>

                {/* Action Button */}
                <div className="pt-4 border-t border-[#f0f2f4] dark:border-gray-800">
                  <button
                    type="submit"
                    disabled={loading}
                    data-testid="report-submit"
                    className="w-full flex cursor-pointer items-center justify-center rounded-xl h-14 bg-primary text-white text-lg font-bold shadow-lg hover:shadow-primary/20 hover:bg-primary/90 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {loading ? <LoadingSpinner size="small" /> : 'Submit Complaint'}
                  </button>
                </div>
              </form>

              {/* Success Message */}
              {submitted && (
                <div data-testid="report-success" className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800/50 rounded-xl p-6 flex items-start gap-4">
                  <div className="bg-green-500 text-white rounded-full p-2 flex items-center justify-center">
                    <span className="material-symbols-outlined">check_circle</span>
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center justify-between mb-1">
                      <h3 className="text-green-800 dark:text-green-400 font-bold text-lg">
                        Report Submitted Successfully
                      </h3>
                      <span className="bg-primary text-white text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
                        Submitted
                      </span>
                    </div>
                    <p className="text-green-700 dark:text-green-500 text-sm mb-3">
                      Your report has been logged. Our maintenance crew has been notified and will prioritize the repair based on the severity detected.
                    </p>
                    <div className="flex items-center gap-2">
                      <span className="text-[#617589] dark:text-gray-400 text-sm font-medium">Complaint ID:</span>
                      <code data-testid="report-complaint-id" className="bg-white dark:bg-gray-800 border border-green-100 dark:border-green-900 px-2 py-1 rounded font-bold text-green-800 dark:text-green-400">
                        #{reportId}
                      </code>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </main>

          <Footer />
        </div>
      </div>
    </div>
  )
}

export default ReportPotholePage
