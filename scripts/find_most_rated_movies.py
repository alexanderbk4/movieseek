#!/usr/bin/env python3
"""
Find movies with the most ratings from TMDb.

This script retrieves multiple pages of movies from TMDb and sorts them
by vote count to find movies with the most ratings/votes.
"""

import os
import sys
import argparse
import asyncio
import logging
import json
from pprint import pprint

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.api.services.tmdb_service import tmdb_api

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_movies_from_multiple_pages(method, page_count=5):
    """Get movies from multiple pages of TMDb API results."""
    all_results = []
    
    for page in range(1, page_count + 1):
        print(f"Fetching page {page}...")
        
        if method == "popular":
            data = await tmdb_api.get_popular_movies(page=page)
        elif method == "top_rated":
            data = await tmdb_api.get_top_rated_movies(page=page)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        if "error" in data:
            print(f"Error fetching page {page}: {data['error']}")
            continue
        
        results = data.get("results", [])
        all_results.extend(results)
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    return all_results

async def find_most_rated_movies(method="top_rated", sort_by="vote_count", page_count=5, limit=50):
    """Find movies with the most ratings or by other criteria."""
    print(f"\n=== Finding movies from {method.replace('_', ' ').title()} ===")
    print(f"Fetching {page_count} pages, sorting by {sort_by}, showing top {limit} results...")
    
    # Get movies from multiple pages
    movies = await get_movies_from_multiple_pages(method, page_count)
    
    # Sort movies based on criteria
    if sort_by == "vote_count":
        movies = sorted(movies, key=lambda x: x.get("vote_count", 0), reverse=True)
    elif sort_by == "vote_average":
        # Only consider movies with at least 1000 votes for rating sorting
        movies = [m for m in movies if m.get("vote_count", 0) >= 1000]
        movies = sorted(movies, key=lambda x: x.get("vote_average", 0), reverse=True)
    elif sort_by == "popularity":
        movies = sorted(movies, key=lambda x: x.get("popularity", 0), reverse=True)
    elif sort_by == "release_date":
        movies = sorted(movies, key=lambda x: x.get("release_date", ""), reverse=True)
    else:
        print(f"Unknown sort_by value: {sort_by}, defaulting to vote_count")
        movies = sorted(movies, key=lambda x: x.get("vote_count", 0), reverse=True)
    
    # Print the top results
    for i, movie in enumerate(movies[:limit], 1):
        title = movie.get("title")
        year = movie.get("release_date", "")[:4]
        vote_count = movie.get("vote_count", 0)
        vote_avg = movie.get("vote_average", 0)
        popularity = movie.get("popularity", 0)
        movie_id = movie.get("id")
        
        print(f"{i}. {title} ({year}) - {vote_count:,} votes, Rating: {vote_avg}, Popularity: {popularity:.1f}, ID: {movie_id}")

async def get_movie_details(movie_id):
    """Get detailed information about a specific movie."""
    print(f"\n=== Getting details for movie ID: {movie_id} ===")
    
    # Get movie details from TMDb
    movie_details = await tmdb_api.get_movie_details(movie_id)
    
    if "error" in movie_details:
        print(f"Error fetching movie details: {movie_details['error']}")
        return
    
    # Extract basic information
    title = movie_details.get("title")
    original_title = movie_details.get("original_title")
    year = movie_details.get("release_date", "")[:4]
    runtime = movie_details.get("runtime")
    vote_count = movie_details.get("vote_count", 0)
    vote_avg = movie_details.get("vote_average", 0)
    popularity = movie_details.get("popularity", 0)
    overview = movie_details.get("overview", "")
    imdb_id = movie_details.get("imdb_id")
    
    # Extract genres
    genres = [genre.get("name") for genre in movie_details.get("genres", [])]
    
    # Extract directors
    directors = []
    for crew_member in movie_details.get("credits", {}).get("crew", []):
        if crew_member.get("job") == "Director":
            directors.append(crew_member.get("name"))
    
    # Extract top cast
    cast = []
    for actor in movie_details.get("credits", {}).get("cast", [])[:10]:
        cast.append(f"{actor.get('name')} as {actor.get('character')}")
    
    # Print the details
    print(f"Title: {title}")
    if original_title and original_title != title:
        print(f"Original Title: {original_title}")
    print(f"Year: {year}")
    print(f"Runtime: {runtime} minutes")
    print(f"IMDb ID: {imdb_id}")
    print(f"Votes: {vote_count:,}")
    print(f"Rating: {vote_avg}")
    print(f"Popularity: {popularity:.1f}")
    print(f"Genres: {', '.join(genres)}")
    print(f"Director(s): {', '.join(directors)}")
    print("\nOverview:")
    print(overview)
    print("\nTop Cast:")
    for actor_role in cast:
        print(f"- {actor_role}")
    
    # Optional: Save full details to a JSON file
    output_file = f"movie_{movie_id}_details.json"
    with open(output_file, "w") as f:
        json.dump(movie_details, f, indent=2)
    
    print(f"\nFull details saved to {output_file}")

async def main():
    """Parse arguments and run the appropriate function."""
    parser = argparse.ArgumentParser(description="Find movies with the most ratings from TMDb")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List movies with high vote counts")
    list_parser.add_argument("--method", choices=["popular", "top_rated"], default="top_rated",
                        help="Which TMDb endpoint to use (default: top_rated)")
    list_parser.add_argument("--sort", choices=["vote_count", "vote_average", "popularity", "release_date"], 
                        default="vote_count", help="How to sort the results (default: vote_count)")
    list_parser.add_argument("--pages", type=int, default=5, 
                        help="Number of pages to fetch (default: 5, max recommended: 10)")
    list_parser.add_argument("--limit", type=int, default=50,
                        help="Maximum number of results to display (default: 50)")
    
    # Details command
    details_parser = subparsers.add_parser("details", help="Get detailed information about a specific movie")
    details_parser.add_argument("movie_id", type=int, help="TMDb movie ID to get details for")
    
    args = parser.parse_args()
    
    print("TMDb Movie Explorer")
    print("==================")
    
    if args.command == "list" or args.command is None:
        # Default to list command if none provided
        await find_most_rated_movies(
            method=getattr(args, "method", "top_rated"),
            sort_by=getattr(args, "sort", "vote_count"),
            page_count=getattr(args, "pages", 5),
            limit=getattr(args, "limit", 50)
        )
    elif args.command == "details":
        await get_movie_details(args.movie_id)
    else:
        parser.print_help()

if __name__ == "__main__":
    asyncio.run(main()) 