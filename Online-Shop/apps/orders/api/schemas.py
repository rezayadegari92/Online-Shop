
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    product_name = serializers.CharField(read_only=True)
    quantity = serializers.IntegerField(read_only=True)
    price_at_purchase = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_item_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)
    shipping_address = serializers.SerializerMethodField(read_only=True)
    payment_status = serializers.CharField(read_only=True)
    discount_code = serializers.CharField(allow_null=True, read_only=True)

    def get_shipping_address(self, obj):
        return f"{obj.shipping_street}, {obj.shipping_city}, {obj.shipping_state}, {obj.shipping_postal_code}, {obj.shipping_country}"
