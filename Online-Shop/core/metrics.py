"""
Custom Prometheus metrics for Online Shop application.
This module defines business-specific metrics that are not covered by django-prometheus.
"""
from prometheus_client import Counter, Histogram, Gauge

# Business Metrics - Orders
orders_created_total = Counter(
    'onlineshop_orders_created_total',
    'Total number of orders created',
    ['status']  # status: pending, completed, cancelled
)

order_value_total = Counter(
    'onlineshop_order_value_total',
    'Total value of all orders',
    ['status']
)

# Business Metrics - Products
product_views_total = Counter(
    'onlineshop_product_views_total',
    'Total number of product views',
    ['product_id', 'category']
)

product_searches_total = Counter(
    'onlineshop_product_searches_total',
    'Total number of product searches',
    ['query']
)

# Business Metrics - Cart
cart_additions_total = Counter(
    'onlineshop_cart_additions_total',
    'Total number of items added to cart',
    ['product_id']
)

cart_removals_total = Counter(
    'onlineshop_cart_removals_total',
    'Total number of items removed from cart',
    ['product_id']
)

cart_checkouts_total = Counter(
    'onlineshop_cart_checkouts_total',
    'Total number of cart checkouts initiated'
)

# Business Metrics - Users
user_registrations_total = Counter(
    'onlineshop_user_registrations_total',
    'Total number of user registrations'
)

user_logins_total = Counter(
    'onlineshop_user_logins_total',
    'Total number of user logins',
    ['method']  # method: jwt, session, etc.
)

active_users = Gauge(
    'onlineshop_active_users',
    'Number of currently active users'
)

# Business Metrics - Wishlist
wishlist_additions_total = Counter(
    'onlineshop_wishlist_additions_total',
    'Total number of items added to wishlist',
    ['product_id']
)

wishlist_removals_total = Counter(
    'onlineshop_wishlist_removals_total',
    'Total number of items removed from wishlist',
    ['product_id']
)

# API Performance Metrics
api_request_duration = Histogram(
    'onlineshop_api_request_duration_seconds',
    'API request duration in seconds',
    ['endpoint', 'method'],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0]
)

# Cache Metrics
cache_hits_total = Counter(
    'onlineshop_cache_hits_total',
    'Total number of cache hits',
    ['cache_key']
)

cache_misses_total = Counter(
    'onlineshop_cache_misses_total',
    'Total number of cache misses',
    ['cache_key']
)

# Database Query Metrics
db_query_duration = Histogram(
    'onlineshop_db_query_duration_seconds',
    'Database query duration in seconds',
    ['model', 'operation'],  # operation: select, insert, update, delete
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0]
)

