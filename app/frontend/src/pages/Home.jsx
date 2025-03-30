import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'
import MovieCard from '../components/MovieCard'
import { getTMDbImageUrl } from '../utils'

const Home = () => {
  const [movies, setMovies] = useState([])
  const [genres, setGenres] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true)
        // Fetch real data from API
        const response = await axios.get('/api/movies?limit=24')
        
        // Map any necessary transformations
        const processedMovies = response.data.map(movie => ({
          ...movie,
          // Extract year from the movie model if needed
          year: movie.year
        }))
        
        setMovies(processedMovies)
        setError(null)
      } catch (err) {
        console.error('Error fetching movies:', err)
        setError('Failed to fetch movies. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    const fetchGenres = async () => {
      try {
        const response = await axios.get('/api/genres')
        setGenres(response.data)
      } catch (err) {
        console.error('Error fetching genres:', err)
      }
    }

    // Fetch both movies and genres
    fetchMovies()
    fetchGenres()
  }, [])

  return (
    <div className="animate-fade-in">
      {/* Hero Section */}
      <div className="relative h-64 md:h-96 w-full mb-8">
        {movies.length > 0 && (
          <>
            <img
              src={movies[0].backdrop_path 
                ? getTMDbImageUrl(movies[0].backdrop_path, 'original')
                : 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&auto=format&fit=crop&w=1740&q=80'}
              alt="Featured movie"
              className="absolute inset-0 w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black to-transparent"></div>
            <div className="absolute inset-0 bg-gradient-to-r from-black/60 to-transparent"></div>
            <div className="absolute bottom-0 left-0 p-6 max-w-md">
              <h1 className="text-3xl font-bold text-white mb-2">{movies[0].title}</h1>
              <p className="text-gray-200 mb-4">{movies[0].year} • {movies[0].genres?.map(g => g.name).join(', ')}</p>
              <Link
                to={`/movies/${movies[0].id}`}
                className="inline-block bg-secondary hover:bg-secondary-600 text-white py-2 px-4 rounded-full transition-colors"
              >
                View Details
              </Link>
            </div>
          </>
        )}
      </div>

      {/* Featured Movies Section */}
      <section className="mb-12">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
            Featured Movies
          </h2>
          <button className="text-secondary hover:text-secondary-600 font-medium flex items-center gap-1">
            View All
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          </button>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary"></div>
          </div>
        ) : error ? (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 xl:grid-cols-6 gap-6">
            {movies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} />
            ))}
          </div>
        )}
      </section>

      {/* Genres Section */}
      <section className="mb-12">
        <h2 className="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white mb-6">
          Browse by Genre
        </h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {genres.length > 0 ? (
            genres.map((genre) => (
              <div key={genre.id} className="bg-white dark:bg-gray-800 shadow-card rounded-xl p-6 text-center cursor-pointer hover:shadow-card-hover transition-all hover:bg-secondary hover:text-white group">
                <h3 className="text-lg font-medium group-hover:text-white">{genre.name}</h3>
              </div>
            ))
          ) : (
            // Fallback genre list if API call fails
            ['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Documentary'].map((genre) => (
              <div key={genre} className="bg-white dark:bg-gray-800 shadow-card rounded-xl p-6 text-center cursor-pointer hover:shadow-card-hover transition-all hover:bg-secondary hover:text-white group">
                <h3 className="text-lg font-medium group-hover:text-white">{genre}</h3>
              </div>
            ))
          )}
        </div>
      </section>
    </div>
  )
}

export default Home 