# MovieSeek Utility Scripts

This directory contains utility scripts for the MovieSeek application, providing functionality for database management and movie data import.

## Available Scripts

- **clear_database.py**: Clears all data from the database (movies and genres)
- **explore_tmdb.py**: Explores TMDb API by displaying popular and top-rated movies
- **find_most_rated_movies.py**: Finds movies with the most ratings/votes from TMDb
- **import_tmdb_data.py**: Imports movie data from TMDb into the database
- **import_top_voted.py**: Imports the top 1000 movies by vote count from TMDb
- **quick_import.py**: Simple utility for quickly importing movies by ID or top movies
- **recreate_database.py**: Drops and recreates all database tables to ensure schema is up to date

## Usage Examples

### Clear the Database

```bash
python3 scripts/clear_database.py
```

### Recreate Database

```bash
python3 scripts/recreate_database.py
```

### Explore TMDb Data

```bash
python3 scripts/explore_tmdb.py
```

### Find Movies with Most Ratings

```bash
# List top rated movies sorted by vote count (default 50 results)
python3 scripts/find_most_rated_movies.py list --method top_rated --sort vote_count

# Get detailed information about a specific movie
python3 scripts/find_most_rated_movies.py details 12345
```

### Import Movies from TMDb

```bash
# Import specific movies by TMDb ID
python3 scripts/quick_import.py ids 11 13 27205

# Import top movies by vote count
python3 scripts/quick_import.py top --count 10

# More comprehensive import with customization
python3 scripts/import_tmdb_data.py --popular 2 --top_rated 2
```

### Import Top 1000 Movies by Vote Count

```bash
# Import top 1000 movies with the most votes
python3 scripts/import_top_voted.py

# Import top 500 movies with the most votes
python3 scripts/import_top_voted.py --count 500

# Recreate database and import top 1000 movies
python3 scripts/import_top_voted.py --recreate
``` 