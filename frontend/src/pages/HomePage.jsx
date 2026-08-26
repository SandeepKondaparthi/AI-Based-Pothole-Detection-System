import { Link } from 'react-router-dom'
import Header from '../components/Header'
import Footer from '../components/Footer'

const HomePage = () => {
  return (
    <div className="bg-background-light dark:bg-background-dark font-display text-[#111418] dark:text-white transition-colors duration-200">
      <div className="relative flex min-h-screen w-full flex-col overflow-x-hidden">
        <Header />

        <main className="flex flex-col items-center flex-1">
          {/* Hero Section */}
          <div className="w-full max-w-[1280px] px-6 md:px-10 py-12 md:py-24">
            <div className="flex flex-col gap-8 md:flex-row items-center">
              {/* Text Content */}
              <div className="flex flex-col gap-6 flex-1 text-left">
                <div className="flex flex-col gap-3">
                  <span className="inline-flex items-center px-3 py-1 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-wider w-fit">
                    AI-Powered Maintenance
                  </span>
                  <h1 className="text-[#111418] dark:text-white text-4xl md:text-6xl font-black leading-tight tracking-[-0.033em]">
                    AI-Based Road Damage & Pothole Detection
                  </h1>
                  <p className="text-[#4f5b6b] dark:text-gray-400 text-base md:text-lg font-normal leading-relaxed max-w-[600px]">
                    Empowers citizens to report road hazards instantly using AI. Help your city stay safe and smooth by flagging potholes in seconds. Our system automatically verifies reports for faster repairs.
                  </p>
                </div>
                <div className="flex flex-wrap gap-4">
                  <Link 
                    to="/citizen-login"
                    className="flex min-w-[160px] cursor-pointer items-center justify-center rounded-xl h-14 px-6 bg-primary text-white text-base font-bold shadow-lg shadow-primary/25 hover:translate-y-[-2px] transition-all"
                  >
                    <span className="material-symbols-outlined mr-2">add_a_photo</span>
                    Report Pothole
                  </Link>
                  <Link 
                    to="/authority-login"
                    className="flex min-w-[160px] cursor-pointer items-center justify-center rounded-xl h-14 px-6 bg-white dark:bg-white/5 border border-primary/20 text-[#111418] dark:text-white text-base font-bold hover:bg-primary/5 transition-all"
                  >
                    <span className="material-symbols-outlined mr-2">admin_panel_settings</span>
                    Authority Login
                  </Link>
                </div>
              </div>

              {/* Visual Side */}
              <div className="flex-1 w-full flex justify-center items-center relative">
                <div className="relative w-full aspect-square md:aspect-video rounded-2xl overflow-hidden shadow-2xl">
                  <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 to-transparent mix-blend-overlay"></div>
                  <img 
                    alt="Clean city road with modern infrastructure" 
                    className="w-full h-full object-cover" 
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuAOgagAcHlwcj0ddv4ovemajUNqtpdMRGd4OR22qHcscBrKDkWcFBS49fXkMBzTqaqqMPLZ8vLvOB8L9I3P9F1MYZxSo0FQ6NslqEca6R7-Uu-dNuPMSKCqZJCYqS46UC3idkwrciB0HeRVE9NwerHeHFUVnewHhtGVGi37RF01DMLnP97aWBi4B0BMzM9aOuEX1gsQUE96k-zvypeCJtpw37wzsqpr4jD-nEf5YH-uxXU_-LKfiGwgpSdNqTVHy81XNVG1hmVkKzg"
                  />
                  <div className="absolute bottom-4 left-4 right-4 bg-white/90 dark:bg-background-dark/90 backdrop-blur-sm p-4 rounded-xl border border-white/20 flex items-center gap-4">
                    <div className="bg-primary/10 p-2 rounded-lg">
                      <span className="material-symbols-outlined text-primary">location_on</span>
                    </div>
                    <div>
                      <p className="text-xs font-bold text-primary uppercase">Recently Fixed</p>
                      <p className="text-sm font-semibold dark:text-white">Main Street Blvd, Sector 4</p>
                    </div>
                  </div>
                </div>
                <div className="absolute -z-10 -top-10 -right-10 w-64 h-64 bg-primary/10 rounded-full blur-3xl"></div>
              </div>
            </div>
          </div>

          {/* Stats Section */}
          <div className="w-full bg-white dark:bg-background-dark/50 border-y border-gray-100 dark:border-white/5">
            <div className="max-w-[1280px] mx-auto px-6 md:px-10 py-12">
              <div className="flex flex-wrap gap-6">
                <div className="flex min-w-[200px] flex-1 flex-col gap-2 rounded-xl p-8 bg-background-light dark:bg-white/5 border border-transparent hover:border-primary/30 transition-all">
                  <span className="material-symbols-outlined text-primary text-3xl mb-2">task_alt</span>
                  <p className="text-[#617589] text-sm font-medium uppercase tracking-wider">Potholes Fixed</p>
                  <p className="text-[#111418] dark:text-white tracking-tight text-4xl font-black">1,240</p>
                </div>
                <div className="flex min-w-[200px] flex-1 flex-col gap-2 rounded-xl p-8 bg-background-light dark:bg-white/5 border border-transparent hover:border-primary/30 transition-all">
                  <span className="material-symbols-outlined text-primary text-3xl mb-2">groups</span>
                  <p className="text-[#617589] text-sm font-medium uppercase tracking-wider">Active Citizens</p>
                  <p className="text-[#111418] dark:text-white tracking-tight text-4xl font-black">5,000+</p>
                </div>
                <div className="flex min-w-[200px] flex-1 flex-col gap-2 rounded-xl p-8 bg-background-light dark:bg-white/5 border border-transparent hover:border-primary/30 transition-all">
                  <span className="material-symbols-outlined text-primary text-3xl mb-2">speed</span>
                  <p className="text-[#617589] text-sm font-medium uppercase tracking-wider">Avg. Repair Time</p>
                  <p className="text-[#111418] dark:text-white tracking-tight text-4xl font-black">48 hrs</p>
                </div>
              </div>
            </div>
          </div>

          {/* How it Works Section */}
          <div id="how-it-works" className="w-full max-w-[1280px] px-6 md:px-10 py-20">
            <div className="flex flex-col gap-12 items-center">
              <div className="flex flex-col gap-4 text-center max-w-[720px]">
                <h2 className="text-[#111418] dark:text-white tracking-tight text-3xl md:text-5xl font-black leading-tight">
                  How RoadCare Works
                </h2>
                <p className="text-[#4f5b6b] dark:text-gray-400 text-lg font-normal leading-normal">
                  Our AI-driven platform streamlines the process of road maintenance from initial citizen detection to final verified repair.
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full">
                {/* Step 1 */}
                <div className="flex flex-col gap-6 rounded-2xl bg-white dark:bg-white/5 p-8 border border-gray-100 dark:border-white/10 hover:shadow-xl transition-all group">
                  <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                    <span className="material-symbols-outlined text-3xl">photo_camera</span>
                  </div>
                  <div className="flex flex-col gap-2">
                    <h3 className="text-[#111418] dark:text-white text-xl font-bold leading-tight">1. Report Instantly</h3>
                    <p className="text-[#617589] dark:text-gray-400 text-base font-normal leading-relaxed">
                      Simply take a photo of the road damage through our web app. Our system geotags the location and captures technical data automatically.
                    </p>
                  </div>
                </div>

                {/* Step 2 */}
                <div className="flex flex-col gap-6 rounded-2xl bg-white dark:bg-white/5 p-8 border border-gray-100 dark:border-white/10 hover:shadow-xl transition-all group">
                  <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                    <span className="material-symbols-outlined text-3xl">psychology</span>
                  </div>
                  <div className="flex flex-col gap-2">
                    <h3 className="text-[#111418] dark:text-white text-xl font-bold leading-tight">2. AI Verification</h3>
                    <p className="text-[#617589] dark:text-gray-400 text-base font-normal leading-relaxed">
                      Advanced AI analyzes the image in real-time to confirm damage type (pothole, crack, or fade) and assess the priority level based on severity.
                    </p>
                  </div>
                </div>

                {/* Step 3 */}
                <div className="flex flex-col gap-6 rounded-2xl bg-white dark:bg-white/5 p-8 border border-gray-100 dark:border-white/10 hover:shadow-xl transition-all group">
                  <div className="w-14 h-14 rounded-full bg-primary/10 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                    <span className="material-symbols-outlined text-3xl">construction</span>
                  </div>
                  <div className="flex flex-col gap-2">
                    <h3 className="text-[#111418] dark:text-white text-xl font-bold leading-tight">3. Authority Action</h3>
                    <p className="text-[#617589] dark:text-gray-400 text-base font-normal leading-relaxed">
                      Validated reports are dispatched to local repair crews. You&apos;ll receive a notification once the maintenance is completed.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Authority Portal Preview Section */}
          <div className="w-full bg-primary/5 py-20 px-6">
            <div className="max-w-[1280px] mx-auto flex flex-col md:flex-row gap-12 items-center">
              <div className="flex-1 space-y-6">
                <h2 className="text-3xl font-black dark:text-white">Built for City Management</h2>
                <p className="text-lg text-gray-600 dark:text-gray-400">
                  RoadCare provides a powerful dashboard for municipal authorities to manage work orders, track budget allocation, and visualize road health across the city.
                </p>
                <ul className="space-y-4">
                  <li className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-medium dark:text-white">Real-time Heatmaps of Road Health</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-medium dark:text-white">Automated Crew Dispatch System</span>
                  </li>
                  <li className="flex items-center gap-3">
                    <span className="material-symbols-outlined text-primary">check_circle</span>
                    <span className="font-medium dark:text-white">Public Transparency Reporting</span>
                  </li>
                </ul>
              </div>
              <div className="flex-1 w-full">
                <div className="bg-white dark:bg-background-dark p-2 rounded-xl shadow-2xl border border-primary/10">
                  <img 
                    alt="Analytics Dashboard interface" 
                    className="rounded-lg w-full h-auto" 
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuCUTKLOIJaPmJYmVetYezbaBxbTrEViNuJiDEKys0tKT33Mp7JtXZYpGhYNBlH0bTtPGFb_vtonQg8c2RTdCkrJ3HQifky7zGe59sucd7zKP4G7rxzQqF9SMw927p8J39HowZjmcvBSgMKiQeAAOHrWwR_q0Y8mzuHoLr8p7CesT550g8fSVwL3jeV1v5fBzE6pDvkLXmBd_zDPBH2cnM3MwaVtHauODOBZCdEBV0V73d4eUTXopCX6qjhmt4uTBqkYYV57Usg-71s"
                  />
                </div>
              </div>
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </div>
  )
}

export default HomePage
