const LoadingSpinner = ({ fullScreen = false, size = 'medium' }) => {
  const sizeClasses = {
    small: 'h-6 w-6',
    medium: 'h-12 w-12',
    large: 'h-16 w-16'
  }

  const spinner = (
    <div className={`animate-spin rounded-full border-b-2 border-primary ${sizeClasses[size]}`}></div>
  )

  if (fullScreen) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background-light dark:bg-background-dark">
        {spinner}
      </div>
    )
  }

  return (
    <div className="flex items-center justify-center p-8">
      {spinner}
    </div>
  )
}

export default LoadingSpinner
