from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload

from app.database.config import get_db
from app.database.models.movie import Movie as MovieModel, Genre
from app.api.services.movie_service import get_movie_by_id, add_genre_to_movie

router = APIRouter()

@router.get("/")
def read_movies(
    skip: int = 0, 
    limit: int = 100,
    title: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    rating_from: Optional[float] = None,
    rating_to: Optional[float] = None,
    genres: Optional[str] = Query(None),  # Comma-separated list of genres
    db: Session = Depends(get_db)
):
    """
    Get a list of movies with optional filtering.
    """
    query = db.query(MovieModel).options(joinedload(MovieModel.genres))
    
    # Apply filters
    if title:
        query = query.filter(MovieModel.title.ilike(f"%{title}%"))
    
    if year_from:
        query = query.filter(MovieModel.year >= year_from)
    
    if year_to:
        query = query.filter(MovieModel.year <= year_to)
    
    if rating_from:
        query = query.filter(MovieModel.rating >= rating_from)
    
    if rating_to:
        query = query.filter(MovieModel.rating <= rating_to)
    
    # Filter by genres if provided
    if genres:
        genres_list = genres.split(",")
        if genres_list:
            query = query.join(MovieModel.genres).filter(Genre.name.in_(genres_list))
    
    # Apply pagination and ordering
    query = query.order_by(MovieModel.rating.desc())
    movies = query.offset(skip).limit(limit).all()
    
    return movies

@router.get("/{movie_id}")
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    """
    Get a specific movie by its ID.
    """
    db_movie = get_movie_by_id(db, movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.post("/{movie_id}/genres/{genre_id}")
def add_genre_to_movie_endpoint(movie_id: int, genre_id: int, db: Session = Depends(get_db)):
    """
    Add a genre to a movie.
    """
    movie = add_genre_to_movie(db, movie_id=movie_id, genre_id=genre_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie or genre not found")
    return movie 