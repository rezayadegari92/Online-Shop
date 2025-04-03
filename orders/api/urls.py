from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, DiscountCodeViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'discount-codes', DiscountCodeViewSet, basename='discount-code')

urlpatterns = [
    path('', include(router.urls)),
]