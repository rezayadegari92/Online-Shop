"""
Redis Cache Utility Functions
Provides reusable caching decorators and helper functions for the Online Shop API.

Features:
- Cache stampede prevention using Redis locks
- Probabilistic early expiration
- Stale-while-revalidate support
"""

import hashlib
import json
import logging
import random
import time
from functools import wraps

from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


# Cache stampede prevention settings
LOCK_TIMEOUT = 30  # seconds - maximum time a lock can be held
LOCK_WAIT_TIMEOUT = 10  # seconds - maximum time to wait for lock
PROBABILISTIC_EXPIRATION_DELTA = 0.1  # 10% of TTL for early expiration


def generate_cache_key(prefix, *args, **kwargs):
    """
    Generate a unique cache key based on prefix and arguments.

    Args:
        prefix: String prefix for the cache key
        *args: Positional arguments to include in key
        **kwargs: Keyword arguments to include in key

    Returns:
        Unique cache key string
    """
    key_parts = [prefix]

    # Add args to key
    for arg in args:
        if arg is not None:
            key_parts.append(str(arg))

    # Add sorted kwargs to key
    for k, v in sorted(kwargs.items()):
        if v is not None:
            key_parts.append(f"{k}={v}")

    # Create hash for long keys
    key_string = ":".join(key_parts)
    if len(key_string) > 200:
        key_hash = hashlib.md5(key_string.encode()).hexdigest()
        return f"{prefix}:{key_hash}"

    return key_string


def cache_view_response(
    cache_key_prefix,
    timeout=None,
    query_params=None,
    prevent_stampede=True,
    use_stale=False,
):
    """
    Decorator to cache API view responses with stampede prevention.

    Args:
        cache_key_prefix: Prefix for the cache key
        timeout: Cache timeout in seconds (uses settings default if None)
        query_params: List of query parameters to include in cache key
        prevent_stampede: Enable cache stampede prevention (default: True)
        use_stale: Serve stale cache while revalidating (default: False)

    Features:
        - Cache stampede prevention using Redis locks
        - Probabilistic early expiration
        - Optional stale-while-revalidate

    Usage:
        @cache_view_response(
            'product_list',
            timeout=600,
            query_params=['search', 'category', 'brand'],
            prevent_stampede=True
        )
        def get(self, request):
            ...
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(view_instance, request, *args, **kwargs):
            # Don't cache authenticated user-specific data by default
            # (unless explicitly needed)
            if (
                request.user.is_authenticated
                and "user_specific" not in cache_key_prefix
            ):
                return view_func(view_instance, request, *args, **kwargs)

            # Build cache key from parameters
            key_kwargs = {}

            # Add URL path parameters
            for key, value in kwargs.items():
                key_kwargs[key] = value

            # Add query parameters if specified
            if query_params:
                for param in query_params:
                    value = request.GET.get(param)
                    if value:
                        key_kwargs[param] = value

            # Generate unique cache key
            cache_key = generate_cache_key(cache_key_prefix, **key_kwargs)
            cache_timeout = timeout or settings.CACHES["default"]["TIMEOUT"]

            # Try to get from cache with stampede prevention
            if prevent_stampede:
                cached_data = get_with_stampede_prevention(
                    cache_key=cache_key,
                    compute_func=lambda: view_func(
                        view_instance, request, *args, **kwargs
                    ),
                    timeout=cache_timeout,
                    use_stale=use_stale,
                )
                # Reconstruct Response from cached data
                if isinstance(cached_data, dict):
                    from rest_framework.response import Response

                    return Response(
                        data=cached_data.get("data"),
                        status=cached_data.get("status", 200),
                    )
                return cached_data
            else:
                # Standard cache without stampede prevention
                cached_data = cache.get(cache_key)
                if cached_data is not None:
                    logger.debug(f"Cache HIT: {cache_key}")
                    # Reconstruct Response from cached data
                    from rest_framework.response import Response

                    return Response(
                        data=cached_data.get("data"),
                        status=cached_data.get("status", 200),
                    )

                logger.debug(f"Cache MISS: {cache_key}")

                # Call the actual view
                response = view_func(view_instance, request, *args, **kwargs)

                # Cache successful responses only
                if response.status_code == 200:
                    # Store data dict instead of Response object
                    cache_data = {
                        "data": response.data,
                        "status": response.status_code,
                    }
                    cache.set(cache_key, cache_data, cache_timeout)
                    logger.debug(
                        f"Cached response: {cache_key} (timeout: {cache_timeout}s)"
                    )

                return response

        return wrapped_view

    return decorator


def get_with_stampede_prevention(cache_key, compute_func, timeout, use_stale=False):
    """
    Get value from cache with cache stampede prevention.

    Uses Redis locks to ensure only one process computes the value
    when cache expires, while others wait for the result.

    Args:
        cache_key: Cache key to retrieve
        compute_func: Function to compute value if cache miss
        timeout: Cache timeout in seconds
        use_stale: Serve stale cache while revalidating

    Returns:
        Cached or computed value
    """
    from django_redis import get_redis_connection

    # Check if we should probabilistically expire early
    # This helps spread out cache regeneration
    cached_data = cache.get(cache_key)

    if cached_data is not None:
        # Check for probabilistic early expiration
        ttl = cache.ttl(cache_key)
        if ttl and should_expire_early(ttl, timeout):
            logger.debug(f"Probabilistic early expiration: {cache_key}")
            # Continue to revalidate, but can serve stale if enabled
            if not use_stale:
                cached_data = None
        else:
            logger.debug(f"Cache HIT: {cache_key}")
            return cached_data

    # Cache miss or early expiration - need to compute
    lock_key = f"{cache_key}:lock"
    redis_conn = get_redis_connection("default")

    # Try to acquire lock
    lock_acquired = redis_conn.set(lock_key, "1", nx=True, ex=LOCK_TIMEOUT)

    if lock_acquired:
        # This process won the race - compute the value
        logger.debug(f"Lock acquired, computing: {cache_key}")
        try:
            response = compute_func()

            # Cache successful responses only
            if hasattr(response, "status_code") and response.status_code == 200:
                # Store data dict instead of Response object
                cache_data = {
                    "data": response.data,
                    "status": response.status_code,
                }
                cache.set(cache_key, cache_data, timeout)
                logger.debug(f"Cached response: {cache_key} (timeout: {timeout}s)")

            return response

        finally:
            # Always release the lock
            redis_conn.delete(lock_key)
    else:
        # Another process is computing - wait for it
        logger.debug(f"Lock held by another process, waiting: {cache_key}")

        # If stale data available and use_stale enabled, serve it
        if use_stale and cached_data is not None:
            logger.info(f"Serving stale cache while revalidating: {cache_key}")
            return cached_data

        # Wait for the other process to finish
        wait_start = time.time()
        while time.time() - wait_start < LOCK_WAIT_TIMEOUT:
            # Check if value is now in cache
            cached_response = cache.get(cache_key)
            if cached_response is not None:
                logger.debug(f"Cache populated by another process: {cache_key}")
                return cached_response

            # Wait a bit before checking again
            time.sleep(0.1)

        # Timeout waiting for lock - compute anyway to avoid request failure
        logger.warning(f"Timeout waiting for lock, computing anyway: {cache_key}")
        response = compute_func()

        if hasattr(response, "status_code") and response.status_code == 200:
            # Store data dict instead of Response object
            cache_data = {
                "data": response.data,
                "status": response.status_code,
            }
            cache.set(cache_key, cache_data, timeout)

        return response


def should_expire_early(ttl, original_timeout):
    """
    Determine if cache should expire early using probabilistic approach.

    This helps prevent cache stampede by randomly expiring cache entries
    slightly before their actual expiration time.

    Formula: probability = delta * log(time_since_creation) / ttl
    Where: time_since_creation = original_timeout - ttl

    Args:
        ttl: Current time-to-live in seconds
        original_timeout: Original cache timeout in seconds

    Returns:
        Boolean indicating if cache should expire early
    """
    if ttl <= 0 or ttl >= original_timeout:
        return False

    # Calculate time since creation
    time_since_creation = original_timeout - ttl

    # Don't expire if freshly created (less than 10% of lifetime)
    if time_since_creation < original_timeout * 0.1:
        return False

    # Probabilistic expiration: higher probability as cache ages
    # probability = delta * log(time_since_creation) / ttl
    import math

    try:
        probability = (
            PROBABILISTIC_EXPIRATION_DELTA * math.log(time_since_creation) / ttl
        )
        # Cap probability at 0.5 (50%)
        probability = min(probability, 0.5)

        should_expire = random.random() < probability

        if should_expire:
            logger.debug(
                f"Probabilistic early expiration triggered "
                f"(probability: {probability:.2%}, ttl: {ttl}s)"
            )

        return should_expire
    except (ValueError, ZeroDivisionError):
        return False


def invalidate_cache_pattern(pattern):
    """
    Invalidate all cache keys matching a pattern.

    Args:
        pattern: String pattern to match cache keys (e.g., 'product:*')

    Returns:
        Number of keys deleted
    """
    try:
        from django_redis import get_redis_connection

        redis_conn = get_redis_connection("default")

        # Get all keys matching pattern
        full_pattern = f"{settings.CACHES['default']['KEY_PREFIX']}:{pattern}"
        keys = redis_conn.keys(full_pattern)

        if keys:
            deleted_count = redis_conn.delete(*keys)
            logger.info(f"Invalidated {deleted_count} cache keys matching '{pattern}'")
            return deleted_count
        return 0
    except Exception as e:
        logger.error(f"Error invalidating cache pattern '{pattern}': {str(e)}")
        return 0


def invalidate_product_cache(product_id=None):
    """
    Invalidate product-related cache entries.

    Args:
        product_id: Specific product ID to invalidate (None for all products)
    """
    patterns = [
        "product_list:*",
        "top_rated:*",
        "discounted:*",
        "category_products:*",
        "brand_products:*",
    ]

    if product_id:
        patterns.append(f"product_detail:*pk={product_id}*")
    else:
        patterns.append("product_detail:*")

    total_deleted = 0
    for pattern in patterns:
        total_deleted += invalidate_cache_pattern(pattern)

    logger.info(
        f"Invalidated product cache (product_id={product_id}): {total_deleted} keys"
    )
    return total_deleted


def invalidate_category_cache(category_id=None):
    """
    Invalidate category-related cache entries.

    Args:
        category_id: Specific category ID to invalidate (None for all categories)
    """
    patterns = [
        "category_list:*",
        "product_list:*",
    ]

    if category_id:
        patterns.append(f"category_products:*pk={category_id}*")
    else:
        patterns.append("category_products:*")

    total_deleted = 0
    for pattern in patterns:
        total_deleted += invalidate_cache_pattern(pattern)

    logger.info(
        f"Invalidated category cache (category_id={category_id}): {total_deleted} keys"
    )
    return total_deleted


def invalidate_brand_cache(brand_id=None):
    """
    Invalidate brand-related cache entries.

    Args:
        brand_id: Specific brand ID to invalidate (None for all brands)
    """
    patterns = [
        "brand_list:*",
        "product_list:*",
    ]

    if brand_id:
        patterns.append(f"brand_products:*pk={brand_id}*")
    else:
        patterns.append("brand_products:*")

    total_deleted = 0
    for pattern in patterns:
        total_deleted += invalidate_cache_pattern(pattern)

    logger.info(f"Invalidated brand cache (brand_id={brand_id}): {total_deleted} keys")
    return total_deleted


def get_or_set_cache(key, callable_func, timeout=None):
    """
    Get value from cache or set it using the callable function.

    Args:
        key: Cache key
        callable_func: Function to call if cache miss
        timeout: Cache timeout in seconds

    Returns:
        Cached or newly computed value
    """
    cached_value = cache.get(key)

    if cached_value is not None:
        logger.debug(f"Cache HIT: {key}")
        return cached_value

    logger.debug(f"Cache MISS: {key}")
    value = callable_func()

    cache_timeout = timeout or settings.CACHES["default"]["TIMEOUT"]
    cache.set(key, value, cache_timeout)

    return value


def clear_all_cache():
    """
    Clear all cache entries (use with caution).

    Returns:
        Boolean indicating success
    """
    try:
        cache.clear()
        logger.warning("All cache cleared")
        return True
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return False
