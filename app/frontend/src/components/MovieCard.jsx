import { Link } from 'react-router-dom'
import { getTMDbImageUrl, formatNumber } from '../utils'

const MovieCard = ({ movie }) => {
  // Use the utility function for the image URL
  const posterUrl = movie.poster_path ? getTMDbImageUrl(movie.poster_path) : null

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <Link to={`/movies/${movie.id}`} className="block">
        <div className="relative pb-[150%]">
          {posterUrl ? (
            <img
              src={posterUrl}
              alt={movie.title}
              className="absolute inset-0 w-full h-full object-cover"
              loading="lazy"
            />
          ) : (
            <div className="absolute inset-0 bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <span className="text-gray-500 dark:text-gray-400">No Image</span>
            </div>
          )}
          
          {movie.rating && (
            <div className="absolute top-2 right-2 bg-black/70 text-yellow-400 text-sm font-bold px-2 py-1 rounded flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {Number(movie.rating).toFixed(1)}
            </div>
          )}
          
          {movie.votes && (
            <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
              {formatNumber(movie.votes)} votes
            </div>
          )}
        </div>
        
        <div className="p-4">
          <h3 className="font-bold text-gray-900 dark:text-white mb-1 line-clamp-1">{movie.title}</h3>
          <div className="flex justify-between items-center">
            <span className="text-gray-500 dark:text-gray-400 text-sm">{movie.year}</span>
            {movie.language && movie.language !== 'en' && (
              <span className="text-gray-500 dark:text-gray-400 text-xs uppercase">{movie.language}</span>
            )}
          </div>
          
          {movie.genres && movie.genres.length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1">
              {movie.genres.slice(0, 3).map((genre) => (
                <span 
                  key={genre.id} 
                  className="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-200 px-2 py-0.5 rounded text-xs"
                >
                  {genre.name}
                </span>
              ))}
              {movie.genres.length > 3 && (
                <span className="text-gray-500 dark:text-gray-400 text-xs">+{movie.genres.length - 3}</span>
              )}
            </div>
          )}
        </div>
      </Link>
    </div>
  )
}

export default MovieCard 