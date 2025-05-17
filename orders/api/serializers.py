# orders/api/v1/serializers.py

from rest_framework import serializers
from orders.models import Order, OrderItem
from products.models import Product  # فرض می‌کنیم اینو لازم داریم

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price_at_purchase']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    discount_code = serializers.StringRelatedField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'created_at', 'status', 'status_display', 'discount_code', 'total_price', 'items']
