#!/usr/bin/env python
"""
Simple script to import SQL backup file into PostgreSQL database.
Run this from inside the Docker container or with proper database access.

Usage: python import_sql_simple.py <backup_file.sql>
"""
import os
import sys
import subprocess

def import_sql_file(sql_file_path):
    """Import SQL file using psql command"""
    if not os.path.exists(sql_file_path):
        print(f"Error: SQL file not found: {sql_file_path}")
        sys.exit(1)
    
    # Database connection parameters
    db_name = os.getenv("POSTGRES_DB", "onlineshop")
    db_user = os.getenv("POSTGRES_USER", "onlineshop")
    db_password = os.getenv("POSTGRES_PASSWORD", "onlineshop")
    db_host = os.getenv("POSTGRES_HOST", "db")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    
    print("=" * 60)
    print("SQL Backup Import Script")
    print("=" * 60)
    print(f"Database: {db_name}")
    print(f"Host: {db_host}:{db_port}")
    print(f"User: {db_user}")
    print(f"File: {sql_file_path}")
    print("=" * 60)
    print()
    
    # Set environment variable for password
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    # Build psql command
    cmd = [
        'psql',
        '-h', db_host,
        '-p', db_port,
        '-U', db_user,
        '-d', db_name,
        '-f', sql_file_path
    ]
    
    print("Executing psql command...")
    print(f"Command: {' '.join(cmd[:6])} ... -f {sql_file_path}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✓ SQL backup imported successfully!")
            if result.stdout:
                print("\nOutput:")
                print(result.stdout)
        else:
            print("✗ Error importing SQL backup")
            if result.stderr:
                print("\nError output:")
                print(result.stderr)
            if result.stdout:
                print("\nStandard output:")
                print(result.stdout)
            sys.exit(1)
            
    except FileNotFoundError:
        print("✗ Error: psql command not found!")
        print("Make sure PostgreSQL client tools are installed.")
        print("Or use the shell script: ./import_sql_backup_docker.sh")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python import_sql_simple.py <backup_file.sql>")
        print("\nExample:")
        print("  python import_sql_simple.py backup_20251221_142048.sql")
        sys.exit(1)
    
    sql_file = sys.argv[1]
    
    # If relative path, make it relative to current directory
    if not os.path.isabs(sql_file):
        sql_file = os.path.join(os.getcwd(), sql_file)
    
    import_sql_file(sql_file)


if __name__ == '__main__':
    main()

