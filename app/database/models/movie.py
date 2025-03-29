from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship

from app.database.models.base import Base, TimestampMixin

# Association tables for many-to-many relationships
movie_genre = Table(
    'movie_genre',
    Base.metadata,
    Column('movie_id', String, ForeignKey('movies.imdb_id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)

movie_actor = Table(
    'movie_actor',
    Base.metadata,
    Column('movie_id', String, ForeignKey('movies.imdb_id')),
    Column('actor_id', Integer, ForeignKey('actors.id'))
)

movie_director = Table(
    'movie_director',
    Base.metadata,
    Column('movie_id', String, ForeignKey('movies.imdb_id')),
    Column('director_id', Integer, ForeignKey('directors.id'))
)

class Movie(Base, TimestampMixin):
    """Movie model containing essential movie information."""
    __tablename__ = "movies"
    
    imdb_id = Column(String, primary_key=True, index=True)
    tmdb_id = Column(String, unique=True, index=True, nullable=True)
    title = Column(String, index=True, nullable=False)
    original_title = Column(String, nullable=True)
    year = Column(Integer, index=True)
    release_date = Column(Date, nullable=True)
    runtime = Column(Integer, nullable=True)  # in minutes
    
    # Ratings and metrics
    imdb_rating = Column(Float, nullable=True)
    imdb_votes = Column(Integer, nullable=True)
    metacritic_score = Column(Integer, nullable=True)
    rotten_tomatoes_score = Column(Integer, nullable=True)
    
    # Basic information
    plot = Column(String, nullable=True)
    tagline = Column(String, nullable=True)
    poster_url = Column(String, nullable=True)
    backdrop_url = Column(String, nullable=True)
    
    # Extended metadata (flexible structure)
    metadata = Column(JSON, nullable=True)
    
    # Relationships
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    actors = relationship("Actor", secondary=movie_actor, back_populates="movies")
    directors = relationship("Director", secondary=movie_director, back_populates="movies")

class Genre(Base):
    """Genre model."""
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres")

class Actor(Base, TimestampMixin):
    """Actor model."""
    __tablename__ = "actors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    tmdb_id = Column(Integer, unique=True, nullable=True)
    imdb_id = Column(String, unique=True, nullable=True)
    profile_url = Column(String, nullable=True)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_actor, back_populates="actors")

class Director(Base, TimestampMixin):
    """Director model."""
    __tablename__ = "directors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    tmdb_id = Column(Integer, unique=True, nullable=True)
    imdb_id = Column(String, unique=True, nullable=True)
    profile_url = Column(String, nullable=True)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_director, back_populates="directors") 