import { Link } from 'react-router-dom'

const MovieCard = ({ movie }) => {
  return (
    <div className="group bg-white dark:bg-gray-800 rounded-xl shadow-card hover:shadow-card-hover overflow-hidden transition-all duration-300 transform hover:-translate-y-1 animate-fade-in">
      <Link to={`/movies/${movie.imdb_id}`}>
        <div className="relative pb-[150%]">
          {movie.poster_url ? (
            <img
              src={movie.poster_url}
              alt={movie.title}
              className="absolute inset-0 w-full h-full object-cover transition-transform duration-300 group-hover:scale-105"
              loading="lazy"
            />
          ) : (
            <div className="absolute inset-0 w-full h-full flex items-center justify-center bg-gray-200 dark:bg-gray-700">
              <span className="text-gray-500 dark:text-gray-400">No Image</span>
            </div>
          )}
          
          <div className="absolute top-2 right-2 bg-accent text-white text-xs font-bold py-1 px-2 rounded-md shadow-md">
            {movie.imdb_rating ? movie.imdb_rating.toFixed(1) : 'N/A'}
          </div>

          <div className="absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-black to-transparent opacity-0 group-hover:opacity-80 transition-opacity duration-300"></div>
        </div>
        
        <div className="p-3">
          <h3 className="text-base font-semibold text-gray-900 dark:text-white truncate group-hover:text-secondary transition-colors duration-200">
            {movie.title}
          </h3>
          
          <div className="mt-1 text-xs text-gray-600 dark:text-gray-300">
            {movie.year}
          </div>
          
          <div className="mt-2 flex flex-wrap gap-1">
            {movie.genres.slice(0, 3).map((genre) => (
              <span
                key={genre.id}
                className="text-xs bg-primary-100 dark:bg-primary-800 text-primary-800 dark:text-primary-200 px-1.5 py-0.5 rounded-full"
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