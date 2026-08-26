import { Link } from 'react-router-dom'
import Header from '../components/Header'
import Footer from '../components/Footer'

const HowItWorksPage = () => {
  return (
    <div className="bg-background-light dark:bg-background-dark min-h-screen text-[#111418] dark:text-white">
      <Header showAuthButtons={true} />
      
      <main className="flex-1 flex justify-center py-16 px-4">
        <div className="layout-content-container flex flex-col max-w-[900px] w-full gap-12">
          {/* Page Heading */}
          <div className="flex flex-col gap-3">
            <h1 className="text-[#111418] dark:text-white text-4xl font-black leading-tight tracking-[-0.033em]">
              How It Works
            </h1>
            <p className="text-[#617589] dark:text-gray-400 text-lg font-normal leading-normal">
              RoadCare uses AI-powered technology to detect and report road damage efficiently.
            </p>
          </div>

          {/* Steps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {/* Step 1 */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary text-2xl">camera_alt</span>
                </div>
                <h3 className="text-xl font-bold">1. Capture Photo</h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Citizens take a photo of the pothole or road damage using their phone camera. Clear images work best.
              </p>
            </div>

            {/* Step 2 */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary text-2xl">location_on</span>
                </div>
                <h3 className="text-xl font-bold">2. Add Location</h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                The app automatically detects your GPS location. You can adjust it manually if needed.
              </p>
            </div>

            {/* Step 3 */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary text-2xl">smart_toy</span>
                </div>
                <h3 className="text-xl font-bold">3. AI Analysis</h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Our AI system analyzes the image using computer vision to detect potholes with high accuracy.
              </p>
            </div>

            {/* Step 4 */}
            <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-[#dbe0e6] dark:border-gray-800 p-8 flex flex-col gap-4">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
                  <span className="material-symbols-outlined text-primary text-2xl">task_alt</span>
                </div>
                <h3 className="text-xl font-bold">4. Submit & Track</h3>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Reports are submitted and tracked. Authorities review and dispatch repairs.
              </p>
            </div>
          </div>

          {/* Key Features */}
          <div className="flex flex-col gap-6">
            <h2 className="text-2xl font-bold">Key Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="flex flex-col gap-3">
                <span className="material-symbols-outlined text-primary text-3xl">verified_user</span>
                <h4 className="font-semibold">AI Verification</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Automatic detection and verification of pothole reports.
                </p>
              </div>
              <div className="flex flex-col gap-3">
                <span className="material-symbols-outlined text-primary text-3xl">location_on</span>
                <h4 className="font-semibold">GPS Tracking</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Precise location tracking for effective repairs.
                </p>
              </div>
              <div className="flex flex-col gap-3">
                <span className="material-symbols-outlined text-primary text-3xl">group</span>
                <h4 className="font-semibold">Community Driven</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Report issues and contribute to safer roads.
                </p>
              </div>
            </div>
          </div>

          {/* CTA */}
          <div className="bg-primary/10 dark:bg-primary/20 rounded-xl border border-primary/30 p-8 flex flex-col gap-4 items-center text-center">
            <h3 className="text-2xl font-bold">Ready to Report?</h3>
            <p className="text-gray-600 dark:text-gray-400">
              Help us keep roads safe by reporting damage in your area.
            </p>
            <Link
              to="/report-pothole"
              className="bg-primary text-white px-8 py-3 rounded-lg font-semibold hover:bg-primary/90 transition-colors"
            >
              Report a Pothole
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  )
}

export default HowItWorksPage
