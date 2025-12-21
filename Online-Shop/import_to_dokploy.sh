#!/bin/bash
# Simple script to import SQL backup to Dokploy
# Usage: ./import_to_dokploy.sh <sql_file> [dokploy_password]

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${GREEN}ℹ${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Check if SQL file is provided
if [ -z "${1:-}" ]; then
    print_error "SQL file required!"
    echo ""
    echo "Usage:"
    echo "  $0 <sql_file> [dokploy_password]"
    echo ""
    echo "Or set environment variables:"
    echo "  export DOKPLOY_DB_PASSWORD=your-password"
    echo "  export DOKPLOY_DB_HOST=your-host (optional, default: localhost)"
    echo "  $0 backup_20251221_142048.sql"
    exit 1
fi

SQL_FILE="$1"
DOKPLOY_PASSWORD="${2:-${DOKPLOY_DB_PASSWORD:-}}"

# Dokploy database config
DOKPLOY_DB_HOST=${DOKPLOY_DB_HOST:-"localhost"}
DOKPLOY_DB_PORT=${DOKPLOY_DB_PORT:-"5432"}
DOKPLOY_DB_NAME=${DOKPLOY_DB_NAME:-"onlineshop"}
DOKPLOY_DB_USER=${DOKPLOY_DB_USER:-"onlineshop"}

# Check if file exists
if [ ! -f "$SQL_FILE" ]; then
    print_error "SQL file not found: $SQL_FILE"
    echo ""
    echo "Current directory: $(pwd)"
    echo "Files in current directory:"
    ls -la *.sql 2>/dev/null || echo "No .sql files found"
    exit 1
fi

# Check if password is provided
if [ -z "$DOKPLOY_PASSWORD" ]; then
    print_error "Dokploy database password not provided!"
    echo ""
    echo "Please provide password in one of these ways:"
    echo "  1. As second argument: $0 $SQL_FILE your-password"
    echo "  2. As environment variable: export DOKPLOY_DB_PASSWORD=your-password"
    exit 1
fi

print_info "Importing to Dokploy database..."
echo "=========================================="
echo "  SQL File: $SQL_FILE"
echo "  Host: $DOKPLOY_DB_HOST:$DOKPLOY_DB_PORT"
echo "  Database: $DOKPLOY_DB_NAME"
echo "  User: $DOKPLOY_DB_USER"
echo "=========================================="
echo ""

# Check if psql is available
if ! command -v psql &> /dev/null; then
    print_error "psql command not found!"
    echo ""
    echo "Installing PostgreSQL client..."
    apt-get update -qq && apt-get install -y -qq postgresql-client > /dev/null 2>&1 || {
        print_error "Failed to install postgresql-client"
        echo "Please install it manually: apt-get install postgresql-client"
        exit 1
    }
fi

# Import SQL file
export PGPASSWORD="$DOKPLOY_PASSWORD"
print_info "Starting import (this may take a while)..."
echo ""

psql -h "$DOKPLOY_DB_HOST" \
     -p "$DOKPLOY_DB_PORT" \
     -U "$DOKPLOY_DB_USER" \
     -d "$DOKPLOY_DB_NAME" \
     -f "$SQL_FILE" \
     2>&1 | tee /tmp/import_output.log

EXIT_CODE=${PIPESTATUS[0]}
unset PGPASSWORD

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    print_success "Database imported successfully to Dokploy!"
    echo ""
    echo "File imported: $SQL_FILE"
else
    print_error "Failed to import database (exit code: $EXIT_CODE)"
    echo ""
    echo "Last 20 lines of output:"
    tail -20 /tmp/import_output.log
    echo ""
    echo "Check the full log: cat /tmp/import_output.log"
    exit 1
fi

