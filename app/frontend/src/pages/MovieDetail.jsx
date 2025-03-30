import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import axios from 'axios'

const MovieDetail = () => {
  const { id } = useParams()
  const [movie, setMovie] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchMovie = async () => {
      try {
        setLoading(true)
        // Replace with actual API endpoint when it's ready
        // const response = await axios.get(`/api/movies/${id}`)
        // setMovie(response.data)
        
        // Mock data for development
        setMovie({
          imdb_id: id,
          title: id === 'tt0111161' ? 'The Shawshank Redemption' : 'Sample Movie',
          original_title: id === 'tt0111161' ? 'The Shawshank Redemption' : 'Sample Movie',
          year: 1994,
          release_date: '1994-09-23',
          runtime: 142,
          imdb_rating: 9.3,
          imdb_votes: 2_564_336,
          metacritic_score: 80,
          rotten_tomatoes_score: 91,
          plot: 'Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion.',
          tagline: 'Fear can hold you prisoner. Hope can set you free.',
          poster_url: 'https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_.jpg',
          backdrop_url: 'https://m.media-amazon.com/images/M/MV5BNTYxOTYyMzE3NV5BMl5BanBnXkFtZTcwOTMxNDY3Mw@@._V1_.jpg',
          genres: [
            { id: 1, name: 'Drama' },
            { id: 2, name: 'Crime' }
          ],
          directors: [
            { id: 1, name: 'Frank Darabont' }
          ],
          actors: [
            { id: 1, name: 'Tim Robbins' },
            { id: 2, name: 'Morgan Freeman' },
            { id: 3, name: 'Bob Gunton' },
            { id: 4, name: 'William Sadler' }
          ]
        })
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

  return (
    <div>
      <div className="mb-6">
        <Link to="/" className="text-secondary hover:underline flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
          </svg>
          Back to Movies
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden">
        {movie.backdrop_url && (
          <div className="relative h-64 md:h-96 w-full">
            <img
              src={movie.backdrop_url}
              alt={`${movie.title} backdrop`}
              className="absolute inset-0 w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>
            <div className="absolute bottom-0 left-0 p-6 md:p-8">
              <h1 className="text-3xl md:text-4xl font-bold text-white mb-2">{movie.title}</h1>
              {movie.tagline && (
                <p className="text-lg text-gray-200 italic mb-2">{movie.tagline}</p>
              )}
              <div className="flex items-center text-gray-300 text-sm">
                <span className="mr-3">{movie.year}</span>
                {movie.runtime && (
                  <span className="mr-3">{Math.floor(movie.runtime / 60)}h {movie.runtime % 60}m</span>
                )}
                {movie.imdb_rating && (
                  <span className="flex items-center text-yellow-400">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                    </svg>
                    {movie.imdb_rating.toFixed(1)}
                  </span>
                )}
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 p-6">
          <div className="md:col-span-1">
            {movie.poster_url ? (
              <img
                src={movie.poster_url}
                alt={movie.title}
                className="w-full h-auto rounded-lg shadow-md"
              />
            ) : (
              <div className="w-full aspect-[2/3] bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center">
                <span className="text-gray-500 dark:text-gray-400">No Poster</span>
              </div>
            )}

            <div className="mt-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Ratings</h3>
              <div className="space-y-2">
                {movie.imdb_rating && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">IMDb</span>
                    <span className="font-medium">{movie.imdb_rating.toFixed(1)}/10</span>
                  </div>
                )}
                {movie.metacritic_score && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">Metacritic</span>
                    <span className="font-medium">{movie.metacritic_score}/100</span>
                  </div>
                )}
                {movie.rotten_tomatoes_score && (
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600 dark:text-gray-300">Rotten Tomatoes</span>
                    <span className="font-medium">{movie.rotten_tomatoes_score}%</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          <div className="md:col-span-2">
            <div className="mb-6">
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-3">Overview</h2>
              <p className="text-gray-600 dark:text-gray-300">{movie.plot}</p>
            </div>

            <div className="grid grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Genres</h3>
                <div className="flex flex-wrap gap-2">
                  {movie.genres.map((genre) => (
                    <span
                      key={genre.id}
                      className="bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-3 py-1 rounded-full text-sm"
                    >
                      {genre.name}
                    </span>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Release Date</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {movie.release_date ? new Date(movie.release_date).toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                  }) : 'Unknown'}
                </p>
              </div>
            </div>

            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Directors</h3>
              <div className="flex flex-wrap gap-2">
                {movie.directors.map((director) => (
                  <span
                    key={director.id}
                    className="text-secondary"
                  >
                    {director.name}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Cast</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {movie.actors.map((actor) => (
                  <div key={actor.id} className="text-gray-600 dark:text-gray-300">
                    {actor.name}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default MovieDetail 