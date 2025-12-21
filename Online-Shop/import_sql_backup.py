#!/usr/bin/env python
"""
Script to import SQL backup file into PostgreSQL database.
Usage: python import_sql_backup.py <backup_file.sql>
"""
import os
import sys
import django
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from django.db import connection
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def import_sql_file(sql_file_path):
    """
    Import SQL backup file into PostgreSQL database.
    
    Args:
        sql_file_path: Path to the SQL backup file
    """
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found: {sql_file_path}")
        sys.exit(1)
    
    # Get database connection parameters
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
    
    print(f"Connecting to database: {db_name} on {db_host}:{db_port}")
    print(f"User: {db_user}")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        
        # Set isolation level to allow multiple statements
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        print(f"\nReading SQL file: {sql_file_path}")
        with open(sql_file_path, 'r', encoding='utf-8') as f:
            sql_content = f.read()
        
        if not sql_content.strip():
            print("Warning: SQL file is empty!")
            return
        
        print("Executing SQL commands...")
        
        # Split by semicolon and execute each statement
        # Note: This is a simple approach. For complex SQL with functions/procedures,
        # you might need to use psql command line tool instead
        statements = [s.strip() for s in sql_content.split(';') if s.strip()]
        
        total_statements = len(statements)
        print(f"Found {total_statements} SQL statements to execute")
        
        executed = 0
        errors = 0
        
        for i, statement in enumerate(statements, 1):
            # Skip comments and empty statements
            if statement.startswith('--') or not statement:
                continue
            
            try:
                cursor.execute(statement)
                executed += 1
                if i % 100 == 0:
                    print(f"Progress: {i}/{total_statements} statements executed...")
            except psycopg2.Error as e:
                errors += 1
                # Some errors are expected (like DROP IF EXISTS on non-existent objects)
                if 'does not exist' not in str(e).lower():
                    print(f"\nWarning: Error executing statement {i}: {str(e)[:200]}")
        
        print(f"\n✓ Import completed!")
        print(f"  - Executed: {executed} statements")
        print(f"  - Errors: {errors} (some may be expected)")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Database import successful!")
        
    except psycopg2.OperationalError as e:
        print(f"\n✗ Database connection error: {e}")
        print("\nMake sure:")
        print("  1. Database container is running: docker compose up -d db")
        print("  2. Database credentials are correct in settings.py")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python import_sql_backup.py <backup_file.sql>")
        print("\nExample:")
        print("  python import_sql_backup.py backup_20251221_142048.sql")
        sys.exit(1)
    
    sql_file = sys.argv[1]
    
    # If relative path, make it relative to script directory
    if not os.path.isabs(sql_file):
        sql_file = os.path.join(BASE_DIR, sql_file)
    
    print("=" * 60)
    print("SQL Backup Import Script")
    print("=" * 60)
    
    import_sql_file(sql_file)


if __name__ == '__main__':
    main()

