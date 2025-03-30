import { Link } from 'react-router-dom'
import { useState } from 'react'

const Navbar = () => {
  const [searchQuery, setSearchQuery] = useState('')
  
  const handleSearch = (e) => {
    e.preventDefault()
    // Implement search functionality
    console.log('Search for:', searchQuery)
  }
  
  return (
    <nav className="bg-primary text-white shadow-md">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="flex items-center space-x-2">
          <span className="text-2xl font-bold">MovieSeek</span>
        </Link>
        
        <div className="flex-1 max-w-xl mx-4">
          <form onSubmit={handleSearch} className="relative">
            <input
              type="text"
              placeholder="Search movies..."
              className="w-full px-4 py-2 rounded-full text-gray-800 focus:outline-none focus:ring-2 focus:ring-secondary"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-secondary text-white p-2 rounded-full hover:bg-secondary-dark focus:outline-none focus:ring-2 focus:ring-secondary-light"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </button>
          </form>
        </div>
        
        <div className="flex space-x-4">
          <Link to="/genres" className="hover:text-secondary">Genres</Link>
          <Link to="/top-rated" className="hover:text-secondary">Top Rated</Link>
        </div>
      </div>
    </nav>
  )
}

export default Navbar 