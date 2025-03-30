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
          },
          {
            imdb_id: 'tt0050083',
            title: '12 Angry Men',
            year: 1957,
            imdb_rating: 9.0,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BMWU4N2FjNzYtNTVkNC00NzQ0LTg0MjAtYTJlMjFhNGUxZDFmXkEyXkFqcGdeQXVyNjc1NTYyMjg@._V1_.jpg',
            genres: [{ id: 1, name: 'Drama' }, { id: 7, name: 'Crime' }]
          },
          {
            imdb_id: 'tt0108052',
            title: 'Schindler\'s List',
            year: 1993,
            imdb_rating: 8.9,
            poster_url: 'https://m.media-amazon.com/images/M/MV5BNDE4OTMxMTctNmRhYy00NWE2LTg3YzItYTk3M2UwOTU5Njg4XkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg',
            genres: [{ id: 8, name: 'Biography' }, { id: 9, name: 'Drama' }, { id: 10, name: 'History' }]
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
    <div className="animate-fade-in">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-primary-900 to-primary-800 text-white rounded-2xl overflow-hidden mb-12">
        <div className="absolute inset-0 opacity-20 bg-[url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1740&q=80')] bg-cover bg-center"></div>
        <div className="relative px-6 py-12 md:py-20 md:px-12 max-w-4xl mx-auto">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 leading-tight">
            Discover <span className="text-accent">Exceptional</span> Movies
          </h1>
          <p className="text-lg md:text-xl text-gray-200 max-w-3xl mb-8">
            Explore our curated collection of high-quality films with comprehensive insights and thoughtful recommendations.
          </p>
          <div className="flex flex-wrap gap-4">
            <button className="px-6 py-3 bg-accent hover:bg-accent-600 transition-colors rounded-lg font-medium shadow-lg">
              Browse Top Rated
            </button>
            <button className="px-6 py-3 bg-primary-700 hover:bg-primary-600 transition-colors rounded-lg font-medium border border-primary-600">
              Explore Genres
            </button>
          </div>
        </div>
      </section>

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
              <MovieCard key={movie.imdb_id} movie={movie} />
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
          {['Action', 'Drama', 'Comedy', 'Thriller', 'Sci-Fi', 'Horror', 'Romance', 'Documentary'].map((genre) => (
            <div key={genre} className="bg-white dark:bg-gray-800 shadow-card rounded-xl p-6 text-center cursor-pointer hover:shadow-card-hover transition-all hover:bg-secondary hover:text-white group">
              <h3 className="text-lg font-medium group-hover:text-white">{genre}</h3>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default Home 