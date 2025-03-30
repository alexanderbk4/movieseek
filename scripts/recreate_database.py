#!/usr/bin/env python3
"""
Recreate the database for MovieSeek.

This script drops and recreates all tables in the database to ensure schema is up to date.
"""

import sys
import os
import logging

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database.models import Base
from app.database.config import engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def recreate_database():
    """Drop and recreate all tables in the database."""
    logger.info("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    logger.info("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    logger.info("Database schema has been reset and recreated.")

if __name__ == "__main__":
    recreate_database() 