import { Link } from 'react-router-dom'
import { useTheme } from '../context/ThemeContext'
import { useAuth } from '../context/AuthContext'

const Header = ({ showAuthButtons = true }) => {
  const { toggleTheme, isDark } = useTheme()
  const { isAuthenticated, user, logout } = useAuth()

  return (
    <header className="flex items-center justify-center border-b border-solid border-[#f0f2f4] dark:border-white/10 bg-white/80 dark:bg-background-dark/80 backdrop-blur-md sticky top-0 z-50">
      <div className="layout-content-container flex flex-1 max-w-[1280px] items-center justify-between px-6 md:px-10 py-3">
        <Link to="/" className="flex items-center gap-4 text-primary">
          <div className="size-8 flex items-center justify-center">
            <span className="material-symbols-outlined text-4xl">edit_road</span>
          </div>
          <h2 className="text-[#111418] dark:text-white text-xl font-bold leading-tight tracking-[-0.015em]">
            RoadCare
          </h2>
        </Link>
        
        <div className="flex flex-1 justify-end gap-8 items-center">
          <nav className="hidden md:flex items-center gap-9">
            <Link to="/how-it-works" className="text-[#111418] dark:text-gray-300 text-sm font-medium hover:text-primary transition-colors">
              How it Works
            </Link>
            <Link to="/recent-reports" className="text-[#111418] dark:text-gray-300 text-sm font-medium hover:text-primary transition-colors">
              Recent Reports
            </Link>
            <Link to="/contact" className="text-[#111418] dark:text-gray-300 text-sm font-medium hover:text-primary transition-colors">
              Contact
            </Link>
          </nav>
          
          <div className="flex gap-3 items-center">
            {/* Theme Toggle */}
            <button
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              aria-label="Toggle theme"
            >
              <span className="material-symbols-outlined text-[#111418] dark:text-white">
                {isDark ? 'light_mode' : 'dark_mode'}
              </span>
            </button>
            
            {showAuthButtons && (
              <>
                {isAuthenticated ? (
                  <>
                    {/* Logged in user menu */}
                    <Link 
                      to={user?.role === 'authority' ? '/authority-dashboard' : '/report-pothole'}
                      className="flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold hover:brightness-110 transition-all shadow-md"
                    >
                      <span className="material-symbols-outlined mr-2 text-lg">
                        {user?.role === 'authority' ? 'dashboard' : 'add_a_photo'}
                      </span>
                      <span>{user?.role === 'authority' ? 'Dashboard' : 'Report'}</span>
                    </Link>
                    <div className="hidden sm:flex items-center gap-2 px-3 py-2 rounded-lg bg-gray-100 dark:bg-gray-800">
                      <span className="material-symbols-outlined text-primary">person</span>
                      <span className="text-sm font-medium">{user?.name || user?.email}</span>
                    </div>
                    <button
                      onClick={logout}
                      className="hidden sm:flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 border border-red-500 text-red-500 text-sm font-bold hover:bg-red-50 dark:hover:bg-red-900/20 transition-all"
                    >
                      <span className="material-symbols-outlined mr-2 text-lg">logout</span>
                      <span>Logout</span>
                    </button>
                  </>
                ) : (
                  <>
                    <Link 
                      to="/citizen-login"
                      className="flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold hover:brightness-110 transition-all shadow-md"
                    >
                      <span>Citizen Login</span>
                    </Link>
                    <Link 
                      to="/authority-login"
                      className="hidden sm:flex min-w-[84px] cursor-pointer items-center justify-center rounded-lg h-10 px-4 border border-primary text-primary dark:text-primary text-sm font-bold hover:bg-primary/10 transition-all"
                    >
                      <span>Authority Login</span>
                    </Link>
                  </>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
