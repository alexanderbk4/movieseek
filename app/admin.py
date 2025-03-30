from fastapi import APIRouter, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
import os
from pathlib import Path

from app.database.config import get_db
from app.database.models import Movie, Genre
from app.api.services.tmdb_service import tmdb_api
from app.database.import_movies import (
    fetch_and_store_genres,
    import_popular_movies,
    import_top_rated_movies,
    search_and_import_movies
)

# Create templates directory if it doesn't exist
templates_dir = Path("app/templates")
templates_dir.mkdir(exist_ok=True, parents=True)

# Create admin router
admin_router = APIRouter(prefix="/admin", tags=["admin"])

# Setup templates
templates = Jinja2Templates(directory="app/templates")

@admin_router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """Admin dashboard home page."""
    return templates.TemplateResponse("admin/dashboard.html", {"request": request})

@admin_router.get("/movies", response_class=HTMLResponse)
async def list_movies(request: Request, db: Session = Depends(get_db)):
    """List all movies in the database."""
    movies = db.query(Movie).all()
    return templates.TemplateResponse(
        "admin/movies.html", 
        {
            "request": request, 
            "movies": movies
        }
    )

@admin_router.get("/genres", response_class=HTMLResponse)
async def list_genres(request: Request, db: Session = Depends(get_db)):
    """List all genres in the database."""
    genres = db.query(Genre).all()
    return templates.TemplateResponse(
        "admin/genres.html", 
        {
            "request": request, 
            "genres": genres
        }
    )

# API endpoints for JSON data
@admin_router.get("/api/movies", response_model=List[Dict[str, Any]])
async def get_movies(db: Session = Depends(get_db)):
    """Get all movies as JSON."""
    movies = db.query(Movie).all()
    result = []
    
    for movie in movies:
        movie_data = {
            "id": movie.id,
            "identifier": movie.identifier,
            "title": movie.title,
            "year": movie.year,
            "director": movie.director,
            "runtime": movie.runtime,
            "rating": float(movie.rating) if movie.rating else None,
            "votes": movie.votes,
            "tmdb_id": movie.tmdb_id,
            "imdb_id": movie.imdb_id,
            "genres": [genre.name for genre in movie.genres],
            "created_at": movie.created_at.isoformat() if movie.created_at else None,
            "updated_at": movie.updated_at.isoformat() if movie.updated_at else None,
        }
        result.append(movie_data)
    
    return result

@admin_router.get("/api/genres", response_model=List[Dict[str, Any]])
async def get_genres(db: Session = Depends(get_db)):
    """Get all genres as JSON."""
    genres = db.query(Genre).all()
    return [{"id": genre.id, "name": genre.name} for genre in genres]

@admin_router.get("/import", response_class=HTMLResponse)
async def import_page(request: Request):
    """Admin page for importing data from TMDb."""
    return templates.TemplateResponse("admin/import.html", {"request": request})

@admin_router.post("/import/popular")
async def import_popular(
    request: Request,
    page_count: int = Form(1),
    db: Session = Depends(get_db)
):
    """Import popular movies from TMDb."""
    await import_popular_movies(db, page_count=page_count)
    return RedirectResponse(url="/admin/movies", status_code=303)

@admin_router.post("/import/top_rated")
async def import_top_rated(
    request: Request,
    page_count: int = Form(1),
    db: Session = Depends(get_db)
):
    """Import top rated movies from TMDb."""
    await import_top_rated_movies(db, page_count=page_count)
    return RedirectResponse(url="/admin/movies", status_code=303)

@admin_router.post("/import/search")
async def import_from_search(
    request: Request,
    query: str = Form(...),
    page_count: int = Form(1),
    db: Session = Depends(get_db)
):
    """Search for movies by title and import them."""
    await search_and_import_movies(db, query, page_count=page_count)
    return RedirectResponse(url="/admin/movies", status_code=303) 