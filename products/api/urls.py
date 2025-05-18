from django.urls import path
from .views import (
    ProductListView, ProductDetailView,
    CategoryListView, CategoryProductsView,
    TopRatedProductsView,
    BrandListView, BrandProductsView,DiscountedProductList,DiscountedProductDetailView
)

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/products/', CategoryProductsView.as_view(), name='category-products'),
    path('products/top-rated/', TopRatedProductsView.as_view(), name='top-rated-products'),
    path('brands/', BrandListView.as_view(), name='brand-list'),
    path('brands/<int:pk>/products/', BrandProductsView.as_view(), name='brand-products'),
    path('discounted-products/', DiscountedProductList.as_view(), name='discounted-products'),
    path('discounted-products/<int:pk>/', DiscountedProductDetailView.as_view(), name='discounted-product-detail'),


]
