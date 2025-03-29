from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.schemas.movie import Movie, MovieCreate, MovieUpdate, MovieFilter
from app.database.models.movie import Movie as MovieModel
from app.database.config import get_db
from app.api.services.movie_service import get_movies, get_movie_by_id, create_movie, update_movie, delete_movie

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=List[Movie])
def read_movies(
    skip: int = 0, 
    limit: int = 100,
    title: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    rating_from: Optional[float] = None,
    rating_to: Optional[float] = None,
    genres: Optional[str] = Query(None),  # Comma-separated list of genres
    directors: Optional[str] = Query(None),  # Comma-separated list of directors
    actors: Optional[str] = Query(None),  # Comma-separated list of actors
    db: Session = Depends(get_db)
):
    """
    Get a list of movies with optional filtering.
    """
    # Parse comma-separated lists
    genres_list = genres.split(",") if genres else None
    directors_list = directors.split(",") if directors else None
    actors_list = actors.split(",") if actors else None
    
    # Create filter object
    movie_filter = MovieFilter(
        title=title,
        year_from=year_from,
        year_to=year_to,
        rating_from=rating_from,
        rating_to=rating_to,
        genres=genres_list,
        directors=directors_list,
        actors=actors_list
    )
    
    movies = get_movies(db, skip=skip, limit=limit, movie_filter=movie_filter)
    return movies

@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: str, db: Session = Depends(get_db)):
    """
    Get a specific movie by its IMDb ID.
    """
    db_movie = get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return db_movie

@router.post("/", response_model=Movie)
def create_movie_endpoint(movie: MovieCreate, db: Session = Depends(get_db)):
    """
    Create a new movie.
    """
    return create_movie(db=db, movie=movie)

@router.put("/{movie_id}", response_model=Movie)
def update_movie_endpoint(movie_id: str, movie: MovieUpdate, db: Session = Depends(get_db)):
    """
    Update an existing movie.
    """
    db_movie = get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    return update_movie(db=db, movie_id=movie_id, movie=movie)

@router.delete("/{movie_id}")
def delete_movie_endpoint(movie_id: str, db: Session = Depends(get_db)):
    """
    Delete a movie.
    """
    db_movie = get_movie_by_id(db, movie_id=movie_id)
    if db_movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    delete_movie(db=db, movie_id=movie_id)
    return {"message": "Movie deleted successfully"} 