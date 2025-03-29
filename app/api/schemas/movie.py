from typing import List, Optional, Dict, Any
from datetime import date
from pydantic import BaseModel, Field

# Base schemas for related entities
class GenreBase(BaseModel):
    name: str
    
class GenreCreate(GenreBase):
    pass

class Genre(GenreBase):
    id: int
    
    class Config:
        orm_mode = True

class PersonBase(BaseModel):
    name: str
    imdb_id: Optional[str] = None
    tmdb_id: Optional[int] = None
    profile_url: Optional[str] = None

class ActorCreate(PersonBase):
    pass

class Actor(PersonBase):
    id: int
    
    class Config:
        orm_mode = True

class DirectorCreate(PersonBase):
    pass

class Director(PersonBase):
    id: int
    
    class Config:
        orm_mode = True

# Movie schemas
class MovieBase(BaseModel):
    title: str
    original_title: Optional[str] = None
    year: Optional[int] = None
    release_date: Optional[date] = None
    runtime: Optional[int] = None
    imdb_rating: Optional[float] = None
    imdb_votes: Optional[int] = None
    metacritic_score: Optional[int] = None
    rotten_tomatoes_score: Optional[int] = None
    plot: Optional[str] = None
    tagline: Optional[str] = None
    poster_url: Optional[str] = None
    backdrop_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class MovieCreate(MovieBase):
    imdb_id: str
    tmdb_id: Optional[str] = None

class MovieUpdate(MovieBase):
    pass

class Movie(MovieBase):
    imdb_id: str
    tmdb_id: Optional[str] = None
    genres: List[Genre] = []
    actors: List[Actor] = []
    directors: List[Director] = []
    
    class Config:
        orm_mode = True

# Schema for filtering movies
class MovieFilter(BaseModel):
    title: Optional[str] = None
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    rating_from: Optional[float] = None
    rating_to: Optional[float] = None
    genres: Optional[List[str]] = None
    directors: Optional[List[str]] = None
    actors: Optional[List[str]] = None 