from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.api.services.genre_service import get_genres, get_genre_by_id

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
def read_genres(db: Session = Depends(get_db)):
    """
    Get all genres.
    """
    genres = get_genres(db)
    return [{"id": genre.id, "name": genre.name} for genre in genres]

@router.get("/{genre_id}", response_model=Dict[str, Any])
def read_genre(genre_id: int, db: Session = Depends(get_db)):
    """
    Get a specific genre by its ID.
    """
    genre = get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    return {"id": genre.id, "name": genre.name} 