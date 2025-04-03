from rest_framework import serializers
from orders.models import Order, OrderItem, DiscountCode
from products.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    """ Serializer for items in an order """
    product_name = serializers.ReadOnlyField(source='product.name')

    class Meta:
        model = OrderItem
        fields = ["id", "product", "product_name", "quantity", "price"]


class OrderSerializer(serializers.ModelSerializer):
    """ Serializer for orders, including order items """
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = ["id", "user", "status", "discount_code", "total_price", "items", "created_at"]
        read_only_fields = ["user", "total_price", "created_at"]

    def create(self, validated_data):
        """ Assign the order to the current user """
        request = self.context.get("request")
        user = request.user if request else None
        validated_data["user"] = user
        return super().create(validated_data)


class DiscountCodeSerializer(serializers.ModelSerializer):
    """ Serializer for discount codes """
    class Meta:
        model = DiscountCode
        fields = ["id", "code", "discount_percent"]