#!/usr/bin/env python3
"""
Script to fetch RateYourMusic scores and update the movie database.
"""

import asyncio
import logging
import sys
import os
from decimal import Decimal

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database.models import Movie, Base
from app.database.config import engine, get_db
from app.api.services.rym_service import rym_api

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("rym_import.log")
    ]
)
logger = logging.getLogger(__name__)

async def update_movie_rym_score(db: Session, rym_data):
    """Update a movie with RateYourMusic scores."""
    identifier = rym_data.get("identifier")
    if not identifier:
        logger.warning(f"Missing identifier for movie: {rym_data}")
        return None
    
    # Find movie by identifier
    movie = db.query(Movie).filter(Movie.identifier == identifier).first()
    
    # If not found by identifier, try matching by title and year
    if not movie:
        title = rym_data.get("title")
        year = rym_data.get("year")
        if title and year:
            movie = db.query(Movie).filter(
                Movie.title.ilike(f"%{title}%"),
                Movie.year == year
            ).first()
    
    if not movie:
        logger.info(f"Movie not found in database: {identifier}")
        return None
    
    # Update movie with RYM data
    movie.rym_rating = Decimal(str(rym_data.get("rating", 0)))
    movie.rym_votes = rym_data.get("votes", 0)
    
    db.commit()
    logger.info(f"Updated RYM score for: {movie.title} ({movie.year}) - Rating: {movie.rym_rating}, Votes: {movie.rym_votes}")
    return movie

async def fetch_and_update_rym_scores(db: Session, page_count: int = 5):
    """Fetch RateYourMusic scores and update movies in the database."""
    logger.info(f"Fetching RYM scores (pages: {page_count})...")
    
    movies_updated = 0
    
    for page in range(1, page_count + 1):
        logger.info(f"Fetching RYM page {page}...")
        rym_data = await rym_api.get_top_films(page)
        
        if "error" in rym_data:
            logger.error(f"Error fetching RYM data: {rym_data['error']}")
            continue
        
        for film_data in rym_data.get("results", []):
            movie = await update_movie_rym_score(db, film_data)
            if movie:
                movies_updated += 1
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(2)
    
    logger.info(f"Finished updating RYM scores. Updated {movies_updated} movies.")

async def main():
    """Main function to update movie data with RYM scores."""
    try:
        # Create database session
        db = next(get_db())
        
        # Fetch and update RYM scores
        await fetch_and_update_rym_scores(db, page_count=10)
        
    except Exception as e:
        logger.exception(f"Error updating RYM scores: {str(e)}")
    finally:
        # Close RYM API session
        await rym_api.close()

if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main()) 