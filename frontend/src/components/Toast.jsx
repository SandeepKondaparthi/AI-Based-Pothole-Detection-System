import { useState, useEffect } from 'react'

const Toast = ({ message, type = 'info', duration = 5000, onClose }) => {
  const [isVisible, setIsVisible] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false)
      setTimeout(onClose, 300) // Wait for animation to complete
    }, duration)

    return () => clearTimeout(timer)
  }, [duration, onClose])

  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500'
  }[type]

  return (
    <div 
      className={`fixed top-4 right-4 z-50 transition-all duration-300 ${
        isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-2'
      }`}
    >
      <div className={`${bgColor} text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 max-w-md`}>
        <span className="material-symbols-outlined">
          {type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
        </span>
        <p className="flex-1">{message}</p>
        <button 
          onClick={() => {
            setIsVisible(false)
            setTimeout(onClose, 300)
          }}
          className="hover:opacity-80 transition-opacity"
        >
          <span className="material-symbols-outlined">close</span>
        </button>
      </div>
    </div>
  )
}

export default Toast
