from rest_framework import viewsets, status, permissions, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from products.models import Category, Product, Comment, Rating, Brand
from .serializers import (
    ProductSerializer, 
    ProductRatingSerializer, 
    CommentSerializer, 
    CategorySerializer
)
from .schemas import (
    ProductSerializer as ProductSchemaSerializer,
    ProductListQueryParameters,
    ProductDetailPostRequestSerializer,
    CategorySerializer as CategorySchemaSerializer,
    CategoryProductsQueryParameters,
    BrandSerializer as BrandSchemaSerializer,
    BrandProductsQueryParameters,
    CommentSerializer as CommentSchemaSerializer,
    ProductRatingSerializer as ProductRatingSchemaSerializer
)
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from products.models import Product
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

@extend_schema(
    parameters=[ProductListQueryParameters],
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Products",
    description="Retrieve a list of products with optional search and pagination.",
    tags=['Products']
)
class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        query = request.GET.get('search', '')
        products = Product.objects.all().order_by('id')

        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(brand__name__icontains=query) |
                Q(category__name__icontains=query)
            )

        paginator = PageNumberPagination()
        paginator.page_size = 10  # مثلا 10 محصول در هر صفحه
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@extend_schema(
    parameters=[OpenApiParameter(
        name='pk',
        type=int,
        location=OpenApiParameter.PATH,
        description='ID of the product to retrieve, comment on, or rate.'
    )],
    responses={
        200: ProductSchemaSerializer,
        404: {'description': 'Not Found'}
    },
    summary="Retrieve Product Details, Add Comment or Rating",
    description="Retrieve a product by ID, or add a comment/rating to it.",
    tags=['Products']
)
class ProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    # def get_permissions(self):
    #     if self.request.method == "POST":
    #         return[IsAuthenticated()]
    #     return [AllowAny()]
        
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=ProductDetailPostRequestSerializer,
        responses={
            201: CommentSchemaSerializer,
            200: ProductRatingSchemaSerializer,
            400: {'description': 'Bad Request'},
            404: {'description': 'Not Found'}
        },
        summary="Add Comment or Rating to Discounted Product",
        description="Add a comment or rating to a specific discounted product.",
        tags=['Products']
    )
    def post(self, request, pk):
        """Add comment or rating to a product."""
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        action = request.data.get('action')

        if action == 'comment':
            data = {'content': request.data.get('content')}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                # product و author را اینجا صریحاً ست می‌کنیم
                serializer.save(author=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        elif action == 'rate':
            data = {'value': request.data.get('rating')}
            try:
                rating = product.ratings.get(user=request.user)
                serializer = ProductRatingSerializer(rating, data=data, partial=True)
            except Rating.DoesNotExist:
                serializer = ProductRatingSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)



@extend_schema(
    responses={200: CategorySchemaSerializer(many=True)},
    summary="List Categories",
    description="Retrieve a list of product categories (only root categories with their children).",
    tags=['Categories']
)
class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        roots = Category.objects.filter(parent=None)
        serializer = CategorySerializer(roots, many=True, context={'request': request})
        return Response(serializer.data)


@extend_schema(
    parameters=[CategoryProductsQueryParameters],
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Products by Category",
    description="Retrieve a list of products belonging to a specific category, with pagination.",
    tags=['Categories']
)
class CategoryProductsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)

        products = category.products.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)

@extend_schema(
    parameters=[ProductListQueryParameters],
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Top Rated Products",
    description="Retrieve a list of top-rated products with pagination.",
    tags=['Products']
)
class TopRatedProductsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        products = Product.objects.all()
        sorted_products = sorted(products, key=lambda p: p.average_rating(), reverse=True)

        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(sorted_products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@extend_schema(
    responses={200: BrandSchemaSerializer(many=True)},
    summary="List Brands",
    description="Retrieve a list of all product brands.",
    tags=['Brands']
)
class BrandListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSchemaSerializer(brands, many=True, context={'request': request})
        return Response(serializer.data)


@extend_schema(
    parameters=[BrandProductsQueryParameters],
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Products by Brand",
    description="Retrieve a list of products belonging to a specific brand, with pagination.",
    tags=['Brands']
)
class BrandProductsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({'detail': 'Brand not found.'}, status=status.HTTP_404_NOT_FOUND)

        products = brand.products.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@extend_schema(
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Discounted Products",
    description="Retrieve a list of all products with a discount applied.",
    tags=['Products']
)
class DiscountedProductList(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        products = Product.objects.exclude(discount_percent=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    parameters=[OpenApiParameter(
        name='pk',
        type=int,
        location=OpenApiParameter.PATH,
        description='ID of the discounted product to retrieve.'
    )],
    responses={
        200: ProductSchemaSerializer,
        404: {'description': 'Not Found'}
    },
    summary="Retrieve Discounted Product Details",
    description="Retrieve the details of a specific discounted product.",
    tags=['Products']
)
class DiscountedProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        products = Product.objects.filter(discount_percent__gt=0)
        if not products.exists():
            return Response({"message": "No discounted products available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(products, context={'request': request})
        return Response(serializer.data)

    @extend_schema(
        request=ProductDetailPostRequestSerializer,
        responses={
            201: CommentSchemaSerializer,
            200: ProductRatingSchemaSerializer,
            400: {'description': 'Bad Request'},
            404: {'description': 'Not Found'}
        },
        summary="Add Comment or Rating to Discounted Product",
        description="Add a comment or rating to a specific discounted product.",
        tags=['Products']
    )
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, discount_percent__gt=0)
        action = request.data.get('action')

        if action == 'comment':
            data = {'content': request.data.get('content')}
            serializer = CommentSerializer(data=data)
            if serializer.is_valid():
                serializer.save(author=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'rate':
            data = {'value': request.data.get('rating')}
            try:
                rating = product.ratings.get(user=request.user)
                serializer = ProductRatingSerializer(rating, data=data, partial=True)
            except Rating.DoesNotExist:
                serializer = ProductRatingSerializer(data=data)

            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)
