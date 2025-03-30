import { useState, useEffect } from 'react'
import axios from 'axios'
import { getTMDbImageUrl } from '../utils'

const Test = () => {
  const [moviesData, setMoviesData] = useState(null)
  const [genresData, setGenresData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)
        
        // Test both endpoints
        const [moviesRes, genresRes] = await Promise.all([
          axios.get('/api/movies?limit=5'),
          axios.get('/api/genres')
        ])
        
        setMoviesData(moviesRes.data)
        setGenresData(genresRes.data)
        setError(null)
      } catch (err) {
        console.error('Error fetching data:', err)
        setError(`Failed to fetch data: ${err.message}`)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="p-8">
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-8">
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          <h2 className="text-lg font-bold mb-2">Error</h2>
          <p>{error}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">API Test Page</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold mb-4">Movies Endpoint</h2>
          {moviesData ? (
            <div>
              <p className="mb-2">{moviesData.length} movies fetched</p>
              
              <h3 className="text-lg font-semibold mt-4 mb-2">First Movie</h3>
              {moviesData.length > 0 && (
                <div className="border border-gray-200 dark:border-gray-700 rounded-lg p-4 flex gap-4">
                  {moviesData[0].poster_path && (
                    <img 
                      src={getTMDbImageUrl(moviesData[0].poster_path, 'w200')} 
                      alt={moviesData[0].title}
                      className="w-24 h-auto rounded"
                    />
                  )}
                  <div>
                    <h4 className="font-bold">{moviesData[0].title} ({moviesData[0].year})</h4>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      Rating: {moviesData[0].rating} • Votes: {moviesData[0].votes}
                    </p>
                    <p className="text-sm mt-1">
                      Genres: {moviesData[0].genres?.map(g => g.name).join(', ') || 'None'}
                    </p>
                    <p className="text-sm mt-1">
                      Language: {moviesData[0].language}
                    </p>
                  </div>
                </div>
              )}
              
              <h3 className="text-lg font-semibold mt-4 mb-2">All Movies</h3>
              <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto max-h-60 text-xs">
                {JSON.stringify(moviesData, null, 2)}
              </pre>
            </div>
          ) : (
            <p>No movie data available</p>
          )}
        </div>
        
        <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-lg">
          <h2 className="text-xl font-bold mb-4">Genres Endpoint</h2>
          {genresData ? (
            <div>
              <p className="mb-2">{genresData.length} genres fetched</p>
              
              <h3 className="text-lg font-semibold mt-4 mb-2">All Genres</h3>
              <div className="flex flex-wrap gap-2 mb-4">
                {genresData.map(genre => (
                  <span 
                    key={genre.id}
                    className="bg-primary-100 dark:bg-primary-800 text-primary-800 dark:text-primary-200 px-3 py-1 rounded-full text-sm"
                  >
                    {genre.name}
                  </span>
                ))}
              </div>
              
              <pre className="bg-gray-100 dark:bg-gray-900 p-4 rounded-lg overflow-auto max-h-60 text-xs">
                {JSON.stringify(genresData, null, 2)}
              </pre>
            </div>
          ) : (
            <p>No genre data available</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default Test 