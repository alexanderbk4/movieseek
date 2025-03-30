from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from app.database.models.movie import Movie, Genre, Actor, Director
from app.api.schemas.movie import MovieCreate, MovieUpdate, MovieFilter

def get_movies(db: Session, skip: int = 0, limit: int = 100, movie_filter: Optional[MovieFilter] = None) -> List[Movie]:
    """
    Get a list of movies with optional filtering.
    """
    query = db.query(Movie).options(
        joinedload(Movie.genres),
        joinedload(Movie.directors),
        joinedload(Movie.actors)
    )
    
    # Apply filters if provided
    if movie_filter:
        if movie_filter.title:
            query = query.filter(Movie.title.ilike(f"%{movie_filter.title}%"))
            
        if movie_filter.year_from:
            query = query.filter(Movie.year >= movie_filter.year_from)
            
        if movie_filter.year_to:
            query = query.filter(Movie.year <= movie_filter.year_to)
            
        if movie_filter.rating_from:
            query = query.filter(Movie.imdb_rating >= movie_filter.rating_from)
            
        if movie_filter.rating_to:
            query = query.filter(Movie.imdb_rating <= movie_filter.rating_to)
            
        if movie_filter.genres:
            query = query.join(Movie.genres).filter(Genre.name.in_(movie_filter.genres))
            
        if movie_filter.directors:
            query = query.join(Movie.directors).filter(Director.name.in_(movie_filter.directors))
            
        if movie_filter.actors:
            query = query.join(Movie.actors).filter(Actor.name.in_(movie_filter.actors))
    
    # Apply pagination
    movies = query.offset(skip).limit(limit).all()
    return movies

def get_movie_by_id(db: Session, movie_id: str) -> Optional[Movie]:
    """
    Get a specific movie by its IMDb ID.
    """
    return db.query(Movie).options(
        joinedload(Movie.genres),
        joinedload(Movie.directors),
        joinedload(Movie.actors)
    ).filter(Movie.imdb_id == movie_id).first()

def create_movie(db: Session, movie: MovieCreate) -> Movie:
    """
    Create a new movie.
    """
    db_movie = Movie(
        imdb_id=movie.imdb_id,
        tmdb_id=movie.tmdb_id,
        title=movie.title,
        original_title=movie.original_title,
        year=movie.year,
        release_date=movie.release_date,
        runtime=movie.runtime,
        imdb_rating=movie.imdb_rating,
        imdb_votes=movie.imdb_votes,
        metacritic_score=movie.metacritic_score,
        rotten_tomatoes_score=movie.rotten_tomatoes_score,
        plot=movie.plot,
        tagline=movie.tagline,
        poster_url=movie.poster_url,
        backdrop_url=movie.backdrop_url,
        movie_metadata=movie.movie_metadata
    )
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie

def update_movie(db: Session, movie_id: str, movie: MovieUpdate) -> Movie:
    """
    Update an existing movie.
    """
    db_movie = get_movie_by_id(db, movie_id)
    
    # Update movie attributes
    movie_data = movie.dict(exclude_unset=True)
    for key, value in movie_data.items():
        setattr(db_movie, key, value)
    
    db.commit()
    db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: str) -> None:
    """
    Delete a movie.
    """
    db_movie = get_movie_by_id(db, movie_id)
    db.delete(db_movie)
    db.commit()

def add_genre_to_movie(db: Session, movie_id: str, genre_id: int) -> Movie:
    """
    Add a genre to a movie.
    """
    movie = get_movie_by_id(db, movie_id)
    genre = db.query(Genre).filter(Genre.id == genre_id).first()
    
    if not genre:
        return None
    
    movie.genres.append(genre)
    db.commit()
    db.refresh(movie)
    return movie

def add_actor_to_movie(db: Session, movie_id: str, actor_id: int) -> Movie:
    """
    Add an actor to a movie.
    """
    movie = get_movie_by_id(db, movie_id)
    actor = db.query(Actor).filter(Actor.id == actor_id).first()
    
    if not actor:
        return None
    
    movie.actors.append(actor)
    db.commit()
    db.refresh(movie)
    return movie

def add_director_to_movie(db: Session, movie_id: str, director_id: int) -> Movie:
    """
    Add a director to a movie.
    """
    movie = get_movie_by_id(db, movie_id)
    director = db.query(Director).filter(Director.id == director_id).first()
    
    if not director:
        return None
    
    movie.directors.append(director)
    db.commit()
    db.refresh(movie)
    return movie 