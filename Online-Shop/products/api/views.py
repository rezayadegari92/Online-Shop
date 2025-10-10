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
from django.conf import settings
from django.db.models import Q
from products.models import Product
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
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
        # Get query parameters
        search_query = request.GET.get('search', '')
        category_id = request.GET.get('category')
        brand_id = request.GET.get('brand')
        sort_by = request.GET.get('sort', 'id')
        
        # Start with all products
        products = Product.objects.select_related('brand', 'category').all()

        # Apply search filter
        if search_query:
            products = products.filter(
                Q(name__icontains=search_query) |
                Q(brand__name__icontains=search_query) |
                Q(category__name__icontains=search_query) |
                Q(details__icontains=search_query)
            )

        # Apply category filter
        if category_id:
            try:
                products = products.filter(category_id=category_id)
            except ValueError:
                return Response({'detail': 'Invalid category ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply brand filter
        if brand_id:
            try:
                products = products.filter(brand_id=brand_id)
            except ValueError:
                return Response({'detail': 'Invalid brand ID.'}, status=status.HTTP_400_BAD_REQUEST)

        # Apply sorting
        if sort_by == 'name':
            products = products.order_by('name')
        elif sort_by == 'price':
            products = products.order_by('price')
        elif sort_by == '-price':
            products = products.order_by('-price')
        elif sort_by == 'rating':
            # Use database aggregation for proper sorting with pagination
            products = products.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating', 'id')
        else:
            products = products.order_by('id')

        # Apply pagination
        paginator = CustomPageNumberPagination()
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

        products = category.products.select_related('brand', 'category').all().order_by('id')
        paginator = CustomPageNumberPagination()
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
        # Use database aggregation for proper sorting with pagination
        products = Product.objects.select_related('brand', 'category').annotate(
            avg_rating=Avg('ratings__value')
        ).order_by('-avg_rating', 'id')

        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
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

        products = brand.products.select_related('brand', 'category').all().order_by('id')
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


@extend_schema(
    parameters=[ProductListQueryParameters],
    responses={200: ProductSchemaSerializer(many=True)},
    summary="List Discounted Products",
    description="Retrieve a list of all products with a discount applied, with pagination.",
    tags=['Products']
)
class DiscountedProductList(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        products = Product.objects.select_related('brand', 'category').exclude(
            discount_percent=0
        ).order_by('-discount_percent', 'id')
        
        paginator = CustomPageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(paginated_products, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)


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
