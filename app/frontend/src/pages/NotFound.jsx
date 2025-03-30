import { Link } from 'react-router-dom'

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center py-16 text-center">
      <h1 className="text-6xl font-bold text-gray-900 dark:text-white mb-4">404</h1>
      <h2 className="text-2xl font-semibold text-gray-800 dark:text-gray-200 mb-6">Page Not Found</h2>
      <p className="text-gray-600 dark:text-gray-400 max-w-md mb-8">
        We couldn't find the page you were looking for. The link might be broken, or the page may have been removed.
      </p>
      <Link 
        to="/" 
        className="px-6 py-3 bg-secondary text-white rounded-lg hover:bg-secondary-dark transition-colors"
      >
        Return to Homepage
      </Link>
    </div>
  )
}

export default NotFound 