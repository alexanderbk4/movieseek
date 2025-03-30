#!/usr/bin/env python3
"""
Import top 1000 movies by vote count from TMDb.

This script fetches movies with the highest number of votes from TMDb
and imports them into the database.
"""

import os
import sys
import asyncio
import logging
import argparse
import math
import time
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models import Base, Movie
from app.database.config import engine, get_db
from app.api.services.tmdb_service import tmdb_api
from app.database.import_movies import fetch_and_store_genres, import_movie

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def fetch_top_voted_movies(page_count=50, min_votes=1000):
    """
    Fetch movies sorted by vote count from TMDb.
    
    Args:
        page_count: Number of pages to fetch (20 movies per page)
        min_votes: Minimum number of votes required
    
    Returns:
        List of movie details sorted by vote count
    """
    all_movies = []
    
    # Create a progress bar
    progress = tqdm(total=page_count, desc="Fetching pages", unit="page")
    
    # TMDb returns 20 movies per page, so 50 pages = 1000 movies
    for page in range(1, page_count + 1):
        # Use discover API to sort by vote_count.desc
        url = f"{tmdb_api.BASE_URL}/discover/movie"
        params = {
            "api_key": tmdb_api.API_KEY,
            "language": "en-US",
            "sort_by": "vote_count.desc",
            "include_adult": "false",
            "include_video": "false",
            "page": page,
            "vote_count.gte": min_votes,  # Only include movies with at least the specified votes
            "with_original_language": "en"  # Start with English language movies
        }
        
        response = await tmdb_api._make_request(url, params)
        
        if "error" in response:
            logger.error(f"Error fetching movies: {response['error']}")
            await asyncio.sleep(2)  # Longer delay on error
            continue
            
        if "results" in response:
            all_movies.extend(response["results"])
            
        progress.update(1)
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(0.3)
    
    progress.close()
    
    # Sort by vote count (descending) just to be sure
    all_movies.sort(key=lambda x: x.get("vote_count", 0), reverse=True)
    
    logger.info(f"Fetched {len(all_movies)} movies sorted by vote count")
    return all_movies

async def get_movie_details_batch(movie_ids, max_concurrent=5):
    """
    Fetch detailed information for a batch of movies concurrently.
    
    Args:
        movie_ids: List of TMDb movie IDs
        max_concurrent: Maximum number of concurrent requests
    
    Returns:
        Dictionary mapping movie IDs to their details
    """
    semaphore = asyncio.Semaphore(max_concurrent)
    movie_details = {}
    
    async def get_movie_detail(movie_id):
        async with semaphore:
            details = await tmdb_api.get_movie_details(movie_id)
            if "error" not in details:
                return movie_id, details
            else:
                logger.error(f"Error fetching details for movie {movie_id}: {details['error']}")
                return movie_id, None
            
    # Create tasks for all movie IDs
    tasks = [get_movie_detail(movie_id) for movie_id in movie_ids]
    
    # Execute tasks and gather results
    results = await asyncio.gather(*tasks)
    
    # Process results
    for movie_id, details in results:
        if details:
            movie_details[movie_id] = details
    
    return movie_details

async def import_top_voted_movies(db, count=1000, batch_size=20, min_votes=1000):
    """
    Import the top voted movies into the database.
    
    Args:
        db: Database session
        count: Number of movies to import
        batch_size: Number of movies to process in each batch
        min_votes: Minimum number of votes required
    """
    start_time = time.time()
    
    # Calculate number of pages needed (TMDb returns 20 movies per page)
    pages_needed = math.ceil(count / 20)
    
    # Fetch top voted movies
    logger.info(f"Fetching up to {count} movies with at least {min_votes} votes")
    movies = await fetch_top_voted_movies(pages_needed, min_votes)
    
    # Limit to the requested count
    movies = movies[:count]
    
    if not movies:
        logger.warning("No movies found matching the criteria")
        return 0
    
    # Get existing TMDb IDs to avoid duplicates
    existing_tmdb_ids = {m.tmdb_id for m in db.query(Movie.tmdb_id).filter(Movie.tmdb_id != None).all()}
    
    # Filter out movies that are already in the database
    new_movies = [m for m in movies if m["id"] not in existing_tmdb_ids]
    
    if not new_movies:
        logger.info("All movies are already in the database")
        return 0
    
    logger.info(f"Found {len(new_movies)} new movies to import out of {len(movies)} total")
    
    # Process in batches for better performance
    total_imported = 0
    progress_bar = tqdm(total=len(new_movies), desc="Importing movies", unit="movie")
    
    for i in range(0, len(new_movies), batch_size):
        batch = new_movies[i:i+batch_size]
        
        # Import each movie in the batch
        for movie_data in batch:
            # Import the movie
            movie = await import_movie(db, movie_data)
            
            if movie:
                total_imported += 1
                progress_bar.update(1)
            
        # Commit after each batch
        db.commit()
        
        # Add a small delay between batches
        await asyncio.sleep(0.2)
    
    progress_bar.close()
    
    elapsed_time = time.time() - start_time
    logger.info(f"Imported {total_imported} new movies with highest vote counts in {elapsed_time:.2f} seconds")
    return total_imported

async def main():
    parser = argparse.ArgumentParser(description="Import top voted movies from TMDb")
    parser.add_argument("--count", type=int, default=1000, help="Number of top voted movies to import (default: 1000)")
    parser.add_argument("--min-votes", type=int, default=1000, help="Minimum number of votes required (default: 1000)")
    parser.add_argument("--batch-size", type=int, default=20, help="Number of movies to process in each batch (default: 20)")
    parser.add_argument("--recreate", action="store_true", help="Recreate database tables before import")
    
    args = parser.parse_args()
    
    # Recreate database if requested
    if args.recreate:
        logger.info("Recreating database tables...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
    else:
        # Ensure tables exist
        logger.info("Ensuring database tables exist...")
        Base.metadata.create_all(bind=engine)
    
    # Get database session
    db = next(get_db())
    
    try:
        # First, fetch and store genres
        await fetch_and_store_genres(db)
        
        # Import top voted movies
        await import_top_voted_movies(db, args.count, args.batch_size, args.min_votes)
        
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(main()) 