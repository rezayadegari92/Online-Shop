#!/bin/bash
# Import SQL backup using psql directly (run from inside web container)
# This script should be run from inside the Docker container

if [ $# -eq 0 ]; then
    echo "Usage: ./import_sql_backup_docker.sh <backup_file.sql>"
    echo ""
    echo "Example:"
    echo "  ./import_sql_backup_docker.sh backup_20251221_142048.sql"
    exit 1
fi

SQL_FILE=$1

if [ ! -f "$SQL_FILE" ]; then
    echo "Error: SQL file not found: $SQL_FILE"
    exit 1
fi

echo "=========================================="
echo "Importing SQL backup"
echo "=========================================="
echo "File: $SQL_FILE"
echo ""

# Database connection parameters
DB_NAME="onlineshop"
DB_USER="onlineshop"
DB_HOST="db"
DB_PORT="5432"

# Export password for psql
export PGPASSWORD="onlineshop"

# Import SQL file using psql
echo "Importing SQL file into database..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ SQL backup imported successfully!"
else
    echo ""
    echo "✗ Error importing SQL backup"
    exit 1
fi

# Unset password
unset PGPASSWORD

