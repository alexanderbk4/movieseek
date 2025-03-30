import { Link } from 'react-router-dom'

const Footer = () => {
  return (
    <footer className="bg-primary text-white py-8">
      <div className="container mx-auto px-4">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 className="text-xl font-bold mb-4">MovieSeek</h3>
            <p className="text-gray-300">
              A sophisticated movie recommendation system focused on quality insights and rich data exploration.
            </p>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li><Link to="/" className="text-gray-300 hover:text-secondary">Home</Link></li>
              <li><Link to="/genres" className="text-gray-300 hover:text-secondary">Genres</Link></li>
              <li><Link to="/top-rated" className="text-gray-300 hover:text-secondary">Top Rated</Link></li>
            </ul>
          </div>
          
          <div>
            <h3 className="text-lg font-semibold mb-4">About</h3>
            <ul className="space-y-2">
              <li><Link to="/about" className="text-gray-300 hover:text-secondary">About Us</Link></li>
              <li><Link to="/privacy" className="text-gray-300 hover:text-secondary">Privacy Policy</Link></li>
              <li><Link to="/terms" className="text-gray-300 hover:text-secondary">Terms of Service</Link></li>
            </ul>
          </div>
        </div>
        
        <div className="border-t border-gray-700 mt-8 pt-6 text-center text-gray-400">
          <p>&copy; {new Date().getFullYear()} MovieSeek. All rights reserved.</p>
        </div>
      </div>
    </footer>
  )
}

export default Footer 