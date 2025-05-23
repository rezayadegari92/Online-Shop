from rest_framework import viewsets, status, permissions, filters
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404


from products.models import Category, Product, Comment, Rating
from .serializers import (
    ProductSerializer, 
    ProductRatingSerializer, 
    CommentSerializer, 
    CategorySerializer
)

from django.db.models import Avg

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



class CategoryListView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        roots = Category.objects.filter(parent=None)
        serializer = CategorySerializer(roots, many=True, context={'request': request})
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


class DiscountedProductList(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        products = Product.objects.exclude(discount_percent=0)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class DiscountedProductDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        products = Product.objects.filter(discount_percent__gt=0)
        if not products.exists():
            return Response({"message": "No discounted products available"}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(products, context={'request': request})
        return Response(serializer.data)

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
