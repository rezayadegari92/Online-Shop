from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    # Template Views
    path('', views.home, name='home'),
    path('products/', views.products, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/<int:pk>/', views.category_products, name='category_detail'),
    path('brands/', views.brand_list, name='brand_list'),
    path('brands/<int:pk>/', views.brand_products, name='brand_detail'),
    path('top-rated/', views.top_rated, name='top_rated'),
    path('cart/', views.cart, name='cart'),
    path('discounts/', views.discounts, name='discounts'),

    # API Views
    path('api/products/', views.ProductListView.as_view(), name='products_api'),
    path('api/products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail_api'),
    path('api/categories/', views.CategoryListView.as_view(), name='categories_api'),
    path('api/categories/<int:pk>/products/', views.CategoryProductsView.as_view(), name='category_products_api'),
    path('api/brands/', views.BrandListView.as_view(), name='brands_api'),
    path('api/brands/<int:pk>/products/', views.BrandProductsView.as_view(), name='brand_products_api'),
    path('api/cart/', views.CartView.as_view(), name='cart_api'),
    path('api/top-rated/', views.TopRatedProductsView.as_view(), name='top_rated_api'),
    path('api/discounts/', views.DiscountedProductsView.as_view(), name='discounts_api'),
]