#!/bin/bash
# Migration script that uses database config from docker-compose.yml
# This script reads the database config from your docker-compose setup

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

# Database config from docker-compose.yml
DB_NAME="onlineshop"
DB_USER="onlineshop"
DB_PASSWORD="onlineshop"
DB_HOST="db"  # Docker service name, use 'localhost' if connecting from outside
DB_PORT="5432"

# Dokploy database config (you need to set these)
DOKPLOY_DB_HOST=${DOKPLOY_DB_HOST:-""}
DOKPLOY_DB_PORT=${DOKPLOY_DB_PORT:-"5432"}
DOKPLOY_DB_NAME=${DOKPLOY_DB_NAME:-"onlineshop"}
DOKPLOY_DB_USER=${DOKPLOY_DB_USER:-"onlineshop"}
DOKPLOY_DB_PASSWORD=${DOKPLOY_DB_PASSWORD:-""}

# Function to export from Docker database
export_from_docker() {
    local output_file=${1:-"backup_$(date +%Y%m%d_%H%M%S).sql"}
    
    print_info "Exporting from Docker database..."
    echo "  Database: $DB_NAME"
    echo "  Host: $DB_HOST"
    echo "  User: $DB_USER"
    echo "  Output: $output_file"
    echo ""
    
    # Check if we're inside Docker or outside
    if [ -f /.dockerenv ]; then
        # Inside Docker container - use direct connection
        export PGPASSWORD="$DB_PASSWORD"
        pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
            --clean --if-exists --no-owner --no-acl \
            -f "$output_file"
        unset PGPASSWORD
    else
        # Outside Docker - use docker compose
        if command -v docker-compose &> /dev/null; then
            DOCKER_COMPOSE="docker-compose"
        elif docker compose version &> /dev/null 2>&1; then
            DOCKER_COMPOSE="docker compose"
        else
            print_error "docker-compose not found!"
            exit 1
        fi
        
        $DOCKER_COMPOSE exec -T db pg_dump -U "$DB_USER" -d "$DB_NAME" \
            --clean --if-exists --no-owner --no-acl > "$output_file"
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

# Function to import to Dokploy
import_to_dokploy() {
    local sql_file=$1
    
    if [ ! -f "$sql_file" ]; then
        print_error "SQL file not found: $sql_file"
        exit 1
    fi
    
    if [ -z "$DOKPLOY_DB_PASSWORD" ]; then
        print_error "Dokploy database password not provided!"
        echo ""
        echo "Please set DOKPLOY_DB_PASSWORD environment variable:"
        echo "  export DOKPLOY_DB_PASSWORD=your-password"
        echo ""
        echo "Optional Dokploy settings:"
        echo "  export DOKPLOY_DB_HOST=your-host"
        echo "  export DOKPLOY_DB_PORT=5432"
        echo "  export DOKPLOY_DB_NAME=onlineshop"
        echo "  export DOKPLOY_DB_USER=onlineshop"
        exit 1
    fi
    
    print_info "Importing to Dokploy database..."
    echo "  Host: ${DOKPLOY_DB_HOST:-localhost}:${DOKPLOY_DB_PORT}"
    echo "  Database: $DOKPLOY_DB_NAME"
    echo "  User: $DOKPLOY_DB_USER"
    echo "  SQL File: $sql_file"
    echo ""
    
    export PGPASSWORD="$DOKPLOY_DB_PASSWORD"
    psql -h "${DOKPLOY_DB_HOST:-localhost}" \
         -p "$DOKPLOY_DB_PORT" \
         -U "$DOKPLOY_DB_USER" \
         -d "$DOKPLOY_DB_NAME" \
         -f "$sql_file"
    local exit_code=$?
    unset PGPASSWORD
    
    if [ $exit_code -eq 0 ]; then
        print_success "Database imported successfully to Dokploy!"
    else
        print_error "Failed to import database"
        exit 1
    fi
}

# Function to show current config
show_config() {
    echo "=========================================="
    echo "Current Database Configuration"
    echo "=========================================="
    echo ""
    echo "Docker Database (Source):"
    echo "  Host: $DB_HOST"
    echo "  Port: $DB_PORT"
    echo "  Database: $DB_NAME"
    echo "  User: $DB_USER"
    echo "  Password: $DB_PASSWORD"
    echo ""
    echo "Dokploy Database (Target):"
    echo "  Host: ${DOKPLOY_DB_HOST:-<not set>}"
    echo "  Port: ${DOKPLOY_DB_PORT:-5432}"
    echo "  Database: ${DOKPLOY_DB_NAME:-onlineshop}"
    echo "  User: ${DOKPLOY_DB_USER:-onlineshop}"
    echo "  Password: ${DOKPLOY_DB_PASSWORD:-<not set>}"
    echo "=========================================="
}

# Main script
case "${1:-}" in
    export)
        output_file=$(export_from_docker "${2:-}")
        echo ""
        print_success "Export completed: $output_file"
        ;;
    import)
        if [ -z "${2:-}" ]; then
            print_error "SQL file required for import"
            echo "Usage: $0 import <sql_file>"
            exit 1
        fi
        import_to_dokploy "$2"
        ;;
    migrate)
        print_info "Starting full migration..."
        echo ""
        output_file=$(export_from_docker)
        echo ""
        import_to_dokploy "$output_file"
        echo ""
        print_success "Migration completed!"
        echo "Backup file: $output_file"
        ;;
    config)
        show_config
        ;;
    *)
        echo "Database Migration Script (using docker-compose config)"
        echo ""
        echo "Usage:"
        echo "  $0 config                    # Show current configuration"
        echo "  $0 export [output_file]      # Export from Docker database"
        echo "  $0 import <sql_file>         # Import to Dokploy"
        echo "  $0 migrate                   # Full migration"
        echo ""
        echo "Dokploy Configuration (set as environment variables):"
        echo "  DOKPLOY_DB_HOST      - Dokploy database host"
        echo "  DOKPLOY_DB_PORT      - Dokploy database port (default: 5432)"
        echo "  DOKPLOY_DB_NAME      - Dokploy database name (default: onlineshop)"
        echo "  DOKPLOY_DB_USER      - Dokploy database user (default: onlineshop)"
        echo "  DOKPLOY_DB_PASSWORD  - Dokploy database password (required)"
        echo ""
        echo "Example:"
        echo "  export DOKPLOY_DB_HOST=your-dokploy-host"
        echo "  export DOKPLOY_DB_PASSWORD=your-password"
        echo "  $0 migrate"
        exit 1
        ;;
esac

