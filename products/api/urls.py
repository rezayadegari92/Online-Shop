from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CommentViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('api/', include(router.urls)),
]