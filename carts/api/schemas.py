
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    product = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name', read_only=True)
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, source='product.discounted_price', read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)


class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(source='user.id', read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    discount_code = serializers.CharField(allow_null=True, read_only=True)


class ApplyDiscountRequestSerializer(serializers.Serializer):
    code = serializers.CharField(help_text="Discount code to apply")

class ApplyDiscountResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()


class CheckoutResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
    order_id = serializers.IntegerField(required=False)


class CartDetailResponseSerializer(serializers.Serializer):
    # For authenticated users, this will be the CartSerializer
    # For anonymous users, this will be a dictionary of product_id: quantity
    pass

class CartItemUpdateDeleteRequestSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(help_text="ID of the product to update/remove")
    quantity = serializers.IntegerField(required=False, min_value=0, help_text="New quantity for the product (0 to remove)")
