# cart/api/serializers.py
from rest_framework import serializers
from orders.models import CartItem
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.discounted_price', max_digits=10, decimal_places=2, read_only=True)
    
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity']

class CartItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        fields = ['product', 'quantity']


from carts.models import Cart, DiscountCode
from decimal import Decimal

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    discount_percent = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'discount_code', 'discount_percent', 'total_price', 'final_price']

    def get_total_price(self, obj):
        return sum((item.get_total_price() for item in obj.items.all()), Decimal(0))

    def get_discount_percent(self, obj):
        if obj.discount_code:
            return obj.discount_code.discount_percent
        return 0

    def get_final_price(self, obj):
        total = self.get_total_price(obj)
        if obj.discount_code:
            discount_amount = (total * obj.discount_code.discount_percent) / 100
            return total - discount_amount
        return total


# cart/api/serializers.py 

class ApplyDiscountSerializer(serializers.Serializer):
    code = serializers.CharField()

    def validate_code(self, value):
        try:
            return DiscountCode.objects.get(code=value)
        except DiscountCode.DoesNotExist:
            raise serializers.ValidationError("discount ode is not valid.")
