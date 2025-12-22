"""
Django management command to clear Redis cache.

Usage:
    python manage.py clear_cache              # Clear all cache
    python manage.py clear_cache --products   # Clear only product cache
    python manage.py clear_cache --categories # Clear only category cache
    python manage.py clear_cache --brands     # Clear only brand cache
"""

from core.cache_utils import (
    clear_all_cache,
    invalidate_brand_cache,
    invalidate_category_cache,
    invalidate_product_cache,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clear Redis cache for the online shop"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products",
            action="store_true",
            help="Clear only product-related cache",
        )
        parser.add_argument(
            "--categories",
            action="store_true",
            help="Clear only category-related cache",
        )
        parser.add_argument(
            "--brands",
            action="store_true",
            help="Clear only brand-related cache",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Clear all cache (default if no options specified)",
        )

    def handle(self, *args, **options):
        """Execute the cache clearing command."""

        products = options.get("products")
        categories = options.get("categories")
        brands = options.get("brands")
        clear_all = options.get("all")

        # If no specific option is provided, clear all cache
        if not any([products, categories, brands, clear_all]):
            clear_all = True

        if clear_all:
            self.stdout.write("Clearing all cache...")
            if clear_all_cache():
                self.stdout.write(
                    self.style.SUCCESS("✓ Successfully cleared all cache")
                )
            else:
                self.stdout.write(self.style.ERROR("✗ Failed to clear cache"))
            return

        # Clear specific caches
        total_cleared = 0

        if products:
            self.stdout.write("Clearing product cache...")
            count = invalidate_product_cache()
            total_cleared += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Cleared {count} product cache keys")
            )

        if categories:
            self.stdout.write("Clearing category cache...")
            count = invalidate_category_cache()
            total_cleared += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Cleared {count} category cache keys")
            )

        if brands:
            self.stdout.write("Clearing brand cache...")
            count = invalidate_brand_cache()
            total_cleared += count
            self.stdout.write(self.style.SUCCESS(f"✓ Cleared {count} brand cache keys"))

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Total cache keys cleared: {total_cleared}")
        )
