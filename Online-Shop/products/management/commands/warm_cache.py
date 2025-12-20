"""
Django management command to manually warm cache.

Usage:
    python manage.py warm_cache              # Warm all critical caches
    python manage.py warm_cache --products   # Warm only product caches
    python manage.py warm_cache --categories # Warm only category caches
    python manage.py warm_cache --brands     # Warm only brand caches
    python manage.py warm_cache --top        # Warm only top-rated/discounted
"""

from core.cache_warming import (
    warm_all_critical_caches,
    warm_brand_cache,
    warm_category_cache,
    warm_popular_products_cache,
    warm_product_list_cache,
    warm_top_products_cache,
)
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Warm Redis cache for critical endpoints"

    def add_arguments(self, parser):
        parser.add_argument(
            "--products",
            action="store_true",
            help="Warm only product list cache",
        )
        parser.add_argument(
            "--categories",
            action="store_true",
            help="Warm only category cache",
        )
        parser.add_argument(
            "--brands",
            action="store_true",
            help="Warm only brand cache",
        )
        parser.add_argument(
            "--top",
            action="store_true",
            help="Warm only top-rated and discounted products",
        )
        parser.add_argument(
            "--details",
            action="store_true",
            help="Warm popular product details",
        )
        parser.add_argument(
            "--all",
            action="store_true",
            help="Warm all critical caches (default)",
        )
        parser.add_argument(
            "--product-ids",
            nargs="+",
            type=int,
            help="Specific product IDs to warm (for --details)",
        )

    def handle(self, *args, **options):
        """Execute the cache warming command."""

        products = options.get("products")
        categories = options.get("categories")
        brands = options.get("brands")
        top = options.get("top")
        details = options.get("details")
        warm_all = options.get("all")
        product_ids = options.get("product_ids")

        # If no specific option is provided, warm all caches
        if not any([products, categories, brands, top, details, warm_all]):
            warm_all = True

        if warm_all:
            self.stdout.write(self.style.WARNING("🔥 Warming all critical caches..."))
            summary = warm_all_critical_caches()

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n✓ Successfully warmed {summary['total']} cache entries:"
                )
            )
            self.stdout.write(f"  • Product lists: {summary['product_list']}")
            self.stdout.write(f"  • Top products: {summary['top_products']}")
            self.stdout.write(f"  • Categories: {summary['categories']}")
            self.stdout.write(f"  • Brands: {summary['brands']}")
            self.stdout.write(f"  • Product details: {summary['product_details']}")
            return

        # Warm specific caches
        total_warmed = 0

        if products:
            self.stdout.write("🔥 Warming product list cache...")
            count = warm_product_list_cache()
            total_warmed += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Warmed {count} product list cache entries")
            )

        if categories:
            self.stdout.write("🔥 Warming category cache...")
            count = warm_category_cache()
            total_warmed += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Warmed {count} category cache entries")
            )

        if brands:
            self.stdout.write("🔥 Warming brand cache...")
            count = warm_brand_cache()
            total_warmed += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Warmed {count} brand cache entries")
            )

        if top:
            self.stdout.write("🔥 Warming top products cache...")
            count = warm_top_products_cache()
            total_warmed += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Warmed {count} top product cache entries")
            )

        if details:
            self.stdout.write("🔥 Warming product details cache...")
            count = warm_popular_products_cache(product_ids)
            total_warmed += count
            self.stdout.write(
                self.style.SUCCESS(f"✓ Warmed {count} product detail cache entries")
            )

        self.stdout.write(
            self.style.SUCCESS(f"\n✓ Total cache entries warmed: {total_warmed}")
        )
