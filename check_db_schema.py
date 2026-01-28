#!/usr/bin/env python3
"""
Script to check the actual database schema
"""
import os
import sys
from sqlalchemy import create_engine, inspect

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.src.config import settings

def check_database_schema():
    # Create engine using the database URL from settings
    engine = create_engine(settings.database_url)

    # Get inspector
    inspector = inspect(engine)

    # Get table names
    tables = inspector.get_table_names()
    print("Tables in database:")
    for table in tables:
        print(f"  - {table}")

    # Check columns in conversation table
    if 'conversation' in tables:
        print("\nColumns in 'conversation' table:")
        columns = inspector.get_columns('conversation')
        for col in columns:
            print(f"  - {col['name']} ({col['type']}) - nullable: {col['nullable']}")

    # Check columns in message table
    if 'message' in tables:
        print("\nColumns in 'message' table:")
        columns = inspector.get_columns('message')
        for col in columns:
            print(f"  - {col['name']} ({col['type']}) - nullable: {col['nullable']}")

if __name__ == "__main__":
    check_database_schema()