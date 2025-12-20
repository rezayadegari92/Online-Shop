# Online Shop Setup Guide

## Prerequisites

- Docker & Docker Compose installed
- Ports 3000, 8000, 5432, 6379 available

## ⚠️ Database Issues? Run This First!

If you see **empty results** or **old data** in the API/admin:

```bash
# Check database status
docker-compose exec web python check_database.py

# Fix database issues (automated)
chmod +x fix_database.sh
./fix_database.sh

# Or manually:
docker-compose down
docker volume rm online-shop_postgres_data
docker-compose up -d
sleep 10
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py create_sample_data
```

## Quick Setup

```bash
# 1. Navigate to project
cd Online-Shop/Online-Shop

# 2. Start services
docker-compose up -d

# 3. Wait for services to be ready (30 seconds)
docker-compose logs -f web

# 4. Run migrations
docker-compose exec web python manage.py migrate

# 5. Create sample data
docker-compose exec web python manage.py create_sample_data

# 6. (Optional) Create admin user
docker-compose exec web python manage.py createsuperuser

# 7. Test the API
curl http://localhost:8000/api/products/
```

## Services

After `docker-compose up -d`, the following services will be running:

| Service | Container | Port | Description |
|---------|-----------|------|-------------|
| **Frontend** | onlineshop_frontend | 3000 | Vue.js frontend |
| **Backend** | onlineshop_web | 8000 | Django REST API |
| **Database** | onlineshop_db | 5432 | PostgreSQL |
| **Cache** | onlineshop_redis | 6379 | Redis cache & broker |
| **Worker** | onlineshop_celery | - | Celery worker |
| **Scheduler** | onlineshop_celery_beat | - | Celery Beat scheduler |

## URLs

- **Frontend:** http://localhost:3000
- **API:** http://localhost:8000/api/
- **Admin:** http://localhost:8000/admin/
- **API Docs:** http://localhost:8000/api/schema/swagger-ui/

## Verify Installation

```bash
# Check all services are running
docker-compose ps

# Check database connection
docker-compose exec web python manage.py check

# Test cache
docker-compose exec web python test_cache_fix.py

# Check Redis
docker-compose exec redis redis-cli ping  # Should return: PONG

# View logs
docker-compose logs -f web
docker-compose logs -f celery-beat
```

## Sample Data

The `create_sample_data` command creates:

- **17 Products:**
  - 4 Smartphones (iPhone, Samsung Galaxy)
  - 5 Laptops (MacBook, Dell XPS, HP, Lenovo)
  - 3 Tablets (iPad, Galaxy Tab)
  - 5 Clothing items (Nike, Adidas)

- **8 Categories:**
  - Electronics → Smartphones, Laptops, Tablets
  - Clothing → Men's, Women's
  - Home & Kitchen

- **7 Brands:**
  - Apple, Samsung, Dell, HP, Lenovo, Nike, Adidas

- **Discounts:**
  - Many products have 5-30% discounts

### Custom Data

```bash
# Clear all data and create fresh
docker-compose exec web python manage.py create_sample_data --clear

# Access Django shell to create custom data
docker-compose exec web python manage.py shell
```

## Cache Management

### Warm Cache (Pre-populate)
```bash
# Warm all critical caches
docker-compose exec web python manage.py warm_cache --all

# Warm specific types
docker-compose exec web python manage.py warm_cache --products
docker-compose exec web python manage.py warm_cache --categories
```

### Clear Cache
```bash
# Clear all cache
docker-compose exec web python manage.py clear_cache --all

# Clear specific types
docker-compose exec web python manage.py clear_cache --products
docker-compose exec web python manage.py clear_cache --categories
```

### Monitor Cache
```bash
# View cache hits
docker-compose logs web | grep "Cache HIT"

# View Celery Beat tasks
docker-compose logs celery-beat | grep "succeeded"

# Check Redis keys
docker-compose exec redis redis-cli KEYS "onlineshop:*"
```

## Troubleshooting

### Services Not Starting

```bash
# Check logs
docker-compose logs web
docker-compose logs db

# Restart services
docker-compose restart

# Rebuild images
docker-compose down
docker-compose up --build
```

### Database Connection Error

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Wait longer for database to be ready
sleep 10
docker-compose exec web python manage.py migrate
```

### Empty API Results or Old Data

**Problem:** API returns `{"results": []}` or shows old data that's not in admin/swagger.

**Cause:** Database volume has old data or migrations weren't run.

**Solution:**

```bash
# Option 1: Use fix script (recommended)
chmod +x fix_database.sh
./fix_database.sh

# Option 2: Manual fix
# 1. Check current state
docker-compose exec web python check_database.py

# 2. Reset database completely
docker-compose down
docker volume rm online-shop_postgres_data
docker-compose up -d
sleep 10

# 3. Run migrations
docker-compose exec web python manage.py migrate

# 4. Create sample data
docker-compose exec web python manage.py create_sample_data

# 5. Clear cache
docker-compose exec web python manage.py clear_cache --all

# 6. Verify
curl http://localhost:8000/api/products/
```

**Verify in multiple places:**
- API: http://localhost:8000/api/products/
- Admin: http://localhost:8000/admin/products/product/
- Swagger: http://localhost:8000/api/schema/swagger-ui/
- Frontend: http://localhost:3000

### Cache Errors

```bash
# Check Redis is running
docker-compose exec redis redis-cli ping

# Test cache manually
docker-compose exec web python test_cache_fix.py

# Restart services
docker-compose restart web celery celery-beat
```

### Port Already in Use

```bash
# Change ports in docker-compose.yml
# Example: Change "8000:8000" to "8001:8000"
vim docker-compose.yml

# Restart
docker-compose down
docker-compose up -d
```

## Development

### Apply Migrations

```bash
# Create migrations
docker-compose exec web python manage.py makemigrations

# Apply migrations
docker-compose exec web python manage.py migrate
```

### Access Django Shell

```bash
docker-compose exec web python manage.py shell
```

### Run Tests

```bash
docker-compose exec web python manage.py test
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f web
docker-compose logs -f celery-beat

# Last 100 lines
docker-compose logs --tail 100 web
```

## Stop Services

```bash
# Stop containers (keep data)
docker-compose stop

# Stop and remove containers (keep volumes)
docker-compose down

# Stop and remove everything including volumes (DELETES DATA!)
docker-compose down -v
```

## Production Considerations

1. **Environment Variables**
   - Set proper `SECRET_KEY` in production
   - Use secure passwords for database
   - Configure `ALLOWED_HOSTS`
   - Set `DEBUG=False`

2. **Database**
   - Use managed PostgreSQL service
   - Regular backups
   - Connection pooling

3. **Redis**
   - Use managed Redis service
   - Set `maxmemory-policy`
   - Monitor memory usage

4. **Static Files**
   - Run `collectstatic`
   - Use CDN for static/media files

5. **Security**
   - Use HTTPS
   - Set secure headers
   - Enable CSRF protection

## API Endpoints

### Products
- `GET /api/products/` - List products (cached 10 min)
- `GET /api/products/{id}/` - Product detail (cached 15 min)
- `GET /api/products/top-rated/` - Top rated products
- `GET /api/products/discounted/` - Discounted products
- `POST /api/products/{id}/` - Add comment/rating (auth required)

### Categories
- `GET /api/categories/` - List categories (cached 30 min)
- `GET /api/categories/{id}/products/` - Products by category

### Brands
- `GET /api/brands/` - List brands (cached 30 min)
- `GET /api/brands/{id}/products/` - Products by brand

### Authentication
- `POST /api/accounts/signup/` - Customer signup
- `POST /api/accounts/verify-otp/` - Verify OTP
- `POST /api/accounts/login/` - Login
- `POST /api/accounts/logout/` - Logout
- `GET /api/accounts/profile/` - User profile (auth required)

### Orders
- `GET /api/orders/` - List orders (auth required)
- `GET /api/orders/{id}/` - Order detail (auth required)

### Cart
- `GET /api/cart/` - View cart
- `POST /api/cart/items/` - Add item to cart
- `DELETE /api/cart/items/{id}/` - Remove item

## Support

For detailed documentation:
- **Cache Guide:** `CACHE_README.md`
- **Stampede Prevention:** `CACHE_STAMPEDE_PREVENTION.md`
- **General Docs:** `CACHING.md`
