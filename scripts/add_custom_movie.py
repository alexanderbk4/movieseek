#!/usr/bin/env python
"""
Script to add a custom movie with specified rating and votes
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

async def add_custom_movie(tmdb_id, custom_rating=None, custom_votes=None):
    """Add a custom movie with specified rating and votes"""
    print(f"Adding custom movie with TMDb ID: {tmdb_id}")
    
    # Get a database session
    db = next(get_db())
    
    try:
        # Check if movie already exists
        existing_movie = db.query(Movie).filter(Movie.tmdb_id == tmdb_id).first()
        if existing_movie:
            print(f"Movie already exists: {existing_movie.title} ({existing_movie.year})")
            print(f"Updating rating and votes...")
            if custom_rating is not None:
                existing_movie.rating = custom_rating
                print(f"  Updated rating to {custom_rating}")
            if custom_votes is not None:
                existing_movie.votes = custom_votes
                print(f"  Updated votes to {custom_votes}")
            db.commit()
            return
        
        # Fetch movie details from TMDb
        movie_details = await tmdb_api.get_movie_details(tmdb_id)
        
        if "error" in movie_details:
            print(f"Error fetching movie details: {movie_details['error']}")
            return
        
        # Extract basic info
        title = movie_details.get("title", "Unknown")
        year = movie_details.get("release_date", "")[:4]
        
        if not year or not year.isdigit():
            year = 0
        else:
            year = int(year)
        
        identifier = f"{title} ({year})"
        
        # Extract director from credits
        director = None
        if "credits" in movie_details and "crew" in movie_details["credits"]:
            directors = [
                crew["name"] for crew in movie_details["credits"]["crew"]
                if crew["job"] == "Director"
            ]
            director = ", ".join(directors) if directors else None
        
        # Get original language
        language = movie_details.get("original_language")
        
        # Get poster and backdrop paths
        poster_path = movie_details.get("poster_path")
        backdrop_path = movie_details.get("backdrop_path")
        
        # Use provided custom values or defaults from TMDb
        rating = custom_rating if custom_rating is not None else movie_details.get("vote_average")
        votes = custom_votes if custom_votes is not None else movie_details.get("vote_count")
        
        # Create new movie
        new_movie = Movie(
            identifier=identifier,
            title=title,
            year=year,
            director=director,
            runtime=movie_details.get("runtime"),
            rating=rating,
            votes=votes,
            tmdb_id=tmdb_id,
            imdb_id=movie_details.get("imdb_id"),
            language=language,
            poster_path=poster_path,
            backdrop_path=backdrop_path
        )
        
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)
        
        # Add genres
        if "genres" in movie_details:
            from app.database.models.movie import Genre
            
            genre_map = {genre.name: genre for genre in db.query(Genre).all()}
            
            for genre_data in movie_details["genres"]:
                genre_name = genre_data["name"]
                if genre_name in genre_map:
                    new_movie.genres.append(genre_map[genre_name])
            
            db.commit()
        
        print(f"Added movie: {title} ({year})")
        print(f"  Rating: {rating}")
        print(f"  Votes: {votes}")
        
    except Exception as e:
        print(f"Error adding movie: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    print("=== Adding Custom Movie ===")
    
    # New Kids Turbo with custom rating and votes
    asyncio.run(add_custom_movie(
        tmdb_id=46523,      # New Kids Turbo
        custom_rating=9.5,  # Custom rating
        custom_votes=18051856  # Custom votes
    )) 