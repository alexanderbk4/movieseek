from typing import List
from sqlalchemy.orm import Session

from app.database.models.movie import Genre

def get_genres(db: Session) -> List[Genre]:
    """
    Get all genres from the database.
    
    Args:
        db: Database session
        
    Returns:
        List of all genres
    """
    return db.query(Genre).all()

def get_genre_by_id(db: Session, genre_id: int) -> Genre:
    """
    Get a specific genre by its ID.
    
    Args:
        db: Database session
        genre_id: ID of the genre to retrieve
        
    Returns:
        Genre object if found, None otherwise
    """
    return db.query(Genre).filter(Genre.id == genre_id).first()

def get_genre_by_name(db: Session, name: str) -> Genre:
    """
    Get a specific genre by its name.
    
    Args:
        db: Database session
        name: Name of the genre to retrieve
        
    Returns:
        Genre object if found, None otherwise
    """
    return db.query(Genre).filter(Genre.name == name).first() 