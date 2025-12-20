#!/usr/bin/env python
"""
Database diagnostic script to check connection and data.
Usage: docker-compose exec web python check_database.py
"""

import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.conf import settings
from django.db import connection
from products.models import Brand, Category, Product


def check_database_connection():
    """Check if database connection is working."""
    print("\n" + "=" * 60)
    print("DATABASE CONNECTION CHECK")
    print("=" * 60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ Database connected: {version}")

        # Check database settings
        db_settings = settings.DATABASES["default"]
        print(f"\nDatabase Configuration:")
        print(f"  Engine: {db_settings['ENGINE']}")
        print(f"  Name: {db_settings['NAME']}")
        print(f"  User: {db_settings['USER']}")
        print(f"  Host: {db_settings['HOST']}")
        print(f"  Port: {db_settings['PORT']}")

        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_tables():
    """Check if tables exist."""
    print("\n" + "=" * 60)
    print("TABLES CHECK")
    print("=" * 60)

    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)
            tables = cursor.fetchall()

            if tables:
                print(f"✅ Found {len(tables)} tables:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("❌ No tables found! Run migrations:")
                print("   docker-compose exec web python manage.py migrate")

        return bool(tables)
    except Exception as e:
        print(f"❌ Failed to check tables: {e}")
        return False


def check_data():
    """Check if data exists in the database."""
    print("\n" + "=" * 60)
    print("DATA CHECK")
    print("=" * 60)

    try:
        # Count products
        product_count = Product.objects.count()
        category_count = Category.objects.count()
        brand_count = Brand.objects.count()

        print(f"Products: {product_count}")
        print(f"Categories: {category_count}")
        print(f"Brands: {brand_count}")

        if product_count == 0:
            print("\n⚠️  Database is empty!")
            print("Create sample data:")
            print("  docker-compose exec web python manage.py create_sample_data")
            return False
        else:
            print(f"\n✅ Database has data!")

            # Show sample products
            print("\nSample Products:")
            for product in Product.objects.all()[:5]:
                print(
                    f"  - {product.name} (${product.price}) - {product.category.name}"
                )

            # Show discounted products
            discounted = Product.objects.filter(discount_percent__gt=0).count()
            print(f"\nDiscounted products: {discounted}")

            return True

    except Exception as e:
        print(f"❌ Failed to check data: {e}")
        import traceback

        traceback.print_exc()
        return False


def check_cache():
    """Check Redis cache connection."""
    print("\n" + "=" * 60)
    print("CACHE CHECK")
    print("=" * 60)

    try:
        from django.core.cache import cache

        # Test cache
        test_key = "test_connection"
        test_value = "hello"

        cache.set(test_key, test_value, 60)
        retrieved = cache.get(test_key)

        if retrieved == test_value:
            print("✅ Redis cache is working")

            # Check cache keys
            try:
                from django_redis import get_redis_connection

                redis_conn = get_redis_connection("default")
                keys = redis_conn.keys("onlineshop:*")
                print(f"   Cached items: {len(keys)}")

                if keys:
                    print("   Sample cache keys:")
                    for key in list(keys)[:5]:
                        print(f"     - {key.decode()}")
            except:
                pass

            cache.delete(test_key)
            return True
        else:
            print("❌ Cache set/get failed")
            return False

    except Exception as e:
        print(f"❌ Cache connection failed: {e}")
        return False


def check_environment():
    """Check environment variables."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT CHECK")
    print("=" * 60)

    env_vars = [
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_HOST",
        "DEBUG",
        "CELERY_BROKER_URL",
    ]

    for var in env_vars:
        value = os.getenv(var, "NOT SET")
        print(f"{var}: {value}")


def main():
    """Run all diagnostic checks."""
    print("=" * 60)
    print("ONLINE SHOP DATABASE DIAGNOSTIC")
    print("=" * 60)

    results = []

    # Run checks
    results.append(("Database Connection", check_database_connection()))
    results.append(("Tables", check_tables()))
    results.append(("Data", check_data()))
    results.append(("Cache", check_cache()))

    check_environment()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")

    print(f"\nTotal: {passed}/{total} checks passed")

    # Recommendations
    print("\n" + "=" * 60)
    print("RECOMMENDATIONS")
    print("=" * 60)

    if not results[1][1]:  # Tables check failed
        print("1. Run migrations:")
        print("   docker-compose exec web python manage.py migrate")

    if not results[2][1]:  # Data check failed
        print("2. Create sample data:")
        print("   docker-compose exec web python manage.py create_sample_data")

    if not results[3][1]:  # Cache check failed
        print("3. Check Redis:")
        print("   docker-compose exec redis redis-cli ping")

    print("\n4. Test API:")
    print("   curl http://localhost:8000/api/products/")

    print("\n5. Check admin panel:")
    print("   http://localhost:8000/admin/")
    print("   (Create superuser if needed: python manage.py createsuperuser)")

    print("\n" + "=" * 60)

    if passed == total:
        print("🎉 All checks passed! Your setup is working correctly.")
    else:
        print(f"⚠️  {total - passed} check(s) failed. Follow recommendations above.")

    print("=" * 60)


if __name__ == "__main__":
    main()
