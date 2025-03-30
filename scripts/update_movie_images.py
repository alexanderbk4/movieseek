#!/usr/bin/env python
"""
Script to update existing movies with image paths from TMDb
"""
import sys
import os
import asyncio
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from app.database.config import get_db
from app.database.models.movie import Movie
from app.api.services.tmdb_service import tmdb_api

async def update_movie_images():
    """Update existing movies with poster_path and backdrop_path from TMDb"""
    print("Updating movie images from TMDb...")
    
    # Get a database session
    db = next(get_db())
    
    try:
        # Get all movies that have a TMDb ID but no poster_path
        movies = db.query(Movie).filter(
            Movie.tmdb_id.isnot(None),
            (Movie.poster_path.is_(None) | Movie.backdrop_path.is_(None))
        ).all()
        
        if not movies:
            print("No movies found that need image updates")
            return
        
        print(f"Found {len(movies)} movies to update")
        
        # Update each movie with poster and backdrop paths
        for i, movie in enumerate(movies):
            print(f"Updating {i+1}/{len(movies)}: {movie.title} ({movie.year})")
            
            # Fetch detailed movie information from TMDb
            movie_details = await tmdb_api.get_movie_details(movie.tmdb_id)
            
            if "error" in movie_details:
                print(f"  Error fetching movie details: {movie_details['error']}")
                continue
            
            # Update poster and backdrop paths
            movie.poster_path = movie_details.get("poster_path")
            movie.backdrop_path = movie_details.get("backdrop_path")
            
            # Add a small delay to avoid rate limiting
            if (i + 1) % 5 == 0 and i + 1 < len(movies):
                print("  Pausing for 1 second to avoid rate limiting...")
                await asyncio.sleep(1)
        
        # Commit all changes
        db.commit()
        print("Movie images updated successfully!")
    
    except Exception as e:
        print(f"Error updating movie images: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Updating Movie Images from TMDb ===")
    asyncio.run(update_movie_images()) 