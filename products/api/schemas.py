
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers

class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField(required=False)
    image = serializers.URLField(read_only=True)
    parent = serializers.IntegerField(source='parent.id', allow_null=True, read_only=True)
    children = serializers.SerializerMethodField(read_only=True)

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data


class BrandSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    slug = serializers.CharField(read_only=True)
    image = serializers.URLField(read_only=True)


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    slug = serializers.CharField(read_only=True)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = serializers.IntegerField()
    discounted_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    image = serializers.URLField(read_only=True)
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CommentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    author = serializers.CharField(source='author.username', read_only=True)
    product = serializers.IntegerField(source='product.id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ProductRatingSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    value = serializers.IntegerField(min_value=1, max_value=5)
    user = serializers.CharField(source='user.username', read_only=True)
    product = serializers.IntegerField(source='product.id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class ProductListQueryParameters(serializers.Serializer):
    search = serializers.CharField(required=False, help_text="Search query for products (name, brand, category)")
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")


class ProductDetailPostRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['comment', 'rate'], help_text="Action to perform: 'comment' or 'rate'")
    content = serializers.CharField(required=False, help_text="Content of the comment (if action is 'comment')")
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5, help_text="Rating value (if action is 'rate')")


class CategoryProductsQueryParameters(serializers.Serializer):
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")


class BrandProductsQueryParameters(serializers.Serializer):
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")
