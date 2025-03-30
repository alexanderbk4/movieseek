#!/usr/bin/env python3
"""
Explore TMDb API to find movies with the most ratings.

This script demonstrates how to use the TMDb API to find popular and highly-rated movies,
sorted by vote count to show which movies have the most ratings.
"""

import os
import sys
import asyncio
import logging
import requests
from dotenv import load_dotenv
from pprint import pprint
from app.api.services.tmdb_service import tmdb_api

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Load environment variables
load_dotenv()

# Get API key from environment variables
API_KEY = os.getenv("TMDB_API_KEY")
ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")

# TMDb API base URL
BASE_URL = "https://api.themoviedb.org/3"

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def explore_top_movies():
    """Find and print information about movies with the most ratings."""
    print("\n=== Movies with Most Ratings (Popular) ===")
    
    # Get popular movies
    popular = await tmdb_api.get_popular_movies(page=1)
    
    if "error" in popular:
        print(f"Error: {popular['error']}")
        return
    
    # Sort by vote count (number of ratings)
    movies = sorted(popular.get("results", []), key=lambda x: x.get("vote_count", 0), reverse=True)
    
    # Print top 10 movies with highest vote counts
    for i, movie in enumerate(movies[:10], 1):
        title = movie.get("title")
        year = movie.get("release_date", "")[:4]
        vote_count = movie.get("vote_count", 0)
        vote_avg = movie.get("vote_average", 0)
        
        print(f"{i}. {title} ({year}) - {vote_count:,} votes, Rating: {vote_avg}")
    
    print("\n=== Top Rated Movies with Most Ratings ===")
    
    # Get top rated movies
    top_rated = await tmdb_api.get_top_rated_movies(page=1)
    
    if "error" in top_rated:
        print(f"Error: {top_rated['error']}")
        return
    
    # Sort by vote count (number of ratings)
    movies = sorted(top_rated.get("results", []), key=lambda x: x.get("vote_count", 0), reverse=True)
    
    # Print top 10 movies with highest vote counts
    for i, movie in enumerate(movies[:10], 1):
        title = movie.get("title")
        year = movie.get("release_date", "")[:4]
        vote_count = movie.get("vote_count", 0)
        vote_avg = movie.get("vote_average", 0)
        
        print(f"{i}. {title} ({year}) - {vote_count:,} votes, Rating: {vote_avg}")

async def search_movie(query):
    """Search for a movie and print details."""
    print(f"\n=== Searching for: {query} ===")
    
    # Search for movies
    search_results = await tmdb_api.search_movies(query)
    
    if "error" in search_results:
        print(f"Error: {search_results['error']}")
        return
    
    # Print search results
    results = search_results.get("results", [])
    
    if not results:
        print("No results found.")
        return
    
    # Sort by popularity
    results = sorted(results, key=lambda x: x.get("popularity", 0), reverse=True)
    
    for i, movie in enumerate(results[:5], 1):
        title = movie.get("title")
        year = movie.get("release_date", "")[:4]
        vote_count = movie.get("vote_count", 0)
        vote_avg = movie.get("vote_average", 0)
        overview = movie.get("overview", "")
        
        # Truncate overview if too long
        if len(overview) > 100:
            overview = overview[:97] + "..."
        
        print(f"{i}. {title} ({year}) - {vote_count:,} votes, Rating: {vote_avg}")
        print(f"   {overview}")
        print()

async def main():
    """Main function to explore TMDb API."""
    print("TMDb API Explorer")
    print("==================")
    
    # Find movies with most ratings
    await explore_top_movies()
    
    # Example search
    await search_movie("Inception")

if __name__ == "__main__":
    asyncio.run(main()) 