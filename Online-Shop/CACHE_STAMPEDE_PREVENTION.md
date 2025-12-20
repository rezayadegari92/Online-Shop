# Cache Stampede Prevention Guide 🛡️

## 📋 Table of Contents
- [What is Cache Stampede?](#what-is-cache-stampede)
- [Solutions Implemented](#solutions-implemented)
- [Method 1: Redis Lock-Based Prevention](#method-1-redis-lock-based-prevention)
- [Method 2: Probabilistic Early Expiration](#method-2-probabilistic-early-expiration)
- [Method 3: Stale-While-Revalidate](#method-3-stale-while-revalidate)
- [Method 4: Celery Beat Cache Warming](#method-4-celery-beat-cache-warming)
- [Comparison of Methods](#comparison-of-methods)
- [Configuration](#configuration)
- [Monitoring](#monitoring)
- [Best Practices](#best-practices)

---

## 🚨 What is Cache Stampede?

### The Problem

```
┌─────────────────────────────────────────────────────────┐
│  Popular Cache Entry Expires at 10:00:00               │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  1000 requests arrive at      │
        │  10:00:00.001                 │
        └───────────────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────┐
        │  All hit cache (MISS)         │
        │  All query database           │
        │  simultaneously               │
        └───────────────────────────────┘
                        │
                        ▼
                  💥 DATABASE
                   OVERLOAD
```

### Symptoms
- ⚠️ Sudden spike in database connections
- ⚠️ Slow response times during cache expiration
- ⚠️ Database CPU at 100%
- ⚠️ Multiple identical queries running simultaneously
- ⚠️ Cache hit rate drops to 0% periodically

### Impact
- 📉 Response time: 15ms → 5000ms
- 💰 Database costs spike
- 😞 Poor user experience
- 🔥 Potential service outage

---

## ✅ Solutions Implemented

We've implemented **4 complementary strategies** to prevent cache stampede:

| Method | Type | Effectiveness | Complexity | When to Use |
|--------|------|--------------|------------|-------------|
| **Redis Locks** | Reactive | ⭐⭐⭐⭐⭐ | Low | Always (default) |
| **Probabilistic Expiration** | Reactive | ⭐⭐⭐⭐ | Low | High traffic |
| **Stale-While-Revalidate** | Reactive | ⭐⭐⭐⭐⭐ | Medium | User-facing APIs |
| **Celery Beat Warming** | Proactive | ⭐⭐⭐⭐⭐ | High | Critical endpoints |

### Combined Approach (Recommended)

```
🛡️ Defense in Depth Strategy:

Layer 1: Celery Beat (Proactive)
   └─> Refreshes cache before expiration
   
Layer 2: Probabilistic Expiration (Reactive)
   └─> Spreads out cache regeneration
   
Layer 3: Redis Locks (Reactive)
   └─> Only one process computes value
   
Layer 4: Stale-While-Revalidate (Reactive)
   └─> Serve old data while refreshing
```

---

## 🔒 Method 1: Redis Lock-Based Prevention

### How It Works

```python
# When cache expires and 1000 requests arrive:

Request 1: Acquires lock → Computes value → Updates cache → Releases lock
Request 2-1000: Wait for lock → Get computed value from cache
```

### Implementation

Already enabled by default in all cached views:

```python
from core.cache_utils import cache_view_response

@cache_view_response(
    'product_list',
    timeout=600,
    prevent_stampede=True  # ✅ Default is True
)
def get(self, request):
    # Your view logic
    return Response(data)
```

### Configuration

```python
# In core/cache_utils.py

LOCK_TIMEOUT = 30  # Max time a lock can be held (seconds)
LOCK_WAIT_TIMEOUT = 10  # Max time to wait for lock (seconds)
```

### Flow Diagram

```
Request Arrives
    │
    ▼
Check Cache ────────► Cache Hit? ──Yes──► Return Cached
    │                                      Response
    │ No
    ▼
Try Acquire Lock
    │
    ├─► Lock Acquired? ──Yes──► Compute Value
    │                            │
    │                            ▼
    │                          Update Cache
    │                            │
    │                            ▼
    │                          Release Lock
    │                            │
    │                            ▼
    │                          Return Response
    │
    └─► Lock Held by Another? ──Yes──► Wait for Value
                                         │
                                         ▼
                                       Return Cached
                                       Response
```

### Advantages
✅ Simple to implement
✅ Prevents duplicate database queries
✅ No wasted computation
✅ Works automatically

### Disadvantages
❌ Waiting requests have higher latency
❌ Lock holder failure blocks all requests
❌ Requires Redis

---

## 🎲 Method 2: Probabilistic Early Expiration

### How It Works

Instead of all cache entries expiring at exactly the same time, we randomly expire them slightly early based on a probability formula:

```
probability = delta × log(time_since_creation) / ttl

Where:
- delta = 0.1 (10% factor)
- time_since_creation = original_timeout - current_ttl
- ttl = remaining time to live
```

### Implementation

Already enabled automatically in the lock-based approach:

```python
# In core/cache_utils.py

PROBABILISTIC_EXPIRATION_DELTA = 0.1  # 10% chance factor

def should_expire_early(ttl, original_timeout):
    """
    Probabilistically expire cache early.
    
    Example:
    - TTL: 600 seconds
    - Time since creation: 500 seconds
    - Probability: 0.1 × log(500) / 100 = 6.2%
    """
    probability = delta × log(time_since_creation) / ttl
    return random.random() < probability
```

### Benefits

```
Without Probabilistic Expiration:
All 1000 requests expire at 10:00:00
│
└─────────────────────────────────► 💥 STAMPEDE

With Probabilistic Expiration:
100 requests expire at 9:59:50
200 requests expire at 9:59:55
300 requests expire at 10:00:00
400 requests expire at 10:00:05
│
└─────────────────────────────────► ✅ Spread Out
```

### Configuration

```python
# Adjust in core/cache_utils.py

PROBABILISTIC_EXPIRATION_DELTA = 0.1  # Higher = more aggressive early expiration
```

### Advantages
✅ Spreads cache regeneration over time
✅ Reduces thundering herd effect
✅ No waiting for locks
✅ Works alongside other methods

### Disadvantages
❌ Slightly reduced cache hit rate
❌ Some requests still hit database
❌ Not deterministic

---

## ♻️ Method 3: Stale-While-Revalidate

### How It Works

Serve cached data even if expired, while refreshing in the background:

```
Request Arrives
    │
    ▼
Cache Expired? ──No──► Return Fresh Cache
    │
    │ Yes
    ▼
Return Stale Cache (fast!)
    │
    ├─► Trigger Background Refresh
    │
    └─► Next request gets fresh data
```

### Implementation

Enable per view:

```python
@cache_view_response(
    'product_list',
    timeout=600,
    prevent_stampede=True,
    use_stale=True  # ✅ Enable stale-while-revalidate
)
def get(self, request):
    return Response(data)
```

### User Experience

```
Traditional Cache:
User Request → Cache Miss → Wait 250ms → Get Response
                                ↑
                           DATABASE QUERY

Stale-While-Revalidate:
User Request → Stale Cache → Get Response in 15ms!
                   │
                   └─► Background: Refresh for next user
```

### Configuration

```python
# Enable globally in settings
CACHE_USE_STALE_DEFAULT = True

# Or per-view
@cache_view_response('products', use_stale=True)
```

### Advantages
✅ Best user experience (always fast)
✅ No waiting for cache refresh
✅ Gradual cache updates
✅ Works with locks

### Disadvantages
❌ Users may see slightly outdated data
❌ More complex implementation
❌ Requires background task support

---

## 🔥 Method 4: Celery Beat Cache Warming

### How It Works

**Proactively** refresh cache BEFORE it expires using scheduled tasks:

```
Cache TTL: 10 minutes
Warm Schedule: Every 5 minutes

Timeline:
10:00 ─► Cache created (expires 10:10)
10:05 ─► Celery warms cache (new expires 10:15) ✅
10:10 ─► Old cache would expire, but new cache exists!
10:15 ─► Celery warms again (new expires 10:25) ✅
```

### Implementation

#### 1. Celery Beat Schedule (Already Configured)

```python
# core/celery_config.py

celery_app.conf.beat_schedule = {
    'warm-all-critical-caches': {
        'task': 'cache.warm_all_critical',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'warm-product-list': {
        'task': 'cache.warm_product_list',
        'schedule': crontab(minute='*/3'),  # Every 3 minutes
    },
}
```

#### 2. Start Celery Beat

```bash
# Automatically started with docker-compose
docker-compose up -d

# Or manually
celery -A core.celery_config beat --loglevel=info
```

#### 3. Verify It's Running

```bash
# Check Celery Beat logs
docker-compose logs celery-beat -f

# Expected output:
# [2024-01-01 10:05:00] Scheduler: Sending due task cache.warm_product_list
# [2024-01-01 10:05:01] Task cache.warm_product_list succeeded
```

### Manual Cache Warming

```bash
# Warm all critical caches
python manage.py warm_cache --all

# Warm specific types
python manage.py warm_cache --products
python manage.py warm_cache --categories
python manage.py warm_cache --brands
python manage.py warm_cache --top

# Warm specific products
python manage.py warm_cache --details --product-ids 1 2 3 4 5
```

### Scheduled Tasks

| Task | Schedule | Purpose |
|------|----------|---------|
| `warm-all-critical-caches` | Every 5 min | Warm all endpoints |
| `warm-product-list` | Every 3 min | Most accessed |
| `warm-top-products` | Every 5 min | Top rated/discounted |
| `warm-categories` | Every 15 min | Rarely change |
| `warm-brands` | Every 15 min | Rarely change |

### Advantages
✅ **Zero cache misses** on warmed endpoints
✅ Predictable performance
✅ No user-facing delays
✅ Best for critical pages

### Disadvantages
❌ Requires Celery infrastructure
❌ Uses more resources (pre-computing)
❌ May warm unused cache entries
❌ More complex setup

---

## 📊 Comparison of Methods

### Performance Impact

| Method | Cache Miss Latency | Database Load | Complexity |
|--------|-------------------|---------------|------------|
| **No Prevention** | 250ms | 100% | None |
| **Redis Locks** | 250ms (1st) / 15ms (others) | ~10% | Low |
| **Probabilistic** | 250ms | ~20% | Low |
| **Stale-While-Revalidate** | 15ms (always!) | ~10% | Medium |
| **Celery Beat** | 15ms (always!) | ~5% | High |

### When to Use Each

```python
# HIGH TRAFFIC endpoints (>1000 req/min)
# Use: Locks + Probabilistic + Celery Beat
@cache_view_response(
    'product_list',
    timeout=600,
    prevent_stampede=True,  # Locks
    # Probabilistic is automatic
)
# + Celery Beat warming every 3-5 minutes

# MEDIUM TRAFFIC endpoints (100-1000 req/min)
# Use: Locks + Probabilistic
@cache_view_response(
    'brand_products',
    timeout=600,
    prevent_stampede=True,
)

# LOW TRAFFIC endpoints (<100 req/min)
# Use: Just locks (or nothing)
@cache_view_response(
    'rarely_accessed',
    timeout=600,
    prevent_stampede=False,  # Not needed
)

# USER-FACING endpoints (need best UX)
# Use: Stale-While-Revalidate + Locks
@cache_view_response(
    'homepage_products',
    timeout=600,
    prevent_stampede=True,
    use_stale=True,  # Always fast
)
```

---

## ⚙️ Configuration

### Global Settings

```python
# core/settings.py

# Cache TTLs
CACHE_TTL = {
    "PRODUCT_LIST": 600,       # 10 min - Warm every 5 min
    "PRODUCT_DETAIL": 900,     # 15 min - Warm every 10 min
    "CATEGORY_LIST": 1800,     # 30 min - Warm every 15 min
}

# Stampede prevention
CACHE_STAMPEDE_PREVENTION = {
    "ENABLED": True,
    "LOCK_TIMEOUT": 30,
    "LOCK_WAIT_TIMEOUT": 10,
    "PROBABILISTIC_DELTA": 0.1,
    "USE_STALE_DEFAULT": False,
}
```

### Per-View Configuration

```python
# Most aggressive (all methods)
@cache_view_response(
    'critical_endpoint',
    timeout=300,
    prevent_stampede=True,
    use_stale=True,
)
# + Celery Beat warming

# Moderate (locks + probabilistic)
@cache_view_response(
    'standard_endpoint',
    timeout=600,
    prevent_stampede=True,
)

# Minimal (no prevention)
@cache_view_response(
    'low_traffic_endpoint',
    timeout=1800,
    prevent_stampede=False,
)
```

### Celery Beat Schedule Tuning

```python
# core/celery_config.py

# More aggressive (higher traffic)
'warm-product-list': {
    'schedule': crontab(minute='*/2'),  # Every 2 minutes
}

# Less aggressive (lower traffic)
'warm-categories': {
    'schedule': crontab(minute='*/30'),  # Every 30 minutes
}

# Peak hours only
'warm-hot-products': {
    'schedule': crontab(
        minute='*/5',
        hour='9-18'  # Only 9am-6pm
    ),
}
```

---

## 📈 Monitoring

### Check Cache Stampede Occurrence

```bash
# Look for multiple lock acquisitions
docker-compose logs web | grep "Lock acquired, computing"

# Look for lock waits
docker-compose logs web | grep "Lock held by another process"

# Check probabilistic early expirations
docker-compose logs web | grep "Probabilistic early expiration"
```

### Metrics to Track

```python
# Add to your monitoring

# Cache stampede indicators
cache_miss_rate = cache_misses / total_requests
lock_wait_count = redis.get('lock_waits')
concurrent_recomputes = redis.get('concurrent_cache_builds')

# Alerts
if cache_miss_rate > 0.3:  # >30% miss rate
    alert("Potential cache stampede")

if concurrent_recomputes > 10:
    alert("Too many concurrent cache builds")
```

### Celery Beat Monitoring

```bash
# Check if Celery Beat is running
docker-compose ps celery-beat

# View scheduled tasks
docker-compose exec celery-beat celery -A core.celery_config inspect scheduled

# Check task success rate
docker-compose logs celery-beat | grep "succeeded"
docker-compose logs celery-beat | grep "failed"
```

### Dashboard Metrics

Track these in your monitoring dashboard (Grafana/Datadog):

```
┌─────────────────────────────────────┐
│  Cache Performance Dashboard        │
├─────────────────────────────────────┤
│  Cache Hit Rate: 94.5%  📈          │
│  Cache Miss Rate: 5.5%  📉          │
│  Lock Acquisitions: 12/min          │
│  Lock Waits: 45/min                 │
│  Probabilistic Expirations: 8/min   │
│  Celery Beat Tasks: 12 ✅ / 0 ❌    │
│  Avg Response Time: 18ms            │
│  P99 Response Time: 85ms            │
└─────────────────────────────────────┘
```

---

## 🎯 Best Practices

### DO ✅

1. **Enable stampede prevention by default**
   ```python
   prevent_stampede=True  # Default
   ```

2. **Use Celery Beat for critical endpoints**
   - Homepage products
   - Top-rated items
   - Category listings

3. **Match warm schedule to cache TTL**
   ```
   Cache TTL: 10 minutes → Warm every 5 minutes
   Cache TTL: 30 minutes → Warm every 15 minutes
   ```

4. **Monitor lock waits**
   - High lock waits = need Celery warming

5. **Use stale-while-revalidate for user-facing APIs**
   - Better UX (always fast)
   - Graceful degradation

6. **Adjust probabilistic delta based on traffic**
   ```python
   # High traffic: more aggressive
   PROBABILISTIC_EXPIRATION_DELTA = 0.15  # 15%
   
   # Low traffic: less aggressive
   PROBABILISTIC_EXPIRATION_DELTA = 0.05  # 5%
   ```

### DON'T ❌

1. **Don't over-warm cache**
   - Warming every 1 minute for 30-min TTL is wasteful

2. **Don't use stale data for critical operations**
   - Payment processing
   - Inventory checks
   - User authentication

3. **Don't disable stampede prevention on high-traffic endpoints**
   ```python
   # ❌ Bad for popular endpoints
   prevent_stampede=False
   ```

4. **Don't set lock timeout too high**
   ```python
   # ❌ Too long
   LOCK_TIMEOUT = 300  # 5 minutes
   
   # ✅ Reasonable
   LOCK_TIMEOUT = 30  # 30 seconds
   ```

5. **Don't ignore Celery Beat failures**
   - Set up alerts for task failures
   - Monitor task success rate

---

## 🚀 Deployment Checklist

- [ ] Redis is running and accessible
- [ ] `prevent_stampede=True` on high-traffic views
- [ ] Celery worker is running
- [ ] Celery Beat is running (`docker-compose ps celery-beat`)
- [ ] Verify Beat schedule: `celery -A core.celery_config inspect scheduled`
- [ ] Warm cache after deployment: `python manage.py warm_cache --all`
- [ ] Monitor cache hit rate (aim for >90%)
- [ ] Monitor lock acquisitions in logs
- [ ] Set up alerts for cache stampede indicators
- [ ] Configure Celery Beat schedule for your traffic patterns

---

## 🆘 Troubleshooting

### Problem: Still seeing stampede

**Symptoms:**
- Multiple concurrent database queries
- Response time spikes periodically

**Solutions:**
```bash
# 1. Verify locks are working
docker-compose logs web | grep "Lock acquired"

# 2. Check Celery Beat is running
docker-compose ps celery-beat

# 3. Enable more aggressive warming
# Edit core/celery_config.py:
'warm-product-list': {
    'schedule': crontab(minute='*/2'),  # More frequent
}

# 4. Enable stale-while-revalidate
@cache_view_response('products', use_stale=True)
```

### Problem: High lock wait times

**Symptoms:**
- Many "waiting for lock" log entries
- Slow response times

**Solutions:**
```python
# 1. Increase lock timeout
LOCK_TIMEOUT = 60  # Instead of 30

# 2. Enable Celery Beat warming
# Reduces lock contention

# 3. Use stale-while-revalidate
use_stale=True  # Don't wait for locks
```

### Problem: Celery Beat not running tasks

**Check:**
```bash
# 1. Is Beat service running?
docker-compose ps celery-beat

# 2. Check Beat logs
docker-compose logs celery-beat

# 3. Is worker running?
docker-compose ps celery

# 4. Verify schedule
docker-compose exec celery-beat celery -A core.celery_config inspect scheduled
```

---

## 📚 Additional Resources

- [Cache Warming Documentation](./CACHING.md)
- [Core Cache Utils](./core/cache_utils.py)
- [Cache Warming Functions](./core/cache_warming.py)
- [Celery Configuration](./core/celery_config.py)

---

**Summary:** We've implemented a **4-layer defense** against cache stampede:
1. 🔒 **Redis Locks** - Prevent duplicate computation
2. 🎲 **Probabilistic Expiration** - Spread out regeneration
3. ♻️ **Stale-While-Revalidate** - Serve stale, refresh background
4. 🔥 **Celery Beat Warming** - Proactive cache refresh

**Recommendation:** Use **Redis Locks (always) + Celery Beat (critical endpoints) + Stale-While-Revalidate (user-facing)**

🎉 **With these methods, cache stampede is eliminated!**