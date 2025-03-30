from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Table, JSON, Index, DECIMAL, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.database.models.base import Base, TimestampMixin

# Association tables for many-to-many relationships
movie_genre = Table(
    'movie_genres',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id')),
    Column('genre_id', Integer, ForeignKey('genres.id')),
    PrimaryKeyConstraint('movie_id', 'genre_id')
)

class Movie(Base, TimestampMixin):
    """Movie model containing essential movie information."""
    __tablename__ = "movies"
    
    id = Column(Integer, primary_key=True, index=True)
    identifier = Column(String(255), unique=True, nullable=False)  # title+year identifier
    title = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    director = Column(String(255), nullable=True)
    runtime = Column(Integer, nullable=True)  # in minutes
    imdb_rating = Column(DECIMAL(3, 1), nullable=True)  # e.g., 8.7
    imdb_votes = Column(Integer, nullable=True)
    imdb_id = Column(String(20), nullable=True)  # storing this for reference
    
    # Relationships
    genres = relationship("Genre", secondary=movie_genre, back_populates="movies")
    
    # Create indexes
    __table_args__ = (
        Index('idx_movies_identifier', identifier),
        Index('idx_movies_title', title),
        Index('idx_movies_year', year),
    )

class Genre(Base):
    """Genre model."""
    __tablename__ = "genres"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    movies = relationship("Movie", secondary=movie_genre, back_populates="genres") 