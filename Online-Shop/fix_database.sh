#!/bin/bash
# Database Fix Script for Online Shop
# This script fixes common database issues

echo "========================================"
echo "Online Shop Database Fix Script"
echo "========================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: docker-compose not found${NC}"
    echo "Please install docker-compose first"
    exit 1
fi

echo "Step 1: Checking services..."
docker-compose ps

echo ""
echo "Step 2: Running database diagnostics..."
docker-compose exec web python check_database.py

echo ""
echo -e "${YELLOW}Do you want to reset the database? This will delete all data! (y/N)${NC}"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo -e "${YELLOW}Resetting database...${NC}"

    # Stop services
    echo "Stopping services..."
    docker-compose stop web celery celery-beat

    # Remove database volume
    echo "Removing database volume..."
    docker-compose down
    docker volume rm online-shop_postgres_data 2>/dev/null || true

    # Start services
    echo "Starting services..."
    docker-compose up -d

    # Wait for database
    echo "Waiting for database to be ready..."
    sleep 10

    # Run migrations
    echo "Running migrations..."
    docker-compose exec web python manage.py migrate

    # Create sample data
    echo "Creating sample data..."
    docker-compose exec web python manage.py create_sample_data

    # Clear cache
    echo "Clearing cache..."
    docker-compose exec web python manage.py clear_cache --all 2>/dev/null || true

    echo ""
    echo -e "${GREEN}✓ Database reset complete!${NC}"
    echo ""
    echo "You can now:"
    echo "  1. Access API: http://localhost:8000/api/products/"
    echo "  2. Access Admin: http://localhost:8000/admin/"
    echo "     (Create superuser: docker-compose exec web python manage.py createsuperuser)"
    echo "  3. Access Frontend: http://localhost:3000"

else
    echo ""
    echo -e "${YELLOW}Running migrations only...${NC}"

    # Run migrations
    docker-compose exec web python manage.py migrate

    # Check if database is empty
    product_count=$(docker-compose exec web python manage.py shell -c "from products.models import Product; print(Product.objects.count())" 2>/dev/null | tail -1)

    if [ "$product_count" = "0" ]; then
        echo ""
        echo -e "${YELLOW}Database is empty. Create sample data? (y/N)${NC}"
        read -r create_data

        if [[ "$create_data" =~ ^([yY][eE][sS]|[yY])$ ]]; then
            docker-compose exec web python manage.py create_sample_data
            echo -e "${GREEN}✓ Sample data created!${NC}"
        fi
    else
        echo -e "${GREEN}✓ Database has $product_count products${NC}"
    fi
fi

echo ""
echo "========================================"
echo "Final Check"
echo "========================================"
docker-compose exec web python check_database.py

echo ""
echo -e "${GREEN}Done!${NC}"
