from rest_framework import viewsets, status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Category, Product, Comment, Rating
from .serializers import (
    ProductSerializer, 
    ProductRatingSerializer, 
    CommentSerializer, 
    CategorySerializer
)

from django.db.models import Avg

# class ProductViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.AllowAny]
#     queryset = Product.objects.annotate(
#         avg_rating=Avg('ratings__value')
#     )
#     #queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
#     filterset_fields = ['category', 'brand']
#     search_fields = ['name', 'category__name', 'brand__name']
#     ordering_fields = ['price', 'avg_rating']
#     ordering = ['-avg_rating']
    
#     @action(detail=True, methods=['get'])
#     def popular(self, request, pk=None):
        
#         queryset = self.get_queryset().order_by('-avg_rating')

#         page = self.paginate_queryset(queryset)
#         if page is not None:
#             serializer = self.get_serializer(page, many=True)
#             return self.get_paginated_response(serializer.data)
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data)
    

# class CommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all().order_by('-created_at')
#     serializer_class = CommentSerializer
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)

#     def create(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return Response({"error": "user must be login for put comments"})
#         return super().create(request, *args, **kwargs)

# class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
#     permission_classes = [permissions.AllowAny]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class RatingViewSet(viewsets.ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = ProductRatingSerializer
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         product = serializer.validated_data['product']
#         user = self.request.user

#         rating , created = Rating.objects.get_or_create(
#             product=product,
#             user=user,
#             defaults={'value': serializer.validated_data['value']}
#         )
#         serializer.instance = rating
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from products.models import Product

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



class ProductDetailView(APIView):
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

    def post(self, request, pk):
        """Add comment or rating to a product."""
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        action = request.data.get('action')

        if action == 'comment':
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif action == 'rate':
            try:
                rating = product.ratings.get(user=request.user)
                serializer = ProductRatingSerializer(rating, data=request.data, partial=True)
            except Rating.DoesNotExist:
                serializer = ProductRatingSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save(user=request.user, product=product)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'detail': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)



class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        categories = Category.objects.filter(parent=None)  # فقط کتگوری‌های اصلی
        serializer = CategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data)


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

from products.models import Brand
from .serializers import Brandserializer

class BrandListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        brands = Brand.objects.all()
        serializer = Brandserializer(brands, many=True, context={'request': request})
        return Response(serializer.data)


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
