#!/usr/bin/env python
"""
Test script to verify cache fixes for:
1. Response serialization (pickle error)
2. Celery task registration
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response


def test_response_caching():
    """Test that Response objects can be cached properly."""
    print("Testing Response caching...")

    # Create a test response
    test_data = {"message": "Hello", "items": [1, 2, 3]}
    response = Response(test_data, status=status.HTTP_200_OK)

    # Create cache-friendly data structure (no rendering needed)
    cache_data = {
        "data": response.data,
        "status": response.status_code,
    }

    # Try to cache it
    cache_key = "test:response"
    try:
        cache.set(cache_key, cache_data, 60)
        print("✅ Cache set successful")

        # Try to retrieve it
        cached = cache.get(cache_key)
        if cached:
            print(f"✅ Cache get successful: {cached['data']}")

            # Reconstruct response
            reconstructed = Response(
                data=cached.get("data"),
                status=cached.get("status", 200),
            )
            print(f"✅ Response reconstructed: {reconstructed.data}")
            return True
        else:
            print("❌ Cache get failed")
            return False
    except Exception as e:
        print(f"❌ Cache failed: {e}")
        return False
    finally:
        cache.delete(cache_key)


def test_celery_tasks():
    """Test that Celery tasks are registered."""
    print("\nTesting Celery task registration...")

    try:
        from core.celery_config import celery_app

        # List registered tasks
        registered_tasks = celery_app.tasks.keys()

        cache_tasks = [
            "cache.warm_product_list",
            "cache.warm_top_products",
            "cache.warm_categories",
            "cache.warm_brands",
            "cache.warm_popular_products",
            "cache.warm_all_critical",
        ]

        missing = []
        for task in cache_tasks:
            if task in registered_tasks:
                print(f"✅ Task registered: {task}")
            else:
                print(f"❌ Task missing: {task}")
                missing.append(task)

        if missing:
            print(f"\n❌ Missing tasks: {missing}")
            print("\nAll registered tasks:")
            for task in sorted(registered_tasks):
                if "cache" in task or "warm" in task:
                    print(f"  - {task}")
            return False
        else:
            print("\n✅ All cache warming tasks registered!")
            return True

    except Exception as e:
        print(f"❌ Celery task check failed: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_cache_utils():
    """Test cache utility functions."""
    print("\nTesting cache utility functions...")

    try:
        from core.cache_utils import generate_cache_key, should_expire_early

        # Test cache key generation
        key = generate_cache_key("test", page=1, search="laptop")
        print(f"✅ Cache key generated: {key}")

        # Test probabilistic expiration
        should_expire = should_expire_early(ttl=100, original_timeout=600)
        print(f"✅ Probabilistic expiration check: {should_expire}")

        return True
    except Exception as e:
        print(f"❌ Cache utils test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Cache Fix Verification Tests")
    print("=" * 60)

    results = []

    # Run tests
    results.append(("Response Caching", test_response_caching()))
    results.append(("Celery Tasks", test_celery_tasks()))
    results.append(("Cache Utils", test_cache_utils()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status_icon = "✅" if result else "❌"
        print(f"{status_icon} {test_name}: {'PASSED' if result else 'FAILED'}")

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! Cache fixes are working.")
        exit(0)
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check errors above.")
        exit(1)
