#!/usr/bin/env python
"""
Script to add poster_path and backdrop_path columns to the movies table
"""
import sys
import os
import sqlite3
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

def add_image_columns():
    """Add poster_path and backdrop_path columns to the movies table"""
    db_path = Path("movieseek.db")
    
    if not db_path.exists():
        print(f"Database file not found at {db_path.absolute()}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the columns already exist
        cursor.execute("PRAGMA table_info(movies)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Add poster_path column if it doesn't exist
        if "poster_path" not in columns:
            print("Adding poster_path column to movies table...")
            cursor.execute("ALTER TABLE movies ADD COLUMN poster_path VARCHAR(255)")
        else:
            print("poster_path column already exists")
        
        # Add backdrop_path column if it doesn't exist
        if "backdrop_path" not in columns:
            print("Adding backdrop_path column to movies table...")
            cursor.execute("ALTER TABLE movies ADD COLUMN backdrop_path VARCHAR(255)")
        else:
            print("backdrop_path column already exists")
        
        conn.commit()
        print("Columns added successfully!")
        
        conn.close()
    except Exception as e:
        print(f"Error adding columns: {str(e)}")

if __name__ == "__main__":
    print("=== Adding Image Columns to Movies Table ===")
    add_image_columns() 