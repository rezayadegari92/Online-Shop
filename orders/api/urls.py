# cart/api/v1/urls.py
from django.urls import path
from .views import CartItemListCreateView, CartItemUpdateDeleteView , CartRetrieveView, ApplyDiscountView, CheckoutView

urlpatterns = [
    path('items/', CartItemListCreateView.as_view(), name='cart-item-list-create'),
    path('items/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
    path('', CartRetrieveView.as_view(), name='cart-detail'),
    path('apply-discount/', ApplyDiscountView.as_view(), name='apply-discount'),
    path('checkout/', CheckoutView.as_view(), name='cart-checkout'),
]
