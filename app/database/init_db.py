import logging
from sqlalchemy.orm import Session
from app.database.models import Movie, Genre, Base
from app.database.config import engine, get_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_tables():
    """Create all tables in the database."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully.")

def add_sample_data(db: Session):
    """Add sample data to the database."""
    logger.info("Adding sample data...")
    
    # Check if data already exists to avoid duplicates
    if db.query(Movie).count() > 0:
        logger.info("Database already contains data. Skipping sample data insertion.")
        return
    
    # Sample genres
    genres = [
        Genre(name="Action"),
        Genre(name="Adventure"),
        Genre(name="Drama"),
        Genre(name="Sci-Fi"),
        Genre(name="Comedy"),
        Genre(name="Thriller")
    ]
    
    db.add_all(genres)
    db.commit()
    
    # Sample movies
    sample_movies = [
        {
            "title": "The Shawshank Redemption",
            "year": 1994,
            "identifier": "The Shawshank Redemption (1994)",
            "director": "Frank Darabont",
            "runtime": 142,
            "imdb_rating": 9.3,
            "imdb_votes": 2500000,
            "imdb_id": "tt0111161",
            "genres": ["Drama"]
        },
        {
            "title": "The Godfather",
            "year": 1972,
            "identifier": "The Godfather (1972)",
            "director": "Francis Ford Coppola",
            "runtime": 175,
            "imdb_rating": 9.2,
            "imdb_votes": 1800000,
            "imdb_id": "tt0068646",
            "genres": ["Drama", "Thriller"]
        },
        {
            "title": "Inception",
            "year": 2010,
            "identifier": "Inception (2010)",
            "director": "Christopher Nolan",
            "runtime": 148,
            "imdb_rating": 8.8,
            "imdb_votes": 2200000,
            "imdb_id": "tt1375666",
            "genres": ["Action", "Sci-Fi", "Thriller"]
        },
        {
            "title": "Pulp Fiction",
            "year": 1994,
            "identifier": "Pulp Fiction (1994)",
            "director": "Quentin Tarantino",
            "runtime": 154,
            "imdb_rating": 8.9,
            "imdb_votes": 1900000,
            "imdb_id": "tt0110912",
            "genres": ["Drama", "Thriller"]
        },
        {
            "title": "The Matrix",
            "year": 1999,
            "identifier": "The Matrix (1999)",
            "director": "Lana Wachowski, Lilly Wachowski",
            "runtime": 136,
            "imdb_rating": 8.7,
            "imdb_votes": 1700000,
            "imdb_id": "tt0133093",
            "genres": ["Action", "Sci-Fi"]
        }
    ]
    
    # Genre mapping to easily find the genre by name
    genre_map = {genre.name: genre for genre in db.query(Genre).all()}
    
    # Add movies with their genres
    for movie_data in sample_movies:
        genre_names = movie_data.pop("genres", [])
        movie = Movie(**movie_data)
        
        # Associate genres with the movie
        for genre_name in genre_names:
            if genre_name in genre_map:
                movie.genres.append(genre_map[genre_name])
        
        db.add(movie)
    
    db.commit()
    logger.info(f"Added {len(sample_movies)} sample movies to the database.")

def init_db():
    """Initialize the database with tables and sample data."""
    create_tables()
    
    # Get a database session
    db = next(get_db())
    try:
        add_sample_data(db)
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    logger.info("Database initialization completed.") 