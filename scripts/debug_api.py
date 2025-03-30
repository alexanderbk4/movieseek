#!/usr/bin/env python
"""
Debug script for API endpoints
"""
import sys
import os
import requests
import sqlite3
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

def test_api_endpoints():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/api/movies",
        "/api/genres",
        "/admin/api/movies",
        "/admin/api/genres"
    ]
    
    for endpoint in endpoints:
        print(f"\nTesting endpoint: {endpoint}")
        try:
            response = requests.get(f"{base_url}{endpoint}")
            print(f"Status code: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Data length: {len(data)} items")
                if data and len(data) > 0:
                    print(f"First item: {data[0]}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Error connecting to {endpoint}: {str(e)}")

def check_database():
    """Check database tables and counts"""
    db_path = Path("movieseek.db")
    
    if not db_path.exists():
        print(f"Database file not found at {db_path.absolute()}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("\nDatabase tables:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            count = cursor.fetchone()[0]
            print(f"  - {table_name}: {count} rows")
            
            # Show sample data for movies and genres
            if table_name in ["movies", "genres"] and count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3;")
                columns = [desc[0] for desc in cursor.description]
                rows = cursor.fetchall()
                
                print(f"\n    Sample {table_name} data:")
                for row in rows:
                    row_dict = {columns[i]: row[i] for i in range(len(columns))}
                    print(f"    {row_dict}")
        
        conn.close()
    except Exception as e:
        print(f"Error checking database: {str(e)}")

if __name__ == "__main__":
    print("=== MovieSeek API Debug Tool ===")
    test_api_endpoints()
    check_database() 