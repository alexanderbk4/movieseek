from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from app.api.routes import api_router
from app.admin import admin_router
from app.database.init_db import init_db

app = FastAPI(
    title="MovieSeek API",
    description="Movie recommendation system API",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Include Admin router
app.include_router(admin_router)

@app.get("/")
async def root():
    return {"message": "Welcome to MovieSeek API"}

if __name__ == "__main__":
    # Initialize the database
    init_db()
    
    # Run the app
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
