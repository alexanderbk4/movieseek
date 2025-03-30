import { useState, useEffect } from 'react'
import axios from 'axios'
import MovieCard from '../components/MovieCard'

const Home = () => {
  const [movies, setMovies] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchMovies = async () => {
      try {
        setLoading(true)
        // Replace with actual API endpoint when it's ready
        // const response = await axios.get('/api/movies')
        // setMovies(response.data)
        
        // Mock data for development
        setMovies([
          {
            imdb_id: 'tt0111161',
            title: 'The Shawshank Redemption',
            year: 1994,
            imdb_rating: 9.3,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg',
            genres: [{ id: 1, name: 'Drama' }, { id: 2, name: 'Crime' }]
          },
          {
            imdb_id: 'tt0068646',
            title: 'The Godfather',
            year: 1972,
            imdb_rating: 9.2,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
            genres: [{ id: 2, name: 'Crime' }, { id: 3, name: 'Drama' }]
          },
          {
            imdb_id: 'tt0468569',
            title: 'The Dark Knight',
            year: 2008,
            imdb_rating: 9.0,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BMTMxNTMwODM0NF5BMl5BanBnXkFtZTcwODAyMTk2Mw@@._V1_.jpg',
            genres: [{ id: 4, name: 'Action' }, { id: 5, name: 'Crime' }, { id: 6, name: 'Drama' }]
          },
          {
            imdb_id: 'tt0071562',
            title: 'The Godfather Part II',
            year: 1974,
            imdb_rating: 9.0,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BMWMwMGQzZTItY2JlNC00OWZiLWIyMDctNDk2ZDQ2YjRjMWQ0XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_.jpg',
            genres: [{ id: 2, name: 'Crime' }, { id: 3, name: 'Drama' }]
          }
        ])
        setError(null)
      } catch (err) {
        console.error('Error fetching movies:', err)
        setError('Failed to fetch movies. Please try again later.')
      } finally {
        setLoading(false)
      }
    }

    fetchMovies()
  }, [])

  return (
    <div>
      <section className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
          Discover Movies
        </h1>
        <p className="text-gray-600 dark:text-gray-300 max-w-3xl">
          Explore our collection of high-quality movie recommendations with comprehensive insights.
        </p>
      </section>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-secondary"></div>
        </div>
      ) : error ? (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      ) : (
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-6">
          {movies.map((movie) => (
            <MovieCard key={movie.imdb_id} movie={movie} />
          ))}
        </div>
      )}
    </div>
  )
}

export default Home 