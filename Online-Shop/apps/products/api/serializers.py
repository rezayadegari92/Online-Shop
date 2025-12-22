from decimal import ROUND_HALF_UP, Decimal

from django.db.models import Min, Max
from rest_framework import serializers

from apps.products.models import Brand, Category, Comment, Product, ProductImage, Rating


class Brandserializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "website"]


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image_url",
        )

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            # Use relative URL to work with nginx proxy
            return obj.image.url
        return obj.image.url


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "author", "content", "created_at", "product")
        read_only_fields = ("id", "created_at", "author", "product")


class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField(read_only=True)
    # avg_rating = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField(read_only=True)
    average_rating = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    ratings = serializers.SerializerMethodField(read_only=True)
    brand = Brandserializer(read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    price_range = serializers.SerializerMethodField(read_only=True)  # ✅ اضافه شده
    banner_image = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "price",
            "discount_percent",
            "discounted_price",
            "brand",
            "category",
            "details",
            "quantity",
            "final_price",
            "avg_rating",
            "average_rating",
            "images",
            "comments",
            "ratings",
            "price_range",
            "banner_image",
        )
        read_only_fields = (
            "id",
            "name",
            "price",
            "discount_percent",
            "discounted_price",
            "brand",
            "category",
            "details",
            "final_price",
            "avg_rating",
            "average_rating",
            "quantity",
            "images",
            "comments",
            "ratings",
            "price_range",
        )

    def get_avg_rating(self, obj):
        value = (
            obj.avg_rating
            if hasattr(obj, "avg_rating") and obj.avg_rating is not None
            else obj.average_rating()
        )
        if value is not None:
            return Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
        return None

    def get_average_rating(self, obj):
        return obj.average_rating()

    def get_ratings(self, obj):
        # Use prefetched ratings if available to avoid N+1 queries
        ratings = getattr(obj, '_prefetched_objects_cache', {}).get('ratings', None)
        if ratings is None:
            ratings = obj.ratings.select_related('user').all()
        return ProductRatingSerializer(ratings, many=True, context=self.context).data

    def get_final_price(self, obj):
        return obj.final_price

    def get_price_range(self, obj):
        # Use aggregation instead of loading all prices into memory
        # Cache this at class level to avoid repeated queries
        if not hasattr(ProductSerializer, '_price_range_cache'):
            price_range = Product.objects.aggregate(
                min_price=Min("price"),
                max_price=Max("price")
            )
            ProductSerializer._price_range_cache = {
                "min": price_range.get("min_price", 0) or 0,
                "max": price_range.get("max_price", 0) or 0
            }
        return ProductSerializer._price_range_cache

    def get_banner_image(self, obj):
        request = self.context.get("request")
        if obj.banner_image and hasattr(obj.banner_image, "url"):
            if request is not None:
                # Use relative URL to work with proxy/nginx
                return obj.banner_image.url
            return obj.banner_image.url
        return None


class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ("id", "user", "product", "value", "created_at")
        read_only_fields = ("user", "user", "product", "created_at")


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ("id", "name", "image", "subcategories")

    def get_subcategories(self, obj):
        # Use prefetched subcategories if available to avoid N+1 queries
        subcategories = getattr(obj, '_prefetched_objects_cache', {}).get('subcategories', None)
        if subcategories is None:
            subcategories = obj.subcategories.all()
        return CategorySerializer(subcategories, many=True, context=self.context).data

    def get_image(self, obj):
        request = self.context.get("request")
        if obj.image and hasattr(obj.image, "url"):
            if request is not None:
                # Use relative URL to work with proxy/nginx
                return obj.image.url
            return obj.image.url
        return None
