# MovieSeek

A movie recommendation system with database management and API.

## Overview

MovieSeek is a web application that provides movie information and recommendations. It features:

- Movie database with details like title, year, director, ratings, etc.
- Genre categorization and filtering
- Admin interface for database management
- RESTful API for accessing movie data
- (Upcoming) Movie recommendations based on user preferences

## Tech Stack

- **Backend**: FastAPI, SQLAlchemy, Uvicorn
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: Simple admin dashboard with Jinja2 templates
- **API**: RESTful API with JSON responses
- **Data Source**: TMDb API (planned)

## Setup and Installation

### Prerequisites

- Python 3.9+
- Virtual environment (recommended)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/movieseek.git
   cd movieseek
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file in the project root):
   ```
   # Database Configuration
   DATABASE_URL=sqlite:///./movieseek.db
   DATABASE_TEST_URL=sqlite:///./movieseek_test.db

   # API Keys
   TMDB_API_KEY=your_tmdb_api_key_here
   TMDB_ACCESS_TOKEN=your_tmdb_read_access_token_here

   # Application Settings
   DEBUG=True
   SECRET_KEY=dev_secret_key_change_in_production
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. Run the application:
   ```
   uvicorn main:app --reload
   ```

The application will be available at `http://localhost:8000`

## API Endpoints

### Movies

- `GET /api/movies/` - List all movies with optional filtering
- `GET /api/movies/{movie_id}` - Get a specific movie by ID
- `POST /api/movies/{movie_id}/genres/{genre_id}` - Add a genre to a movie

### Admin Interface

- `GET /admin/` - Admin dashboard
- `GET /admin/movies` - View all movies
- `GET /admin/genres` - View all genres
- `GET /admin/api/movies` - Get all movies as JSON
- `GET /admin/api/genres` - Get all genres as JSON

## Database Schema

### Movies Table

```sql
CREATE TABLE movies (
    id INTEGER PRIMARY KEY,
    identifier VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    year INTEGER NOT NULL,
    director VARCHAR(255),
    runtime INTEGER,
    imdb_rating DECIMAL(3, 1),
    imdb_votes INTEGER,
    imdb_id VARCHAR(20),
    created_at TIMESTAMP WITH TIME ZONE,
    updated_at TIMESTAMP WITH TIME ZONE
);
```

### Genres Table

```sql
CREATE TABLE genres (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL
);
```

### Junction Table (Movie-Genre)

```sql
CREATE TABLE movie_genres (
    movie_id INTEGER REFERENCES movies(id),
    genre_id INTEGER REFERENCES genres(id),
    PRIMARY KEY (movie_id, genre_id)
);
```

## Data Source

This project uses The Movie Database (TMDb) API to fetch movie data. You'll need to register for a free API key at [https://www.themoviedb.org/documentation/api](https://www.themoviedb.org/documentation/api) and add it to your `.env` file:

```
TMDB_API_KEY=your_tmdb_api_key_here
TMDB_ACCESS_TOKEN=your_tmdb_read_access_token_here
```

## Utility Scripts

The `scripts` directory contains various utility scripts for managing the application:

- **Database Management**: Clear the database (`scripts/clear_database.py`)
- **TMDb Exploration**: Explore TMDb data (`scripts/explore_tmdb.py`, `scripts/find_most_rated_movies.py`)
- **Data Import**: Import movie data from TMDb (`scripts/quick_import.py`, `scripts/import_tmdb_data.py`)

See the [scripts README](scripts/README.md) for more details and usage examples.

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
