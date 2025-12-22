"""
Cache Warming Utilities
Proactively populate cache before expiration to prevent cache stampede.

Features:
- Celery tasks for background cache warming
- Scheduled cache refresh with Celery Beat
- Critical endpoint prioritization
- Monitoring and metrics
"""

import logging
from typing import List, Optional

from django.conf import settings
from django.core.cache import cache
from django.db.models import Avg, Count

logger = logging.getLogger(__name__)


def warm_product_list_cache():
    """
    Warm cache for product list with common filter combinations.

    Returns:
        int: Number of cache entries created
    """
    from apps.products.api.serializers import ProductSerializer
    from apps.products.models import Product

    warmed_count = 0

    try:
        # Base product list (no filters)
        products = Product.objects.select_related("brand", "category").all()[:20]
        serializer = ProductSerializer(products, many=True)
        cache.set(
            "onlineshop:product_list",
            serializer.data,
            settings.CACHE_TTL.get("PRODUCT_LIST", 600),
        )
        warmed_count += 1
        logger.info("Warmed cache: product_list (no filters)")

        # Popular sort orders
        for sort_by in ["name", "price", "-price", "rating"]:
            cache_key = f"onlineshop:product_list:sort={sort_by}"
            if sort_by == "rating":
                products = (
                    Product.objects.select_related("brand", "category")
                    .annotate(avg_rating=Avg("ratings__value"))
                    .order_by("-avg_rating", "id")[:20]
                )
            elif sort_by == "name":
                products = Product.objects.select_related("brand", "category").order_by(
                    "name"
                )[:20]
            elif sort_by == "price":
                products = Product.objects.select_related("brand", "category").order_by(
                    "price"
                )[:20]
            else:  # -price
                products = Product.objects.select_related("brand", "category").order_by(
                    "-price"
                )[:20]

            serializer = ProductSerializer(products, many=True)
            cache.set(
                cache_key, serializer.data, settings.CACHE_TTL.get("PRODUCT_LIST", 600)
            )
            warmed_count += 1
            logger.info(f"Warmed cache: product_list (sort={sort_by})")

    except Exception as e:
        logger.error(f"Error warming product list cache: {str(e)}")

    return warmed_count


def warm_top_products_cache():
    """
    Warm cache for top-rated and discounted products.

    Returns:
        int: Number of cache entries created
    """
    from apps.products.api.serializers import ProductSerializer
    from apps.products.models import Product

    warmed_count = 0

    try:
        # Top rated products
        products = (
            Product.objects.select_related("brand", "category")
            .annotate(rating_count=Count("ratings"), avg_rating=Avg("ratings__value"))
            .filter(rating_count__gt=0)
            .order_by("-avg_rating", "id")[:20]
        )

        serializer = ProductSerializer(products, many=True)
        cache.set(
            "onlineshop:top_rated",
            serializer.data,
            settings.CACHE_TTL.get("TOP_RATED", 900),
        )
        warmed_count += 1
        logger.info("Warmed cache: top_rated")

        # Discounted products
        products = (
            Product.objects.select_related("brand", "category")
            .exclude(discount_percent=0)
            .order_by("-discount_percent", "id")[:20]
        )

        serializer = ProductSerializer(products, many=True)
        cache.set(
            "onlineshop:discounted",
            serializer.data,
            settings.CACHE_TTL.get("DISCOUNTED", 600),
        )
        warmed_count += 1
        logger.info("Warmed cache: discounted")

    except Exception as e:
        logger.error(f"Error warming top products cache: {str(e)}")

    return warmed_count


def warm_category_cache():
    """
    Warm cache for category list and popular category products.

    Returns:
        int: Number of cache entries created
    """
    from apps.products.api.serializers import CategorySerializer, ProductSerializer
    from apps.products.models import Category, Product

    warmed_count = 0

    try:
        # Category list
        roots = Category.objects.filter(parent=None)
        serializer = CategorySerializer(roots, many=True)
        cache.set(
            "onlineshop:category_list",
            serializer.data,
            settings.CACHE_TTL.get("CATEGORY_LIST", 1800),
        )
        warmed_count += 1
        logger.info("Warmed cache: category_list")

        # Top 5 categories by product count
        top_categories = Category.objects.annotate(
            product_count=Count("products")
        ).order_by("-product_count")[:5]

        for category in top_categories:
            products = (
                Product.objects.select_related("brand", "category")
                .filter(category=category)
                .order_by("id")[:20]
            )

            serializer = ProductSerializer(products, many=True)
            cache_key = f"onlineshop:category_products:pk={category.id}"
            cache.set(
                cache_key,
                serializer.data,
                settings.CACHE_TTL.get("CATEGORY_PRODUCTS", 600),
            )
            warmed_count += 1
            logger.info(f"Warmed cache: category_products (category={category.id})")

    except Exception as e:
        logger.error(f"Error warming category cache: {str(e)}")

    return warmed_count


def warm_brand_cache():
    """
    Warm cache for brand list and popular brand products.

    Returns:
        int: Number of cache entries created
    """
    from apps.products.api.schemas import BrandSerializer as BrandSchemaSerializer
    from apps.products.api.serializers import ProductSerializer
    from apps.products.models import Brand, Product

    warmed_count = 0

    try:
        # Brand list
        brands = Brand.objects.all()
        serializer = BrandSchemaSerializer(brands, many=True)
        cache.set(
            "onlineshop:brand_list",
            serializer.data,
            settings.CACHE_TTL.get("BRAND_LIST", 1800),
        )
        warmed_count += 1
        logger.info("Warmed cache: brand_list")

        # Top 5 brands by product count
        top_brands = Brand.objects.annotate(product_count=Count("products")).order_by(
            "-product_count"
        )[:5]

        for brand in top_brands:
            products = (
                Product.objects.select_related("brand", "category")
                .filter(brand=brand)
                .order_by("id")[:20]
            )

            serializer = ProductSerializer(products, many=True)
            cache_key = f"onlineshop:brand_products:pk={brand.id}"
            cache.set(
                cache_key,
                serializer.data,
                settings.CACHE_TTL.get("BRAND_PRODUCTS", 600),
            )
            warmed_count += 1
            logger.info(f"Warmed cache: brand_products (brand={brand.id})")

    except Exception as e:
        logger.error(f"Error warming brand cache: {str(e)}")

    return warmed_count


def warm_popular_products_cache(product_ids: Optional[List[int]] = None):
    """
    Warm cache for individual product details.

    Args:
        product_ids: Optional list of product IDs to warm. If None, warms top 20.

    Returns:
        int: Number of cache entries created
    """
    from apps.products.api.serializers import ProductSerializer
    from apps.products.models import Product

    warmed_count = 0

    try:
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
        else:
            # Get top 20 products by rating
            products = (
                Product.objects.annotate(
                    rating_count=Count("ratings"), avg_rating=Avg("ratings__value")
                )
                .filter(rating_count__gt=0)
                .order_by("-avg_rating")[:20]
            )

        for product in products:
            serializer = ProductSerializer(product)
            cache_key = f"onlineshop:product_detail:pk={product.id}"
            cache.set(
                cache_key,
                serializer.data,
                settings.CACHE_TTL.get("PRODUCT_DETAIL", 900),
            )
            warmed_count += 1
            logger.debug(f"Warmed cache: product_detail (product={product.id})")

        logger.info(f"Warmed cache for {warmed_count} product details")

    except Exception as e:
        logger.error(f"Error warming product details cache: {str(e)}")

    return warmed_count


def warm_all_critical_caches():
    """
    Warm all critical cache endpoints.

    This should be called:
    - After deployment
    - On a schedule (via Celery Beat)
    - After bulk data updates

    Returns:
        dict: Summary of warmed cache entries by type
    """
    logger.info("Starting cache warming for all critical endpoints...")

    summary = {
        "product_list": 0,
        "top_products": 0,
        "categories": 0,
        "brands": 0,
        "product_details": 0,
        "total": 0,
    }

    try:
        summary["product_list"] = warm_product_list_cache()
        summary["top_products"] = warm_top_products_cache()
        summary["categories"] = warm_category_cache()
        summary["brands"] = warm_brand_cache()
        summary["product_details"] = warm_popular_products_cache()

        summary["total"] = sum(summary.values())

        logger.info(
            f"Cache warming completed: {summary['total']} entries "
            f"(products: {summary['product_list']}, "
            f"top: {summary['top_products']}, "
            f"categories: {summary['categories']}, "
            f"brands: {summary['brands']}, "
            f"details: {summary['product_details']})"
        )

    except Exception as e:
        logger.error(f"Error during cache warming: {str(e)}")

    return summary


# Celery tasks for background cache warming
try:
    from celery import shared_task

    @shared_task(name="cache.warm_product_list")
    def warm_product_list_task():
        """Celery task to warm product list cache."""
        return warm_product_list_cache()

    @shared_task(name="cache.warm_top_products")
    def warm_top_products_task():
        """Celery task to warm top products cache."""
        return warm_top_products_cache()

    @shared_task(name="cache.warm_categories")
    def warm_category_task():
        """Celery task to warm category cache."""
        return warm_category_cache()

    @shared_task(name="cache.warm_brands")
    def warm_brand_task():
        """Celery task to warm brand cache."""
        return warm_brand_cache()

    @shared_task(name="cache.warm_popular_products")
    def warm_popular_products_task(product_ids=None):
        """Celery task to warm popular product details cache."""
        return warm_popular_products_cache(product_ids)

    @shared_task(name="cache.warm_all_critical")
    def warm_all_critical_caches_task():
        """
        Celery task to warm all critical caches.

        Schedule this task with Celery Beat to run periodically.
        """
        return warm_all_critical_caches()

except ImportError:
    logger.warning("Celery not available, cache warming tasks not registered")
