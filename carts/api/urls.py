from django.urls import path
from .views import CartView, CartItemListCreateView, CartItemUpdateDeleteView, ApplyDiscountView, CheckoutView

urlpatterns = [
    path('', CartView.as_view(), name='cart-detail'),
    path('items/', CartItemListCreateView.as_view(), name='cart-item-list-create'),
    path('items/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart-item-update-delete'),
    path('apply-discount/', ApplyDiscountView.as_view(), name='apply-discount'),
    path('checkout/', CheckoutView.as_view(), name='cart-checkout'),
]
