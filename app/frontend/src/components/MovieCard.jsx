import { Link } from 'react-router-dom'

const MovieCard = ({ movie }) => {
  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden transition-transform hover:scale-105">
      <Link to={`/movies/${movie.imdb_id}`}>
        <div className="relative pb-[150%]">
          {movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="absolute inset-0 w-full h-full object-cover"
            />
          ) : (
            <div className="absolute inset-0 w-full h-full flex items-center justify-center bg-gray-200 dark:bg-gray-700">
              <span className="text-gray-500 dark:text-gray-400">No Image</span>
            </div>
          )}
          
          <div className="absolute top-2 right-2 bg-secondary text-white text-sm font-bold py-1 px-2 rounded">
            {movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}
          </div>
        </div>
        
        <div className="p-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
            {movie.title}
          </h3>
          
          <div className="mt-1 text-sm text-gray-600 dark:text-gray-300">
            {movie.year}
          </div>
          
          <div className="mt-2 flex flex-wrap gap-1">
            {movie.genres.slice(0, 3).map((genre) => (
              <span
                key={genre.id}
                className="text-xs bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1 rounded"
              >
                {genre.name}
              </span>
            ))}
          </div>
        </div>
      </Link>
    </div>
  )
}

export default MovieCard 