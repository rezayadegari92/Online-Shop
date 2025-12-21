#!/bin/bash
# Alternative method: Import SQL backup using Docker and psql
# This method is more reliable for complex SQL dumps

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
echo "Importing SQL backup using Docker"
echo "=========================================="
echo "File: $SQL_FILE"
echo ""

# Check if docker compose is available
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    echo "Error: docker-compose or docker compose not found"
    exit 1
fi

# Import SQL file
echo "Importing SQL file into database..."
$DOCKER_COMPOSE exec -T db psql -U onlineshop -d onlineshop < "$SQL_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ SQL backup imported successfully!"
else
    echo ""
    echo "✗ Error importing SQL backup"
    exit 1
fi

