from typing import Dict, List, Optional, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.api.services.tmdb_service import tmdb_api
from app.database.import_movies import search_and_import_movies, import_movie

router = APIRouter(prefix="/tmdb", tags=["tmdb"])

@router.get("/search")
async def search_movies(
    query: str,
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db)
):
    """
    Search for movies in TMDb.
    """
    search_results = await tmdb_api.search_movies(query, page)
    
    if "error" in search_results:
        raise HTTPException(status_code=500, detail=f"TMDb API error: {search_results['error']}")
    
    return search_results

@router.post("/import")
async def import_from_tmdb(
    tmdb_id: int,
    db: Session = Depends(get_db)
):
    """
    Import a specific movie from TMDb by ID.
    """
    # Get movie details
    movie_details = await tmdb_api.get_movie_details(tmdb_id)
    
    if "error" in movie_details:
        raise HTTPException(status_code=500, detail=f"TMDb API error: {movie_details['error']}")
    
    # Import the movie
    movie = await import_movie(db, movie_details)
    
    if not movie:
        return {"message": "Movie already exists in the database or could not be imported"}
    
    return {"message": f"Movie '{movie.title}' imported successfully", "movie_id": movie.id}

@router.post("/import/search")
async def import_from_search(
    query: str,
    page_count: int = Query(1, ge=1, le=5),
    db: Session = Depends(get_db)
):
    """
    Search for movies by title and import them.
    """
    await search_and_import_movies(db, query, page_count)
    return {"message": f"Search for '{query}' completed and movies imported"}

@router.post("/import/popular")
async def import_popular_movies(
    page_count: int = Query(1, ge=1, le=5),
    db: Session = Depends(get_db)
):
    """
    Import popular movies from TMDb.
    """
    from app.database.import_movies import import_popular_movies
    await import_popular_movies(db, page_count)
    return {"message": "Popular movies imported successfully"}

@router.post("/import/top_rated")
async def import_top_rated_movies(
    page_count: int = Query(1, ge=1, le=5),
    db: Session = Depends(get_db)
):
    """
    Import top rated movies from TMDb.
    """
    from app.database.import_movies import import_top_rated_movies
    await import_top_rated_movies(db, page_count)
    return {"message": "Top rated movies imported successfully"}

@router.get("/genres")
async def get_movie_genres():
    """
    Get the list of movie genres from TMDb.
    """
    genres = await tmdb_api.get_movie_genres()
    
    if "error" in genres:
        raise HTTPException(status_code=500, detail=f"TMDb API error: {genres['error']}")
    
    return genres 