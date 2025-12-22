"""
Swagger/OpenAPI schema definitions for products API endpoints.
All API documentation decorators are defined here.
"""
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import serializers


# Request/Response Serializers for Swagger
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
    search = serializers.CharField(required=False, help_text="Search query for products")
    category = serializers.IntegerField(required=False, help_text="Filter by category ID")
    brand = serializers.IntegerField(required=False, help_text="Filter by brand ID")
    sort = serializers.ChoiceField(
        choices=['id', 'name', 'price', '-price', 'rating'],
        required=False,
        help_text="Sort products by: id, name, price, -price (descending), rating"
    )
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page (max 100)")


class ProductDetailPostRequestSerializer(serializers.Serializer):
    action = serializers.ChoiceField(choices=['comment', 'rate'], help_text="Action: 'comment' or 'rate'")
    content = serializers.CharField(required=False, help_text="Comment content (if action is 'comment')")
    rating = serializers.IntegerField(required=False, min_value=1, max_value=5, help_text="Rating (if action is 'rate')")


class CategoryProductsQueryParameters(serializers.Serializer):
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")


class BrandProductsQueryParameters(serializers.Serializer):
    page = serializers.IntegerField(required=False, help_text="Page number for pagination")
    page_size = serializers.IntegerField(required=False, help_text="Number of items per page")


# Schema Decorators
def product_list_schema():
    """Schema decorator for Product List endpoint."""
    return extend_schema(
        parameters=[ProductListQueryParameters],
        responses={200: ProductSerializer(many=True)},
        summary="List Products",
        description="Retrieve a list of products with optional search and pagination.",
        tags=["Products"],
    )


def product_detail_get_schema():
    """Schema decorator for Product Detail GET endpoint."""
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the product to retrieve.",
            )
        ],
        responses={200: ProductSerializer, 404: {"description": "Not Found"}},
        summary="Retrieve Product Details",
        description="Retrieve a product by ID.",
        tags=["Products"],
    )


def product_detail_post_schema():
    """Schema decorator for Product Detail POST endpoint."""
    return extend_schema(
        request=ProductDetailPostRequestSerializer,
        responses={
            201: CommentSerializer,
            200: ProductRatingSerializer,
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
        },
        summary="Add Comment or Rating to Product",
        description="Add a comment or rating to a specific product.",
        tags=["Products"],
    )


def category_list_schema():
    """Schema decorator for Category List endpoint."""
    return extend_schema(
        responses={200: CategorySerializer(many=True)},
        summary="List Categories",
        description="Retrieve a list of product categories (only root categories with their children).",
        tags=["Categories"],
    )


def category_products_schema():
    """Schema decorator for Category Products endpoint."""
    return extend_schema(
        parameters=[CategoryProductsQueryParameters],
        responses={200: ProductSerializer(many=True)},
        summary="List Products by Category",
        description="Retrieve a list of products belonging to a specific category, with pagination.",
        tags=["Categories"],
    )


def top_rated_products_schema():
    """Schema decorator for Top Rated Products endpoint."""
    return extend_schema(
        parameters=[ProductListQueryParameters],
        responses={200: ProductSerializer(many=True)},
        summary="List Top Rated Products",
        description="Retrieve a list of top-rated products with pagination.",
        tags=["Products"],
    )


def brand_list_schema():
    """Schema decorator for Brand List endpoint."""
    return extend_schema(
        responses={200: BrandSerializer(many=True)},
        summary="List Brands",
        description="Retrieve a list of all product brands.",
        tags=["Brands"],
    )


def brand_products_schema():
    """Schema decorator for Brand Products endpoint."""
    return extend_schema(
        parameters=[BrandProductsQueryParameters],
        responses={200: ProductSerializer(many=True)},
        summary="List Products by Brand",
        description="Retrieve a list of products belonging to a specific brand, with pagination.",
        tags=["Brands"],
    )


def discounted_products_schema():
    """Schema decorator for Discounted Products endpoint."""
    return extend_schema(
        parameters=[ProductListQueryParameters],
        responses={200: ProductSerializer(many=True)},
        summary="List Discounted Products",
        description="Retrieve a list of all products with a discount applied, with pagination.",
        tags=["Products"],
    )


def discounted_product_detail_get_schema():
    """Schema decorator for Discounted Product Detail GET endpoint."""
    return extend_schema(
        parameters=[
            OpenApiParameter(
                name="pk",
                type=int,
                location=OpenApiParameter.PATH,
                description="ID of the discounted product to retrieve.",
            )
        ],
        responses={200: ProductSerializer, 404: {"description": "Not Found"}},
        summary="Retrieve Discounted Product Details",
        description="Retrieve the details of a specific discounted product.",
        tags=["Products"],
    )


def discounted_product_detail_post_schema():
    """Schema decorator for Discounted Product Detail POST endpoint."""
    return extend_schema(
        request=ProductDetailPostRequestSerializer,
        responses={
            201: CommentSerializer,
            200: ProductRatingSerializer,
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
        },
        summary="Add Comment or Rating to Discounted Product",
        description="Add a comment or rating to a specific discounted product.",
        tags=["Products"],
    )


def shuffled_banner_products_schema():
    """Schema decorator for Shuffled Banner Products endpoint."""
    return extend_schema(
        responses={200: ProductSerializer(many=True)},
        summary="Get Shuffled Products with Banner Images",
        description="Retrieve a shuffled list of products that have banner images. Perfect for homepage display.",
        tags=["Products"],
    )
