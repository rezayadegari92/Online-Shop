# Redis Caching Implementation Guide

## Overview

This online shop application uses **Redis** for caching frequently accessed data to improve performance and reduce database load. Caching is implemented for product listings, category data, brand information, and other read-heavy endpoints.

## Architecture

```
┌─────────────┐      ┌─────────────┐      ┌──────────────┐
│   Client    │─────▶│   Django    │─────▶│  PostgreSQL  │
│  (Browser)  │      │     API     │      │   Database   │
└─────────────┘      └─────────────┘      └──────────────┘
                            │
                            ▼
                     ┌─────────────┐
                     │    Redis    │
                     │    Cache    │
                     └─────────────┘
```

## Cached Endpoints

### High Priority (Frequently Accessed)

| Endpoint | Cache Key Prefix | TTL | Description |
|----------|-----------------|-----|-------------|
| `GET /api/products/` | `product_list` | 10 min | Product list with search/filter |
| `GET /api/products/{id}/` | `product_detail` | 15 min | Individual product details |
| `GET /api/categories/` | `category_list` | 30 min | Category hierarchy |

### Medium Priority

| Endpoint | Cache Key Prefix | TTL | Description |
|----------|-----------------|-----|-------------|
| `GET /api/products/top-rated/` | `top_rated` | 15 min | Top-rated products |
| `GET /api/products/discounted/` | `discounted` | 10 min | Discounted products |
| `GET /api/brands/` | `brand_list` | 30 min | All brands |

### Low Priority

| Endpoint | Cache Key Prefix | TTL | Description |
|----------|-----------------|-----|-------------|
| `GET /api/brands/{id}/products/` | `brand_products` | 10 min | Products by brand |
| `GET /api/categories/{id}/products/` | `category_products` | 10 min | Products by category |

## Configuration

### Settings (`core/settings.py`)

```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {
                "max_connections": 50,
                "retry_on_timeout": True,
            },
        },
        "KEY_PREFIX": "onlineshop",
        "TIMEOUT": 300,  # 5 minutes default
    }
}

# Custom cache TTLs (in seconds)
CACHE_TTL = {
    "PRODUCT_LIST": 600,      # 10 minutes
    "PRODUCT_DETAIL": 900,    # 15 minutes
    "CATEGORY_LIST": 1800,    # 30 minutes
    "TOP_RATED": 900,         # 15 minutes
    "DISCOUNTED": 600,        # 10 minutes
    "BRAND_LIST": 1800,       # 30 minutes
}
```

### Environment Variables

```bash
REDIS_URL=redis://redis:6379/1  # Override default Redis connection
```

## Cache Keys Structure

Cache keys are generated using query parameters to ensure unique keys for different requests:

```
Format: {prefix}:{param1}={value1}:{param2}={value2}

Examples:
- product_list:search=laptop:category=1:page=1
- product_detail:pk=42
- category_products:pk=5:page=2
- top_rated:page=1:page_size=20
```

## Automatic Cache Invalidation

The system automatically invalidates cache when data changes using Django signals:

### Product Changes
- **Create/Update/Delete Product** → Invalidates:
  - Product detail cache for that product
  - All product lists
  - Top-rated lists
  - Discounted lists
  - Category/brand product lists

### Rating Changes
- **Add/Update/Delete Rating** → Invalidates:
  - Product detail for rated product
  - Top-rated product lists

### Comment Changes
- **Add/Update/Delete Comment** → Invalidates:
  - Product detail for commented product

### Category Changes
- **Create/Update/Delete Category** → Invalidates:
  - Category list
  - Category products
  - All product lists

### Brand Changes
- **Create/Update/Delete Brand** → Invalidates:
  - Brand list
  - Brand products
  - All product lists

## Manual Cache Management

### Clear All Cache

```bash
docker-compose exec web python manage.py clear_cache --all
```

### Clear Specific Cache Types

```bash
# Clear only product cache
docker-compose exec web python manage.py clear_cache --products

# Clear only category cache
docker-compose exec web python manage.py clear_cache --categories

# Clear only brand cache
docker-compose exec web python manage.py clear_cache --brands
```

### Using Django Shell

```python
from django.core.cache import cache
from core.cache_utils import *

# Clear all cache
cache.clear()

# Invalidate specific patterns
invalidate_product_cache()
invalidate_category_cache()
invalidate_brand_cache()

# Invalidate specific item
invalidate_product_cache(product_id=42)
invalidate_category_cache(category_id=5)
invalidate_brand_cache(brand_id=3)
```

## Performance Benefits

### Before Caching (Example Metrics)

| Endpoint | Avg Response Time | DB Queries |
|----------|-------------------|------------|
| Product List | 250ms | 15 |
| Product Detail | 120ms | 8 |
| Top Rated | 380ms | 25 |

### After Caching (Cache Hit)

| Endpoint | Avg Response Time | DB Queries |
|----------|-------------------|------------|
| Product List | 15ms | 0 |
| Product Detail | 8ms | 0 |
| Top Rated | 12ms | 0 |

**Expected improvements:**
- 🚀 **94% faster** response times on cache hits
- 📉 **0 database queries** on cached responses
- ⚡ **10x-20x** throughput increase
- 💾 **Reduced database load** by 70-80%

## Cache Monitoring

### Check Cache Status

```python
from django_redis import get_redis_connection

redis_conn = get_redis_connection("default")

# Get cache info
info = redis_conn.info()
print(f"Used memory: {info['used_memory_human']}")
print(f"Connected clients: {info['connected_clients']}")
print(f"Total keys: {redis_conn.dbsize()}")

# List all cache keys (use with caution in production)
keys = redis_conn.keys("onlineshop:*")
print(f"Total cache keys: {len(keys)}")
```

### Cache Hit Rate Calculation

Add this to your monitoring/logging:

```python
import logging
from django.core.cache import cache

logger = logging.getLogger(__name__)

# In your view
cache_key = generate_cache_key("product_list", **params)
cached = cache.get(cache_key)

if cached:
    logger.info(f"Cache HIT: {cache_key}")
else:
    logger.info(f"Cache MISS: {cache_key}")
```

## Best Practices

### ✅ DO

1. **Cache read-heavy endpoints** that don't change frequently
2. **Use appropriate TTLs** based on data volatility
3. **Include relevant query parameters** in cache keys
4. **Invalidate cache on data changes** using signals
5. **Monitor cache hit rates** and adjust TTLs accordingly
6. **Use cache versioning** for breaking changes

### ❌ DON'T

1. **Don't cache user-specific data** without user ID in key
2. **Don't cache sensitive data** like passwords or payment info
3. **Don't use extremely long TTLs** (>1 hour) for volatile data
4. **Don't forget to invalidate** related caches
5. **Don't cache error responses** (only 200 OK)

## Troubleshooting

### Cache Not Working

1. **Check Redis connection:**
   ```bash
   docker-compose exec redis redis-cli ping
   # Should return: PONG
   ```

2. **Verify Django can connect:**
   ```bash
   docker-compose exec web python manage.py shell
   >>> from django.core.cache import cache
   >>> cache.set('test', 'value')
   >>> cache.get('test')
   'value'
   ```

3. **Check logs for errors:**
   ```bash
   docker-compose logs web | grep -i cache
   docker-compose logs redis
   ```

### Cache Not Invalidating

1. **Verify signals are registered:**
   ```bash
   docker-compose exec web python manage.py shell
   >>> from products.apps import ProductsConfig
   >>> ProductsConfig.name
   'products'
   ```

2. **Check signal execution in logs:**
   ```bash
   docker-compose logs web | grep "Cache invalidated"
   ```

3. **Manually invalidate:**
   ```bash
   docker-compose exec web python manage.py clear_cache --all
   ```

### High Memory Usage

1. **Check Redis memory:**
   ```bash
   docker-compose exec redis redis-cli info memory
   ```

2. **Reduce TTLs** in `settings.CACHE_TTL`

3. **Implement LRU eviction:**
   ```bash
   # In Redis config or docker-compose
   maxmemory 256mb
   maxmemory-policy allkeys-lru
   ```

## Advanced Usage

### Custom Cache Decorator

```python
from core.cache_utils import cache_view_response

@cache_view_response(
    'my_custom_endpoint',
    timeout=600,
    query_params=['search', 'category', 'page']
)
def get(self, request):
    # Your view logic
    return Response(data)
```

### Conditional Caching

```python
def get(self, request):
    # Skip cache for authenticated users
    if request.user.is_authenticated:
        return self._get_fresh_data(request)
    
    # Use cache for anonymous users
    cache_key = generate_cache_key('products', **params)
    return get_or_set_cache(cache_key, lambda: self._get_fresh_data(request))
```

### Cache Warming

```python
# Warm up cache after deployment
from products.models import Product
from products.api.serializers import ProductSerializer

def warm_cache():
    products = Product.objects.all()[:100]
    for product in products:
        serializer = ProductSerializer(product)
        cache_key = f"product_detail:pk={product.id}"
        cache.set(cache_key, serializer.data, 900)
```

## Production Considerations

### Scaling Redis

For production with high traffic:

```yaml
# docker-compose.yml
redis:
  image: redis:7-alpine
  command: redis-server --maxmemory 512mb --maxmemory-policy allkeys-lru
  volumes:
    - redis_data:/data
  deploy:
    resources:
      limits:
        memory: 512M
```

### Redis Cluster (Optional)

For very high traffic, consider Redis Cluster:
- **Redis Sentinel** for high availability
- **Redis Cluster** for horizontal scaling
- **ElastiCache** (AWS) or **Cloud Memorystore** (GCP)

### Monitoring Tools

- **RedisInsight** - GUI for Redis monitoring
- **Prometheus + Grafana** - Metrics and dashboards
- **Django Debug Toolbar** - Cache panel for development

## FAQ

**Q: Why use Redis instead of Memcached?**  
A: Redis offers persistence, data structures, pub/sub, and is used for both cache and Celery broker.

**Q: What happens if Redis goes down?**  
A: The application will continue to work, fetching data from PostgreSQL directly. No data loss occurs.

**Q: Should I cache POST/PUT/DELETE requests?**  
A: No, only cache GET requests. Mutations should invalidate cache instead.

**Q: How do I test caching locally?**  
A: Use the same Docker setup. Monitor cache hits in logs or use Redis CLI.

**Q: Can I disable caching for development?**  
A: Yes, set `CACHES['default']['BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'`

## References

- [Django Caching Documentation](https://docs.djangoproject.com/en/4.2/topics/cache/)
- [django-redis Documentation](https://github.com/jazzband/django-redis)
- [Redis Documentation](https://redis.io/documentation)
- [REST API Caching Best Practices](https://restfulapi.net/caching/)

---

**Last Updated:** 2024  
**Maintained By:** Development Team