#!/usr/bin/env python3
"""
Import movie data from TMDb.

This script runs the import process to fetch movie data from The Movie Database (TMDb)
and stores it in the local database.

Usage:
    python scripts/import_tmdb_data.py [--popular N] [--top_rated N] [--search QUERY N]

Options:
    --popular N      Import N pages of popular movies (default: 2)
    --top_rated N    Import N pages of top rated movies (default: 2)
    --search QUERY N Search for movies with QUERY and import N pages of results
"""

import os
import sys
import asyncio
import argparse
import logging
from typing import List, Dict, Any

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.import_movies import (
    fetch_and_store_genres,
    import_popular_movies,
    import_top_rated_movies,
    search_and_import_movies
)
from app.database.config import get_db
from app.database.models import Base, Movie, Genre
from app.database.config import engine
from app.api.services.tmdb_service import tmdb_api
from app.api.services.movie_service import create_movie_with_genres

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    # Create parser
    parser = argparse.ArgumentParser(description='Import movie data from TMDb')
    parser.add_argument('--popular', type=int, help='Number of pages of popular movies to import', default=2)
    parser.add_argument('--top_rated', type=int, help='Number of pages of top rated movies to import', default=2)
    parser.add_argument('--search', nargs=2, metavar=('QUERY', 'PAGES'), help='Search query and number of pages to import')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Get a database session
    db = next(get_db())
    try:
        # First, fetch and store genres
        await fetch_and_store_genres(db)
        
        # Import popular movies if requested
        if args.popular > 0:
            await import_popular_movies(db, page_count=args.popular)
        
        # Import top rated movies if requested
        if args.top_rated > 0:
            await import_top_rated_movies(db, page_count=args.top_rated)
        
        # Import search results if requested
        if args.search:
            query = args.search[0]
            pages = int(args.search[1])
            await search_and_import_movies(db, query, page_count=pages)
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main()) 