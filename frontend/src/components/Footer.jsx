import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-white dark:bg-background-dark border-t border-[#f0f2f4] dark:border-white/10 py-12 mt-auto">
      <div className="max-w-[1280px] mx-auto px-6 md:px-10">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1">
            <div className="flex items-center gap-3 mb-4">
              <span className="material-symbols-outlined text-3xl text-primary">edit_road</span>
              <h3 className="text-lg font-bold text-[#111418] dark:text-white">RoadCare</h3>
            </div>
            <p className="text-sm text-gray-600 dark:text-gray-400">
              AI-powered road damage detection and reporting system for safer communities.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-semibold text-[#111418] dark:text-white mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/how-it-works" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  How it Works
                </Link>
              </li>
              <li>
                <Link to="/recent-reports" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  Recent Reports
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  Contact Us
                </Link>
              </li>
            </ul>
          </div>

          {/* For Authorities */}
          <div>
            <h4 className="font-semibold text-[#111418] dark:text-white mb-4">For Authorities</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/authority-login" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  Dashboard
                </Link>
              </li>
              <li>
                <a href="https://docs.roadcare.local/api" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors" target="_blank" rel="noopener noreferrer">
                  API Documentation
                </a>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h4 className="font-semibold text-[#111418] dark:text-white mb-4">Legal</h4>
            <ul className="space-y-2">
              <li>
                <a href="#" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  Privacy Policy
                </a>
              </li>
              <li>
                <a href="#" className="text-sm text-gray-600 dark:text-gray-400 hover:text-primary transition-colors">
                  Terms of Service
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-200 dark:border-gray-700 mt-8 pt-8 text-center">
          <p className="text-sm text-gray-600 dark:text-gray-400">
            © {new Date().getFullYear()} RoadCare. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  )
}

export default Footer
