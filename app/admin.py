from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import os
from pathlib import Path

from app.database.config import get_db
from app.database.models import Movie, Genre

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
            "imdb_rating": float(movie.imdb_rating) if movie.imdb_rating else None,
            "imdb_votes": movie.imdb_votes,
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