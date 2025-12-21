#!/bin/bash
# Database Migration Script for Dokploy
# This script helps migrate your database from local Docker to Dokploy container

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${GREEN}ℹ${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Function to export database
export_database() {
    local output_file=${1:-"backup_$(date +%Y%m%d_%H%M%S).sql"}
    
    print_info "Exporting database..."
    echo "Output file: $output_file"
    echo ""
    
    # Check if we're in Docker or have direct access
    if command -v docker-compose &> /dev/null || docker compose version &> /dev/null; then
        # Use Docker
        if command -v docker-compose &> /dev/null; then
            DOCKER_COMPOSE="docker-compose"
        else
            DOCKER_COMPOSE="docker compose"
        fi
        
        print_info "Using Docker to export database..."
        $DOCKER_COMPOSE exec -T db pg_dump -U onlineshop -d onlineshop \
            --clean --if-exists --no-owner --no-acl > "$output_file"
    else
        # Direct connection
        export PGPASSWORD=onlineshop
        pg_dump -h localhost -U onlineshop -d onlineshop \
            --clean --if-exists --no-owner --no-acl \
            -f "$output_file"
        unset PGPASSWORD
    fi
    
    if [ $? -eq 0 ]; then
        local file_size=$(du -h "$output_file" | cut -f1)
        print_success "Database exported successfully!"
        echo "  File: $output_file"
        echo "  Size: $file_size"
        echo "$output_file"
    else
        print_error "Failed to export database"
        exit 1
    fi
}

# Function to import database to Dokploy
import_to_dokploy() {
    local sql_file=$1
    local dokploy_host=${DOKPLOY_DB_HOST:-${2:-"localhost"}}
    local dokploy_port=${DOKPLOY_DB_PORT:-${3:-"5432"}}
    local dokploy_db=${DOKPLOY_DB_NAME:-${4:-"onlineshop"}}
    local dokploy_user=${DOKPLOY_DB_USER:-${5:-"onlineshop"}}
    local dokploy_password=${DOKPLOY_DB_PASSWORD:-${6:-""}}
    
    if [ ! -f "$sql_file" ]; then
        print_error "SQL file not found: $sql_file"
        exit 1
    fi
    
    if [ -z "$dokploy_password" ]; then
        print_error "Dokploy database password not provided!"
        echo "Set DOKPLOY_DB_PASSWORD environment variable or provide as argument"
        exit 1
    fi
    
    print_info "Importing to Dokploy database..."
    echo "  Host: $dokploy_host:$dokploy_port"
    echo "  Database: $dokploy_db"
    echo "  User: $dokploy_user"
    echo "  SQL File: $sql_file"
    echo ""
    
    export PGPASSWORD="$dokploy_password"
    psql -h "$dokploy_host" -p "$dokploy_port" -U "$dokploy_user" -d "$dokploy_db" -f "$sql_file"
    local exit_code=$?
    unset PGPASSWORD
    
    if [ $exit_code -eq 0 ]; then
        print_success "Database imported successfully to Dokploy!"
    else
        print_error "Failed to import database"
        exit 1
    fi
}

# Function to show usage
show_usage() {
    echo "Database Migration Script for Dokploy"
    echo ""
    echo "Usage:"
    echo "  $0 export [output_file]              # Export current database"
    echo "  $0 import <sql_file>                 # Import to Dokploy (uses env vars)"
    echo "  $0 migrate                           # Full migration (export + import)"
    echo ""
    echo "Environment Variables for Dokploy:"
    echo "  DOKPLOY_DB_HOST      - Dokploy database host (default: localhost)"
    echo "  DOKPLOY_DB_PORT      - Dokploy database port (default: 5432)"
    echo "  DOKPLOY_DB_NAME      - Dokploy database name (default: onlineshop)"
    echo "  DOKPLOY_DB_USER      - Dokploy database user (default: onlineshop)"
    echo "  DOKPLOY_DB_PASSWORD  - Dokploy database password (required)"
    echo ""
    echo "Examples:"
    echo "  # Export database"
    echo "  $0 export"
    echo ""
    echo "  # Import to Dokploy"
    echo "  export DOKPLOY_DB_HOST=your-dokploy-host"
    echo "  export DOKPLOY_DB_PASSWORD=your-password"
    echo "  $0 import backup_20251221_142048.sql"
    echo ""
    echo "  # Full migration"
    echo "  export DOKPLOY_DB_HOST=your-dokploy-host"
    echo "  export DOKPLOY_DB_PASSWORD=your-password"
    echo "  $0 migrate"
}

# Main script
case "${1:-}" in
    export)
        output_file=$(export_database "${2:-}")
        echo ""
        print_success "Export completed: $output_file"
        ;;
    import)
        if [ -z "${2:-}" ]; then
            print_error "SQL file required for import"
            show_usage
            exit 1
        fi
        import_to_dokploy "$2" "${3:-}" "${4:-}" "${5:-}" "${6:-}" "${7:-}"
        ;;
    migrate)
        print_info "Starting full migration..."
        echo ""
        output_file=$(export_database)
        echo ""
        import_to_dokploy "$output_file"
        echo ""
        print_success "Migration completed!"
        echo "Backup file: $output_file"
        ;;
    *)
        show_usage
        exit 1
        ;;
esac

