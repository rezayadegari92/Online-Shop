#!/usr/bin/env python
"""
Database Migration Script for Dokploy
This script helps migrate your database from local Docker to Dokploy container.

Usage:
    python migrate_to_dokploy.py --export    # Export current database
    python migrate_to_dokploy.py --import    # Import to Dokploy database
    python migrate_to_dokploy.py --migrate   # Full migration (export + import)
"""
import os
import sys
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Setup Django environment
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

import django
django.setup()

from django.conf import settings


def export_database(output_file=None):
    """Export database to SQL file"""
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f"backup_{timestamp}.sql"
    
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']
    
    print("=" * 60)
    print("Exporting Database")
    print("=" * 60)
    print(f"Database: {db_name}")
    print(f"Host: {db_host}:{db_port}")
    print(f"Output file: {output_file}")
    print("=" * 60)
    print()
    
    # Set password environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = db_password
    
    # Build pg_dump command
    cmd = [
        'pg_dump',
        '-h', db_host,
        '-p', str(db_port),
        '-U', db_user,
        '-d', db_name,
        '--clean',           # Include DROP statements
        '--if-exists',       # Use IF EXISTS for DROP
        '--no-owner',        # Don't output commands to set ownership
        '--no-acl',          # Don't output ACL (access privileges)
        '-f', output_file
    ]
    
    print("Running pg_dump...")
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            file_size = os.path.getsize(output_file) / (1024 * 1024)  # Size in MB
            print(f"✓ Database exported successfully!")
            print(f"  File: {output_file}")
            print(f"  Size: {file_size:.2f} MB")
            return output_file
        else:
            print("✗ Error exporting database")
            if result.stderr:
                print(f"Error: {result.stderr}")
            sys.exit(1)
            
    except FileNotFoundError:
        print("✗ Error: pg_dump not found!")
        print("Make sure PostgreSQL client tools are installed.")
        print("\nAlternative: Use Docker to export:")
        print(f"  docker compose exec db pg_dump -U {db_user} -d {db_name} --clean --if-exists > {output_file}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def import_database(sql_file, dokploy_config=None):
    """Import database from SQL file to Dokploy"""
    if not os.path.exists(sql_file):
        print(f"✗ Error: SQL file not found: {sql_file}")
        sys.exit(1)
    
    # Dokploy database configuration
    # You can provide these via environment variables or command line
    dokploy_db_name = os.getenv('DOKPLOY_DB_NAME', dokploy_config.get('name') if dokploy_config else 'onlineshop')
    dokploy_db_user = os.getenv('DOKPLOY_DB_USER', dokploy_config.get('user') if dokploy_config else 'onlineshop')
    dokploy_db_password = os.getenv('DOKPLOY_DB_PASSWORD', dokploy_config.get('password') if dokploy_config else '')
    dokploy_db_host = os.getenv('DOKPLOY_DB_HOST', dokploy_config.get('host') if dokploy_config else 'localhost')
    dokploy_db_port = os.getenv('DOKPLOY_DB_PORT', dokploy_config.get('port') if dokploy_config else '5432')
    
    if not dokploy_db_password:
        print("✗ Error: Dokploy database password not provided!")
        print("Set DOKPLOY_DB_PASSWORD environment variable or provide via --password")
        sys.exit(1)
    
    print("=" * 60)
    print("Importing Database to Dokploy")
    print("=" * 60)
    print(f"Database: {dokploy_db_name}")
    print(f"Host: {dokploy_db_host}:{dokploy_db_port}")
    print(f"User: {dokploy_db_user}")
    print(f"SQL File: {sql_file}")
    print("=" * 60)
    print()
    
    # Set password environment variable
    env = os.environ.copy()
    env['PGPASSWORD'] = dokploy_db_password
    
    # Build psql command
    cmd = [
        'psql',
        '-h', dokploy_db_host,
        '-p', str(dokploy_db_port),
        '-U', dokploy_db_user,
        '-d', dokploy_db_name,
        '-f', sql_file
    ]
    
    print("Importing SQL file...")
    print("This may take a while depending on database size...")
    print()
    
    try:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓ Database imported successfully to Dokploy!")
            if result.stdout:
                print("\nOutput:")
                print(result.stdout[-500:])  # Show last 500 chars
        else:
            print("✗ Error importing database")
            if result.stderr:
                print("\nError output:")
                print(result.stderr[-1000:])  # Show last 1000 chars
            sys.exit(1)
            
    except FileNotFoundError:
        print("✗ Error: psql not found!")
        print("Make sure PostgreSQL client tools are installed.")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


def migrate_full(dokploy_config=None):
    """Full migration: export and import"""
    print("=" * 60)
    print("Full Database Migration to Dokploy")
    print("=" * 60)
    print()
    
    # Step 1: Export
    print("Step 1: Exporting current database...")
    sql_file = export_database()
    print()
    
    # Step 2: Import
    print("Step 2: Importing to Dokploy database...")
    import_database(sql_file, dokploy_config)
    print()
    
    print("=" * 60)
    print("✓ Migration completed successfully!")
    print("=" * 60)
    print(f"Backup file saved as: {sql_file}")
    print("You can keep this file as a backup.")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Migrate database to Dokploy container',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Export database only
  python migrate_to_dokploy.py --export
  
  # Import to Dokploy (set environment variables first)
  export DOKPLOY_DB_HOST=your-dokploy-host
  export DOKPLOY_DB_NAME=onlineshop
  export DOKPLOY_DB_USER=onlineshop
  export DOKPLOY_DB_PASSWORD=your-password
  python migrate_to_dokploy.py --import backup_20251221_142048.sql
  
  # Full migration
  python migrate_to_dokploy.py --migrate
  
  # Import with custom config
  python migrate_to_dokploy.py --import backup.sql \\
    --host dokploy-db.example.com \\
    --name onlineshop \\
    --user onlineshop \\
    --password your-password
        """
    )
    
    parser.add_argument('--export', action='store_true',
                       help='Export current database to SQL file')
    parser.add_argument('--import', dest='import_file', metavar='FILE',
                       help='Import SQL file to Dokploy database')
    parser.add_argument('--migrate', action='store_true',
                       help='Full migration (export + import)')
    
    # Dokploy connection options
    parser.add_argument('--host', help='Dokploy database host')
    parser.add_argument('--port', type=int, default=5432, help='Dokploy database port')
    parser.add_argument('--name', help='Dokploy database name')
    parser.add_argument('--user', help='Dokploy database user')
    parser.add_argument('--password', help='Dokploy database password')
    
    args = parser.parse_args()
    
    # Build dokploy config from args
    dokploy_config = {}
    if args.host:
        dokploy_config['host'] = args.host
    if args.port:
        dokploy_config['port'] = args.port
    if args.name:
        dokploy_config['name'] = args.name
    if args.user:
        dokploy_config['user'] = args.user
    if args.password:
        dokploy_config['password'] = args.password
    
    if args.export:
        export_database()
    elif args.import_file:
        import_database(args.import_file, dokploy_config if dokploy_config else None)
    elif args.migrate:
        migrate_full(dokploy_config if dokploy_config else None)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()

