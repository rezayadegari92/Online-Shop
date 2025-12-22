from apps.products.api.serializers import ProductSerializer
from rest_framework import serializers
from apps.wishlists.models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for Wishlist model with product details."""

    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Wishlist
        fields = ["id", "product", "product_id", "created_at"]
        read_only_fields = ["id", "created_at"]

    def create(self, validated_data):
        """Create wishlist item with user from context."""
        user = self.context["request"].user
        product_id = validated_data.pop("product_id")

        wishlist, created = Wishlist.objects.get_or_create(
            user=user, product_id=product_id
        )
        return wishlist


class WishlistToggleSerializer(serializers.Serializer):
    """Serializer for toggling wishlist items."""

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        """Validate that product exists."""
        from products.models import Product

        if not Product.objects.filter(id=value).exists():
            raise serializers.ValidationError("Product does not exist.")
        return value
