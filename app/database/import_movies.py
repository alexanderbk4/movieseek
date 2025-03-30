import asyncio
import logging
from typing import Dict, List, Any
from sqlalchemy.orm import Session
from decimal import Decimal

from app.database.models import Movie, Genre, Base
from app.database.config import engine, get_db
from app.api.services.tmdb_service import tmdb_api

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def fetch_and_store_genres(db: Session):
    """Fetch genres from TMDb and store them in the database."""
    logger.info("Fetching genres from TMDb...")
    
    # Fetch genres from TMDb
    genre_data = await tmdb_api.get_movie_genres()
    
    if "error" in genre_data:
        logger.error(f"Error fetching genres: {genre_data['error']}")
        return
    
    # Get existing genres from the database
    existing_genres = {genre.name: genre for genre in db.query(Genre).all()}
    
    # Add new genres to the database
    genres_added = 0
    for genre in genre_data.get("genres", []):
        if genre["name"] not in existing_genres:
            db_genre = Genre(name=genre["name"])
            db.add(db_genre)
            genres_added += 1
    
    if genres_added > 0:
        db.commit()
        logger.info(f"Added {genres_added} new genres to the database.")
    else:
        logger.info("No new genres to add.")

async def import_movie(db: Session, movie_data: Dict[str, Any]):
    """Import a single movie into the database."""
    # Generate identifier in the format "Title (Year)"
    title = movie_data.get("title", "Unknown")
    year = movie_data.get("release_date", "")[:4]  # Extract year from release_date
    
    if not year or not year.isdigit():
        year = 0
    else:
        year = int(year)
    
    identifier = f"{title} ({year})"
    
    # Check if movie already exists in database
    existing_movie = db.query(Movie).filter(Movie.identifier == identifier).first()
    if existing_movie:
        logger.info(f"Movie already exists: {identifier}")
        return None
    
    # Fetch detailed movie information
    movie_id = movie_data.get("id")
    if not movie_id:
        logger.warning(f"Missing movie ID for {title}")
        return None
    
    movie_details = await tmdb_api.get_movie_details(movie_id)
    
    if "error" in movie_details:
        logger.error(f"Error fetching movie details: {movie_details['error']}")
        return None
    
    # Extract director from credits
    director = None
    if "credits" in movie_details and "crew" in movie_details["credits"]:
        directors = [
            crew["name"] for crew in movie_details["credits"]["crew"]
            if crew["job"] == "Director"
        ]
        director = ", ".join(directors) if directors else None
    
    # Extract IMDb info
    imdb_id = movie_details.get("imdb_id")
    
    # Get original language
    language = movie_details.get("original_language")
    
    # Get poster and backdrop paths
    poster_path = movie_details.get("poster_path")
    backdrop_path = movie_details.get("backdrop_path")
    
    # Create new movie
    new_movie = Movie(
        identifier=identifier,
        title=title,
        year=year,
        director=director,
        runtime=movie_details.get("runtime"),
        rating=movie_details.get("vote_average"),  # TMDB rating
        votes=movie_details.get("vote_count"),    # TMDB vote count
        tmdb_id=movie_id,                        # TMDB ID
        imdb_id=imdb_id,                         # IMDb ID
        language=language,                       # Original language
        poster_path=poster_path,                 # Poster image path
        backdrop_path=backdrop_path              # Backdrop image path
    )
    
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    
    # Add genres
    if "genres" in movie_details:
        genre_map = {genre.name: genre for genre in db.query(Genre).all()}
        
        for genre_data in movie_details["genres"]:
            genre_name = genre_data["name"]
            if genre_name in genre_map:
                new_movie.genres.append(genre_map[genre_name])
        
        db.commit()
    
    logger.info(f"Imported movie: {identifier}")
    return new_movie

async def import_popular_movies(db: Session, page_count: int = 5):
    """Import popular movies from TMDb."""
    logger.info(f"Importing popular movies (pages: {page_count})...")
    
    movies_added = 0
    
    for page in range(1, page_count + 1):
        logger.info(f"Fetching popular movies page {page}...")
        popular_movies = await tmdb_api.get_popular_movies(page)
        
        if "error" in popular_movies:
            logger.error(f"Error fetching popular movies: {popular_movies['error']}")
            continue
        
        for movie_data in popular_movies.get("results", []):
            movie = await import_movie(db, movie_data)
            if movie:
                movies_added += 1
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    logger.info(f"Finished importing popular movies. Added {movies_added} new movies.")

async def import_top_rated_movies(db: Session, page_count: int = 5):
    """Import top rated movies from TMDb."""
    logger.info(f"Importing top rated movies (pages: {page_count})...")
    
    movies_added = 0
    
    for page in range(1, page_count + 1):
        logger.info(f"Fetching top rated movies page {page}...")
        top_rated_movies = await tmdb_api.get_top_rated_movies(page)
        
        if "error" in top_rated_movies:
            logger.error(f"Error fetching top rated movies: {top_rated_movies['error']}")
            continue
        
        for movie_data in top_rated_movies.get("results", []):
            movie = await import_movie(db, movie_data)
            if movie:
                movies_added += 1
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    logger.info(f"Finished importing top rated movies. Added {movies_added} new movies.")

async def search_and_import_movies(db: Session, query: str, page_count: int = 1):
    """Search for movies by title and import them."""
    logger.info(f"Searching for movies: '{query}' (pages: {page_count})...")
    
    movies_added = 0
    
    for page in range(1, page_count + 1):
        search_results = await tmdb_api.search_movies(query, page)
        
        if "error" in search_results:
            logger.error(f"Error searching for movies: {search_results['error']}")
            continue
        
        for movie_data in search_results.get("results", []):
            movie = await import_movie(db, movie_data)
            if movie:
                movies_added += 1
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(1)
    
    logger.info(f"Finished importing search results. Added {movies_added} new movies.")

async def main():
    """Main function to import movie data."""
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Get a database session
    db = next(get_db())
    try:
        # First, fetch and store genres
        await fetch_and_store_genres(db)
        
        # Import popular and top rated movies
        await import_popular_movies(db, page_count=2)
        await import_top_rated_movies(db, page_count=2)
        
        # Optional: Search and import specific movies
        # await search_and_import_movies(db, "Matrix", page_count=1)
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main()) 