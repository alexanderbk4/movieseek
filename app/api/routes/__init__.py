from fastapi import APIRouter
from app.api.routes.movies import router as movies_router
from app.api.routes.tmdb import router as tmdb_router
from app.api.routes.genres import router as genres_router

api_router = APIRouter()
api_router.include_router(movies_router, prefix="/movies", tags=["movies"])
api_router.include_router(tmdb_router, prefix="/tmdb", tags=["tmdb"])
api_router.include_router(genres_router, prefix="/genres", tags=["genres"]) 