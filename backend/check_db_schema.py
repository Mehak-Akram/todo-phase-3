#!/usr/bin/env python3
"""
Check the current database schema to understand what tables exist.
"""

import os
import sys
from sqlalchemy import create_engine, inspect
from src.config import settings

def check_db_schema():
    """Check the current database schema."""
    engine = create_engine(settings.database_url)

    inspector = inspect(engine)

    print("Database tables:")
    for table_name in inspector.get_table_names():
        print(f"\nTable: {table_name}")

        columns = inspector.get_columns(table_name)
        print("  Columns:")
        for col in columns:
            print(f"    - {col['name']}: {col['type']} (nullable: {col['nullable']})")

        if table_name == 'message':
            # Check if metadata_json column exists
            column_names = [col['name'] for col in columns]
            if 'metadata_json' not in column_names:
                print(f"    [WARNING] metadata_json column missing from {table_name}")
            else:
                print(f"    [OK] metadata_json column exists in {table_name}")

        if table_name == 'message':
            # Check if role column exists and its type
            role_col = next((col for col in columns if col['name'] == 'role'), None)
            if role_col:
                print(f"    Role column type: {role_col['type']}")

    print("\nForeign key constraints:")
    for table_name in inspector.get_table_names():
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            print(f"  {table_name}.{fk['constrained_columns'][0]} -> {fk['referred_table']}.{fk['referred_columns'][0]}")

if __name__ == "__main__":
    check_db_schema()