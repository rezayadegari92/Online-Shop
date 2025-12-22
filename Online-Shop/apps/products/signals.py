"""
Product cache invalidation signals.
Automatically invalidate Redis cache when products, categories, or brands are modified.
"""

import logging

from core.cache_utils import (
    invalidate_brand_cache,
    invalidate_category_cache,
    invalidate_product_cache,
)
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from apps.products.models import Brand, Category, Comment, Product, Rating

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Product)
def invalidate_cache_on_product_save(sender, instance, created, **kwargs):
    """
    Invalidate product cache when a product is created or updated.
    """
    try:
        invalidate_product_cache(product_id=instance.id)
        logger.info(
            f"Cache invalidated for product {instance.id} ({'created' if created else 'updated'})"
        )
    except Exception as e:
        logger.error(f"Error invalidating cache for product {instance.id}: {str(e)}")


@receiver(post_delete, sender=Product)
def invalidate_cache_on_product_delete(sender, instance, **kwargs):
    """
    Invalidate product cache when a product is deleted.
    """
    try:
        invalidate_product_cache(product_id=instance.id)
        logger.info(f"Cache invalidated for deleted product {instance.id}")
    except Exception as e:
        logger.error(
            f"Error invalidating cache for deleted product {instance.id}: {str(e)}"
        )


@receiver(post_save, sender=Category)
def invalidate_cache_on_category_save(sender, instance, created, **kwargs):
    """
    Invalidate category and product cache when a category is created or updated.
    """
    try:
        invalidate_category_cache(category_id=instance.id)
        # Also invalidate product cache since category changes affect product listings
        invalidate_product_cache()
        logger.info(
            f"Cache invalidated for category {instance.id} ({'created' if created else 'updated'})"
        )
    except Exception as e:
        logger.error(f"Error invalidating cache for category {instance.id}: {str(e)}")


@receiver(post_delete, sender=Category)
def invalidate_cache_on_category_delete(sender, instance, **kwargs):
    """
    Invalidate category cache when a category is deleted.
    """
    try:
        invalidate_category_cache(category_id=instance.id)
        invalidate_product_cache()
        logger.info(f"Cache invalidated for deleted category {instance.id}")
    except Exception as e:
        logger.error(
            f"Error invalidating cache for deleted category {instance.id}: {str(e)}"
        )


@receiver(post_save, sender=Brand)
def invalidate_cache_on_brand_save(sender, instance, created, **kwargs):
    """
    Invalidate brand and product cache when a brand is created or updated.
    """
    try:
        invalidate_brand_cache(brand_id=instance.id)
        # Also invalidate product cache since brand changes affect product listings
        invalidate_product_cache()
        logger.info(
            f"Cache invalidated for brand {instance.id} ({'created' if created else 'updated'})"
        )
    except Exception as e:
        logger.error(f"Error invalidating cache for brand {instance.id}: {str(e)}")


@receiver(post_delete, sender=Brand)
def invalidate_cache_on_brand_delete(sender, instance, **kwargs):
    """
    Invalidate brand cache when a brand is deleted.
    """
    try:
        invalidate_brand_cache(brand_id=instance.id)
        invalidate_product_cache()
        logger.info(f"Cache invalidated for deleted brand {instance.id}")
    except Exception as e:
        logger.error(
            f"Error invalidating cache for deleted brand {instance.id}: {str(e)}"
        )


@receiver(post_save, sender=Rating)
def invalidate_cache_on_rating_save(sender, instance, created, **kwargs):
    """
    Invalidate product cache when a rating is added or updated.
    Ratings affect product detail pages and top-rated product lists.
    """
    try:
        invalidate_product_cache(product_id=instance.product.id)
        logger.info(
            f"Cache invalidated for product {instance.product.id} due to rating {'creation' if created else 'update'}"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating cache for product rating {instance.id}: {str(e)}"
        )


@receiver(post_delete, sender=Rating)
def invalidate_cache_on_rating_delete(sender, instance, **kwargs):
    """
    Invalidate product cache when a rating is deleted.
    """
    try:
        invalidate_product_cache(product_id=instance.product.id)
        logger.info(
            f"Cache invalidated for product {instance.product.id} due to rating deletion"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating cache for deleted rating {instance.id}: {str(e)}"
        )


@receiver(post_save, sender=Comment)
def invalidate_cache_on_comment_save(sender, instance, created, **kwargs):
    """
    Invalidate product cache when a comment is added or updated.
    Comments affect product detail pages.
    """
    try:
        invalidate_product_cache(product_id=instance.product.id)
        logger.info(
            f"Cache invalidated for product {instance.product.id} due to comment {'creation' if created else 'update'}"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating cache for product comment {instance.id}: {str(e)}"
        )


@receiver(post_delete, sender=Comment)
def invalidate_cache_on_comment_delete(sender, instance, **kwargs):
    """
    Invalidate product cache when a comment is deleted.
    """
    try:
        invalidate_product_cache(product_id=instance.product.id)
        logger.info(
            f"Cache invalidated for product {instance.product.id} due to comment deletion"
        )
    except Exception as e:
        logger.error(
            f"Error invalidating cache for deleted comment {instance.id}: {str(e)}"
        )
