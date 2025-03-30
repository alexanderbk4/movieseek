import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-white dark:bg-primary-900 border-t border-gray-200 dark:border-primary-800 pt-10 pb-6 mt-10">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <div className="flex items-center space-x-2 mb-4">
              <div className="w-6 h-6 flex-shrink-0 flex items-center justify-center bg-secondary rounded-lg">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ width: '16px', height: '16px' }}>
                  <rect x="2" y="2" width="20" height="20" rx="2.18" ry="2.18"></rect>
                  <line x1="7" y1="2" x2="7" y2="22"></line>
                  <line x1="17" y1="2" x2="17" y2="22"></line>
                  <line x1="2" y1="12" x2="22" y2="12"></line>
                  <line x1="2" y1="7" x2="7" y2="7"></line>
                  <line x1="2" y1="17" x2="7" y2="17"></line>
                  <line x1="17" y1="17" x2="22" y2="17"></line>
                  <line x1="17" y1="7" x2="22" y2="7"></line>
                </svg>
              </div>
              <span className="text-lg font-bold text-primary-900 dark:text-white">MovieSeek</span>
            </div>
            <p className="text-gray-600 dark:text-gray-300 text-sm mb-4">
              A sophisticated movie recommendation system focused on quality insights and rich data exploration.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-secondary transition-colors w-5 h-5 inline-block">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true" style={{ width: '20px', height: '20px' }}>
                  <path fillRule="evenodd" d="M22 12c0-5.523-4.477-10-10-10S2 6.477 2 12c0 4.991 3.657 9.128 8.438 9.878v-6.987h-2.54V12h2.54V9.797c0-2.506 1.492-3.89 3.777-3.89 1.094 0 2.238.195 2.238.195v2.46h-1.26c-1.243 0-1.63.771-1.63 1.562V12h2.773l-.443 2.89h-2.33v6.988C18.343 21.128 22 16.991 22 12z" clipRule="evenodd" />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-secondary transition-colors w-5 h-5 inline-block">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true" style={{ width: '20px', height: '20px' }}>
                  <path d="M8.29 20.251c7.547 0 11.675-6.253 11.675-11.675 0-.178 0-.355-.012-.53A8.348 8.348 0 0022 5.92a8.19 8.19 0 01-2.357.646 4.118 4.118 0 001.804-2.27 8.224 8.224 0 01-2.605.996 4.107 4.107 0 00-6.993 3.743 11.65 11.65 0 01-8.457-4.287 4.106 4.106 0 001.27 5.477A4.072 4.072 0 012.8 9.713v.052a4.105 4.105 0 003.292 4.022 4.095 4.095 0 01-1.853.07 4.108 4.108 0 003.834 2.85A8.233 8.233 0 012 18.407a11.616 11.616 0 006.29 1.84" />
                </svg>
              </a>
              <a href="#" className="text-gray-400 hover:text-secondary transition-colors w-5 h-5 inline-block">
                <svg className="h-5 w-5" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true" style={{ width: '20px', height: '20px' }}>
                  <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
                </svg>
              </a>
            </div>
          </div>
          
          <div>
            <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-3">Navigation</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Home</Link></li>
              <li><Link to="/genres" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Genres</Link></li>
              <li><Link to="/top-rated" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Top Rated</Link></li>
              <li><Link to="/new-releases" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">New Releases</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-3">About</h3>
            <ul className="space-y-2">
              <li><Link to="/about" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">About Us</Link></li>
              <li><Link to="/privacy" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Privacy Policy</Link></li>
              <li><Link to="/terms" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Terms of Service</Link></li>
              <li><Link to="/contact" className="text-sm text-gray-600 dark:text-gray-300 hover:text-secondary dark:hover:text-secondary transition-colors">Contact Us</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-base font-semibold text-gray-900 dark:text-white mb-3">Subscribe</h3>
            <p className="text-gray-600 dark:text-gray-300 text-sm mb-3">
              Stay updated with the latest movies and features.
            </p>
            <form className="flex max-w-xs">
              <input
                type="email"
                placeholder="Your email"
                className="flex-1 px-3 py-1.5 bg-gray-100 dark:bg-primary-800 rounded-l-lg text-gray-800 dark:text-gray-200 focus:outline-none text-sm"
              />
              <button className="px-3 py-1.5 bg-secondary hover:bg-secondary-600 text-white rounded-r-lg transition-colors text-sm">
                Subscribe
              </button>
            </form>
          </div>
        </div>
        
        <div className="border-t border-gray-200 dark:border-gray-700 mt-8 pt-4 flex flex-col md:flex-row justify-between items-center text-gray-500 dark:text-gray-400 text-xs">
          <p>&copy; {new Date().getFullYear()} MovieSeek. All rights reserved.</p>
          <div className="mt-2 md:mt-0">
            <span>Made with </span>
            <span className="text-red-500">❤</span>
            <span> for movie enthusiasts</span>
          </div>
        </div>
      </div>
    </footer>
  )
}

export default Footer 