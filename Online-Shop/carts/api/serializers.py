# cart/api/serializers.py
from rest_framework import serializers
from carts.models import CartItem, Cart, DiscountCode
from products.models import Product
from decimal import Decimal

class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discounted_price', 'image_url']
    
    def get_image_url(self, obj):
        if obj.images.exists():
            first_image = obj.images.first()
            # Return relative URL to work with nginx proxy
            return first_image.image.url
        return None

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
    product_id = serializers.IntegerField(required=False)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        required=False,
        write_only=True
    )
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        # Accept either product_id or product
        product_id = attrs.get('product_id')
        product = attrs.get('product')
        
        if not product_id and not product:
            raise serializers.ValidationError("Either product_id or product is required")
        
        if product_id and not product:
            try:
                attrs['product'] = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError({"product_id": "Product does not exist"})
        
        return attrs

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
