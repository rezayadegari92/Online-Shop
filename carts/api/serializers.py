# cart/api/serializers.py
from rest_framework import serializers
from carts.models import CartItem, Cart, DiscountCode
from products.models import Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discounted_price', 'image']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_image = serializers.ImageField(source='product.image', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'product_image', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.quantity * obj.product.discounted_price

class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value)
            return value
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")

    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1")
        return value

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()
    is_authenticated = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price', 'discount_percent', 'final_price', 'is_authenticated']

    def get_total_price(self, obj):
        return sum(item.quantity * item.product.discounted_price for item in obj.items.all())

    def get_final_price(self, obj):
        total = self.get_total_price(obj)
        if obj.discount_percent:
            discount = total * (obj.discount_percent / 100)
            return total - discount
        return total

    def get_is_authenticated(self, obj):
        return bool(obj.user)

class ApplyDiscountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        # Add your discount code validation logic here
        return value
