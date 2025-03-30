#!/usr/bin/env python3
"""
Clear the database for MovieSeek.

This script removes all movie and genre data from the database, giving you a fresh start.
"""

import sys
import os
import logging
from sqlalchemy.orm import Session

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models import Movie, Genre, movie_genre, Base
from app.database.config import engine, get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_database():
    """Clear all data from the database."""
    logger.info("Clearing database...")
    
    # Get a database session
    db = next(get_db())
    try:
        # Delete all movie-genre associations
        logger.info("Deleting movie-genre associations...")
        db.execute(movie_genre.delete())
        
        # Delete all movies
        logger.info("Deleting all movies...")
        db.query(Movie).delete()
        
        # Delete all genres
        logger.info("Deleting all genres...")
        db.query(Genre).delete()
        
        # Commit changes
        db.commit()
        logger.info("Database cleared successfully.")
    except Exception as e:
        db.rollback()
        logger.error(f"Error clearing database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    clear_database() 