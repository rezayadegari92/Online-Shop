# orders/api/v1/serializers.py

from rest_framework import serializers
from orders.models import Order, OrderItem
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_item_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_name', 'quantity', 'price_at_purchase', 'total_item_price']

    def get_total_item_price(self, obj):
        return obj.get_total_price()

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    discount_code = serializers.StringRelatedField()
    status = serializers.CharField(source='get_status_display', read_only=True)
    payment_status = serializers.CharField(source='get_payment_status_display', read_only=True)
    shipping_address = serializers.SerializerMethodField()
    updated_at = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'items', 'total_price', 'created_at', 'updated_at',
            'status', 'shipping_address', 'payment_status', 'discount_code'
        ]

    def get_shipping_address(self, obj):
        parts = [obj.shipping_street, obj.shipping_city, obj.shipping_state, obj.shipping_postal_code]
        return ', '.join(filter(None, parts))
