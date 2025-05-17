from django.urls import path
from .views import *
#these are for render html files
urlpatterns = [
    path("home/",home, name="home"),
    path("products/",products, name="products"),
    path("product_detail/",product_detail, name="product_detail"),
    path("categories/", categories, name="categories"),
    path("category_products/", category_products, name="category_products"),
    path("brands/", brands, name="brands"),
    path("brand_products/", brand_products, name="brand_products"),
    path("cart/", cart, name="cart"),
    path("top_rated/", top_rated, name="top_rated"),
]