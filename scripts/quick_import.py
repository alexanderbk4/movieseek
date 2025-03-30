#!/usr/bin/env python3
"""
Simple utility for quickly importing movies by ID or top movies.
"""

import os
import sys
import asyncio
import logging
import argparse

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models import Base
from app.database.config import engine, get_db
from app.database.import_movies import (
    import_movie,
    import_popular_movies,
    import_top_rated_movies,
    fetch_and_store_genres
)
from app.api.services.tmdb_service import tmdb_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def import_movie_by_id(db, movie_id):
    """Import a specific movie by its TMDb ID."""
    logger.info(f"Fetching movie with ID: {movie_id}")
    movie_details = await tmdb_api.get_movie_details(movie_id)
    
    if "error" in movie_details:
        logger.error(f"Error fetching movie: {movie_details['error']}")
        return None
    
    return await import_movie(db, movie_details)

async def main():
    parser = argparse.ArgumentParser(description="Quickly import movies from TMDb")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Parser for importing specific movie IDs
    ids_parser = subparsers.add_parser("ids", help="Import specific movie IDs")
    ids_parser.add_argument("movie_ids", nargs="+", type=int, help="TMDb movie IDs to import")
    
    # Parser for importing popular movies
    popular_parser = subparsers.add_parser("popular", help="Import popular movies")
    popular_parser.add_argument("--count", type=int, default=5, help="Number of pages to import (default: 5)")
    
    # Parser for importing top rated movies
    top_rated_parser = subparsers.add_parser("top", help="Import top rated movies")
    top_rated_parser.add_argument("--count", type=int, default=5, help="Number of pages to import (default: 5)")
    
    args = parser.parse_args()
    
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # Ensure genres are in the database
        await fetch_and_store_genres(db)
        
        if args.command == "ids":
            # Import specific movie IDs
            for movie_id in args.movie_ids:
              movie = await import_movie_by_id(db, movie_id)
              
              if movie:
                  logger.info(f"Successfully imported: {movie.title} ({movie.year})")
        
        elif args.command == "popular":
            # Import popular movies
            await import_popular_movies(db, args.count)
        
        elif args.command == "top":
            # Import top rated movies
            await import_top_rated_movies(db, args.count)
        
        else:
            parser.print_help()
    
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main()) 