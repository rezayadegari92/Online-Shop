"""
API views for products, categories, and brands.
Business logic is kept here, Swagger documentation is in schemas.py
"""
import random

from core.cache_utils import cache_view_response
from django.conf import settings
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Brand, Category, Product, Rating

from .schemas import (
    brand_list_schema,
    brand_products_schema,
    category_list_schema,
    category_products_schema,
    discounted_product_detail_get_schema,
    discounted_product_detail_post_schema,
    discounted_products_schema,
    product_detail_get_schema,
    product_detail_post_schema,
    product_list_schema,
    shuffled_banner_products_schema,
    top_rated_products_schema,
)
from .serializers import (
    CategorySerializer,
    CommentSerializer,
    ProductRatingSerializer,
    ProductSerializer,
)


def get_category_descendants(category):
    """Recursively get all descendant category IDs including the category itself."""
    category_ids = [category.id]
    for subcategory in category.subcategories.all():
        category_ids.extend(get_category_descendants(subcategory))
    return category_ids


class CustomPageNumberPagination(PageNumberPagination):
    """Custom pagination with configurable page size."""
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                page_size = int(request.query_params[self.page_size_query_param])
                if page_size > 0:
                    return min(page_size, self.max_page_size)
            except (KeyError, ValueError):
                pass
        return self.page_size


class ProductListView(APIView):
    """List products with filtering, searching, and pagination."""
    permission_classes = [permissions.AllowAny]

    @product_list_schema()
    @cache_view_response(
        "product_list",
        timeout=settings.CACHE_TTL.get("PRODUCT_LIST", 600),
        query_params=["search", "category", "brand", "sort", "page", "page_size"],
    )
    def get(self, request):
        search_query = request.GET.get("search", "")
        category_id = request.GET.get("category")
        brand_id = request.GET.get("brand")
        sort_by = request.GET.get("sort", "id")

        products = Product.objects.select_related(
            "brand", "category"
        ).prefetch_related("images").all()

        if search_query:
            products = products.filter(
                Q(name__icontains=search_query)
                | Q(brand__name__icontains=search_query)
                | Q(category__name__icontains=search_query)
                | Q(details__icontains=search_query)
            )

        if category_id:
            try:
                category = Category.objects.get(pk=category_id)
                category_ids = get_category_descendants(category)
                products = products.filter(category_id__in=category_ids)
            except (ValueError, Category.DoesNotExist):
                return Response(
                    {"detail": "Invalid category ID."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if brand_id:
            try:
                products = products.filter(brand_id=brand_id)
            except ValueError:
                return Response(
                    {"detail": "Invalid brand ID."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        if sort_by == "name":
            products = products.order_by("name")
        elif sort_by == "price":
            products = products.order_by("price")
        elif sort_by == "-price":
            products = products.order_by("-price")
        elif sort_by == "rating":
            products = products.annotate(avg_rating=Avg("ratings__value")).order_by(
                "-avg_rating", "id"
            )
        else:
            products = products.order_by("id")

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_products, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class ProductDetailView(APIView):
    """Retrieve product details, add comments or ratings."""
    permission_classes = [permissions.AllowAny]

    @product_detail_get_schema()
    @cache_view_response(
        "product_detail", timeout=settings.CACHE_TTL.get("PRODUCT_DETAIL", 900)
    )
    def get(self, request, pk):
        try:
            product = Product.objects.select_related(
                "brand", "category"
            ).prefetch_related(
                "images",
                "comments__author",
                "ratings__user"
            ).get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)

    @product_detail_post_schema()
    def post(self, request, pk):
        try:
            product = Product.objects.select_related("brand", "category").get(pk=pk)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        action = request.data.get("action")

        if action == "comment":
            data = {"content": request.data.get("content")}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == "rate":
            data = {"value": request.data.get("rating")}
            try:
                rating = product.ratings.get(user=request.user)
                serializer = ProductRatingSerializer(rating, data=data, partial=True)
            except Rating.DoesNotExist:
                serializer = ProductRatingSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Invalid action."},
            status=status.HTTP_400_BAD_REQUEST
        )


class CategoryListView(APIView):
    """List all root categories with their children."""
    permission_classes = [permissions.AllowAny]

    @category_list_schema()
    @cache_view_response(
        "category_list", timeout=settings.CACHE_TTL.get("CATEGORY_LIST", 1800)
    )
    def get(self, request):
        roots = Category.objects.filter(parent=None).prefetch_related(
            "subcategories",
            "subcategories__subcategories"
        )
        serializer = CategorySerializer(roots, many=True, context={"request": request})
        return Response(serializer.data)


class CategoryProductsView(APIView):
    """List products for a specific category including subcategories."""
    permission_classes = [permissions.AllowAny]

    @category_products_schema()
    @cache_view_response(
        "category_products",
        timeout=settings.CACHE_TTL.get("CATEGORY_PRODUCTS", 600),
        query_params=["page", "page_size"],
    )
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response(
                {"detail": "Category not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        category_ids = get_category_descendants(category)
        products = (
            Product.objects.select_related("brand", "category")
            .prefetch_related("images")
            .filter(category_id__in=category_ids)
            .order_by("id")
        )

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_products, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class TopRatedProductsView(APIView):
    """List top-rated products sorted by average rating."""
    permission_classes = [permissions.AllowAny]

    @top_rated_products_schema()
    @cache_view_response(
        "top_rated",
        timeout=settings.CACHE_TTL.get("TOP_RATED", 900),
        query_params=["page", "page_size"],
    )
    def get(self, request):
        products = (
            Product.objects.select_related("brand", "category")
            .prefetch_related("images")
            .annotate(rating_count=Count("ratings"), avg_rating=Avg("ratings__value"))
            .filter(rating_count__gt=0)
            .order_by("-avg_rating", "id")
        )

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_products, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class BrandListView(APIView):
    """List all product brands."""
    permission_classes = [permissions.AllowAny]

    @brand_list_schema()
    @cache_view_response(
        "brand_list", timeout=settings.CACHE_TTL.get("BRAND_LIST", 1800)
    )
    def get(self, request):
        from .schemas import BrandSerializer as BrandSchemaSerializer
        brands = Brand.objects.all()
        serializer = BrandSchemaSerializer(
            brands, many=True, context={"request": request}
        )
        return Response(serializer.data)


class BrandProductsView(APIView):
    """List products for a specific brand."""
    permission_classes = [permissions.AllowAny]

    @brand_products_schema()
    @cache_view_response(
        "brand_products",
        timeout=settings.CACHE_TTL.get("BRAND_PRODUCTS", 600),
        query_params=["page", "page_size"],
    )
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response(
                {"detail": "Brand not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        products = (
            brand.products.select_related("brand", "category")
            .prefetch_related("images")
            .all()
            .order_by("id")
        )
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_products, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class DiscountedProductList(APIView):
    """List all products with discounts applied."""
    permission_classes = [permissions.AllowAny]

    @discounted_products_schema()
    @cache_view_response(
        "discounted",
        timeout=settings.CACHE_TTL.get("DISCOUNTED", 600),
        query_params=["page", "page_size"],
    )
    def get(self, request):
        products = (
            Product.objects.select_related("brand", "category")
            .prefetch_related("images")
            .exclude(discount_percent=0)
            .order_by("-discount_percent", "id")
        )

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(
            paginated_products, many=True, context={"request": request}
        )
        return paginator.get_paginated_response(serializer.data)


class DiscountedProductDetailView(APIView):
    """Retrieve discounted product details, add comments or ratings."""
    permission_classes = [permissions.AllowAny]

    @discounted_product_detail_get_schema()
    def get(self, request, pk):
        product = get_object_or_404(
            Product.objects.select_related("brand", "category").prefetch_related(
                "images", "comments__author", "ratings__user"
            ),
            pk=pk,
            discount_percent__gt=0
        )
        serializer = ProductSerializer(product, context={"request": request})
        return Response(serializer.data)

    @discounted_product_detail_post_schema()
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, discount_percent__gt=0)
        action = request.data.get("action")

        if action == "comment":
            data = {"content": request.data.get("content")}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == "rate":
            data = {"value": request.data.get("rating")}
            try:
                rating = product.ratings.get(user=request.user)
                serializer = ProductRatingSerializer(rating, data=data, partial=True)
            except Rating.DoesNotExist:
                serializer = ProductRatingSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"detail": "Invalid action."},
            status=status.HTTP_400_BAD_REQUEST
        )


class ShuffledBannerProductsView(APIView):
    """Get shuffled products with banner images for homepage."""
    permission_classes = [permissions.AllowAny]

    @shuffled_banner_products_schema()
    @cache_view_response(
        "shuffled_banner_products",
        timeout=settings.CACHE_TTL.get("SHUFFLED_BANNER", 300),
        query_params=["limit"],
    )
    def get(self, request):
        limit = int(request.GET.get("limit", 10))

        products = Product.objects.select_related("brand", "category").prefetch_related(
            "images"
        ).filter(
            banner_image__isnull=False
        ).exclude(banner_image="")

        products_list = list(products)
        random.shuffle(products_list)
        products_list = products_list[:limit]

        serializer = ProductSerializer(
            products_list, many=True, context={"request": request}
        )
        return Response(serializer.data)
