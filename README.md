# MovieSeek

A sophisticated movie recommendation system focused on quality insights and rich data exploration.

## Project Overview

MovieSeek is a movie-centered recommendation platform that offers:

- High-quality movie data with comprehensive details
- Advanced filtering and sorting capabilities
- Quality metrics beyond basic ratings
- Intuitive UI for movie discovery and exploration

## Technical Stack

- **Frontend**: React with Vite and Tailwind CSS
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic for migrations

## Data Strategy

- Initial dataset includes the top 1000 most-rated movies from IMDb
- Primary identifier: IMDb IDs (e.g., tt0111161)
- Rating system: Primarily IMDb ratings with supplementary metrics
- Data sources:
  - IMDb datasets (available for non-commercial use)
  - The Movie Database (TMDb) API as a supplementary source

## Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 14+

### Backend Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env` and update values

4. Run database migrations:
   ```
   alembic upgrade head
   ```

5. Start the backend server:
   ```
   python main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd app/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

## Development Roadmap

1. **Database Foundation**: Establish core schema and import initial dataset
2. **API Layer**: Build basic CRUD and filtering endpoints
3. **Quality Metrics**: Implement advanced metrics and analysis
4. **UI Development**: Create movie-centered browsing experience

## License

This project is licensed under the MIT License - see the LICENSE file for details.
