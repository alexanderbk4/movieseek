import os
import logging
from typing import Dict, List, Optional, Any
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class TMDbAPI:
    """Client for The Movie Database (TMDb) API."""
    
    BASE_URL = "https://api.themoviedb.org/3"
    
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.access_token = os.getenv("TMDB_ACCESS_TOKEN")
        
        if not self.api_key or not self.access_token:
            logger.warning("TMDb API key or access token not found in environment variables")
    
    async def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a request to the TMDb API."""
        if params is None:
            params = {}
        
        # Add API key to parameters
        if self.api_key:
            params["api_key"] = self.api_key
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json;charset=utf-8"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error occurred: {e}")
            return {"error": str(e)}
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {e}")
            return {"error": str(e)}
    
    async def search_movies(self, query: str, page: int = 1) -> Dict[str, Any]:
        """Search for movies by title."""
        endpoint = "/search/movie"
        params = {
            "query": query,
            "page": page,
            "include_adult": "false"
        }
        return await self._make_request(endpoint, params)
    
    async def get_movie_details(self, movie_id: int) -> Dict[str, Any]:
        """Get detailed information about a movie."""
        endpoint = f"/movie/{movie_id}"
        params = {
            "append_to_response": "credits,keywords,videos,images,release_dates"
        }
        return await self._make_request(endpoint, params)
    
    async def get_popular_movies(self, page: int = 1) -> Dict[str, Any]:
        """Get a list of popular movies."""
        endpoint = "/movie/popular"
        params = {"page": page}
        return await self._make_request(endpoint, params)
    
    async def get_top_rated_movies(self, page: int = 1) -> Dict[str, Any]:
        """Get a list of top rated movies."""
        endpoint = "/movie/top_rated"
        params = {"page": page}
        return await self._make_request(endpoint, params)
    
    async def get_movie_genres(self) -> Dict[str, Any]:
        """Get the list of official genres for movies."""
        endpoint = "/genre/movie/list"
        return await self._make_request(endpoint)

# Create a singleton instance
tmdb_api = TMDbAPI() 