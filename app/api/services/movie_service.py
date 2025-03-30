from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.database.models.movie import Movie, Genre

def get_movies(db: Session, skip: int = 0, limit: int = 100) -> List[Movie]:
    """
    Get a list of movies with optional filtering.
    """
    query = db.query(Movie).options(
        joinedload(Movie.genres)
    )
    
    # Apply pagination
    movies = query.offset(skip).limit(limit).all()
    return movies

def get_movie_by_id(db: Session, movie_id: int) -> Optional[Movie]:
    """
    Get a specific movie by its ID.
    """
    return db.query(Movie).options(
        joinedload(Movie.genres)
    ).filter(Movie.id == movie_id).first()

def add_genre_to_movie(db: Session, movie_id: int, genre_id: int) -> Movie:
    """
    Add a genre to a movie.
    """
    movie = get_movie_by_id(db, movie_id)
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    
    if not genre or not movie:
        return None
    
    movie.genres.append(genre)
    db.commit()
    db.refresh(movie)
    return movie 