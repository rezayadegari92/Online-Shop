# cart/api/serializers.py
from decimal import Decimal

from products.models import Product
from rest_framework import serializers

from carts.models import Cart, CartItem, DiscountCode


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ["id", "name", "price", "discounted_price", "image_url"]

    def get_image_url(self, obj):
        # Use prefetched images if available
        images = getattr(obj, '_prefetched_objects_cache', {}).get('images', None)
        if images:
            first_image = images[0] if images else None
        else:
            first_image = obj.images.first()
        
        if first_image:
            return first_image.image.url
        return None


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    product_price = serializers.DecimalField(
        source="product.price", max_digits=10, decimal_places=2, read_only=True
    )
    product_image = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()
    
    def get_product_image(self, obj):
        # Get image from product's prefetched images or return None
        images = getattr(obj.product, '_prefetched_objects_cache', {}).get('images', None)
        if images:
            first_image = images[0] if images else None
        else:
            first_image = obj.product.images.first()
        
        if first_image:
            return first_image.image.url
        return None

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "product_price",
            "product_image",
            "quantity",
            "total_price",
        ]

    def get_total_price(self, obj):
        return obj.quantity * obj.product.discounted_price


class CartItemCreateSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=False)
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), required=False, write_only=True
    )
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        # Accept either product_id or product
        product_id = attrs.get("product_id")
        product = attrs.get("product")

        if not product_id and not product:
            raise serializers.ValidationError(
                "Either product_id or product is required"
            )

        if product_id and not product:
            try:
                attrs["product"] = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                raise serializers.ValidationError(
                    {"product_id": "Product does not exist"}
                )

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
        fields = [
            "id",
            "items",
            "total_price",
            "discount_percent",
            "final_price",
            "is_authenticated",
        ]

    def get_total_price(self, obj):
        # Use prefetched items to avoid N+1 queries
        items = obj.items.all() if hasattr(obj, '_prefetched_objects_cache') else obj.items.select_related('product').all()
        return sum(
            item.quantity * item.product.discounted_price for item in items
        )

    def get_final_price(self, obj):
        total = self.get_total_price(obj)
        if obj.discount_percent:
            discount = total * (Decimal(str(obj.discount_percent)) / Decimal("100"))
            return total - discount
        return total

    def get_is_authenticated(self, obj):
        return bool(obj.user)


class ApplyDiscountSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=50)

    def validate_code(self, value):
        # Strip whitespace and convert to uppercase for consistency
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError("Discount code cannot be empty")

        try:
            discount_code = DiscountCode.objects.get(code__iexact=value)
            return discount_code
        except DiscountCode.DoesNotExist:
            raise serializers.ValidationError(
                f"Invalid discount code: '{value}'. Please check the code and try again."
            )
