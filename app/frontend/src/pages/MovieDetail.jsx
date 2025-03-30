import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'
import { getTMDbImageUrl, formatNumber } from '../utils'

const MovieDetail = () => {
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        setLoading(true)
        // Fetch real data from API
        const response = await axios.get(`/api/movies/${id}`)
        setMovie(response.data)
        setError(null)
      } catch (err) {
        console.error('Error fetching movie:', err)
        setError('Failed to fetch movie details. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchMovie()
  }, [id])

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary"></div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
        {error}
      </div>
    )
  }

  if (!movie) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-800 dark:text-white mb-4">Movie not found</h2>
        <Link to="/" className="text-secondary hover:underline">Return to homepage</Link>
      </div>
    )
  }

  // Generate fallback backdrop if none is available
  const backdropUrl = movie.backdrop_path 
    ? getTMDbImageUrl(movie.backdrop_path, 'original')
    : 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1740&q=80'

  // Generate fallback poster if none is available
  const posterUrl = movie.poster_path ? getTMDbImageUrl(movie.poster_path) : null

  return (
    <div className="animate-fade-in max-w-7xl mx-auto">
      <div className="mb-6">
        <Link to="/" className="text-secondary hover:text-secondary-600 transition-colors flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Movies
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
        <div className="relative h-48 sm:h-64 md:h-72 lg:h-96 w-full">
          <img
            src={backdropUrl}
            alt={`${movie.title} backdrop`}
            className="absolute inset-0 w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
          <div className="absolute bottom-0 left-0 p-4 sm:p-6 md:p-8 max-w-3xl">
            <h1 className="text-2xl sm:text-3xl md:text-4xl font-bold text-white mb-2">{movie.title}</h1>
            <div className="flex items-center text-gray-300 text-xs sm:text-sm">
              <span className="mr-3">{movie.year}</span>
              {movie.runtime && (
                <span className="mr-3">{Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m</span>
              )}
              {movie.language && (
                <span className="mr-3 uppercase">{movie.language}</span>
              )}
              {movie.rating && (
                <span className="flex items-center text-yellow-400">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 sm:h-5 sm:w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                  {Number(movie.rating).toFixed(1)}
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 p-4 sm:p-6">
          <div className="md:col-span-1">
            {posterUrl ? (
              <div className="max-w-xs mx-auto md:max-w-full">
                <img
                  src={posterUrl}
                  alt={movie.title}
                  className="w-full h-auto rounded-lg shadow-md"
                />
              </div>
            ) : (
              <div className="w-full max-w-xs mx-auto md:max-w-full aspect-[2/3] bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                <span className="text-gray-500 dark:text-gray-400">No Poster</span>
              </div>
            )}

            <div className="mt-6 bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Ratings</h3>
              <div className="space-y-3">
                {movie.rating && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">TMDb</span>
                    <span className="font-medium px-2 py-1 bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-200 rounded">{Number(movie.rating).toFixed(1)}/10</span>
                  </div>
                )}
                {movie.votes && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">Votes</span>
                    <span className="font-medium px-2 py-1 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded">{formatNumber(movie.votes)}</span>
                  </div>
                )}
                {movie.imdb_id && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">IMDb ID</span>
                    <a 
                      href={`https://www.imdb.com/title/${movie.imdb_id}`} 
                      target="_blank" 
                      rel="noopener noreferrer"
                      className="font-medium px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded hover:underline"
                    >
                      {movie.imdb_id}
                    </a>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 mb-6">
              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Genres</h3>
                <div className="flex flex-wrap gap-2">
                  {movie.genres && movie.genres.map((genre) => (
                    <span
                      key={genre.id}
                      className="bg-primary-100 dark:bg-primary-800 text-primary-800 dark:text-primary-200 px-3 py-1 rounded-full text-sm"
                    >
                      {genre.name}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4">
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Details</h3>
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-gray-600 dark:text-gray-300">Release Year</span>
                    <span className="text-gray-800 dark:text-gray-200">{movie.year}</span>
                  </div>
                  {movie.language && (
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-300">Language</span>
                      <span className="text-gray-800 dark:text-gray-200 uppercase">{movie.language}</span>
                    </div>
                  )}
                  {movie.runtime && (
                    <div className="flex justify-between">
                      <span className="text-gray-600 dark:text-gray-300">Runtime</span>
                      <span className="text-gray-800 dark:text-gray-200">{Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3">Director</h3>
              <div className="flex flex-wrap gap-2">
                {movie.director ? (
                  <span className="bg-secondary-100 dark:bg-secondary-900 text-secondary-800 dark:text-secondary-200 px-3 py-1 rounded-full text-sm">
                    {movie.director}
                  </span>
                ) : (
                  <span className="text-gray-600 dark:text-gray-300">Not available</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MovieDetail 