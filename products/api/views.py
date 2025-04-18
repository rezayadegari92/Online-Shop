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

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.annotate(
        avg_rating=Avg('ratings__value')
    )
    #queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name', 'category__name', 'brand__name']
    ordering_fields = ['price', 'avg_rating']
    ordering = ['-avg_rating']
    
    @action(detail=True, methods=['get'])
    def popular(self, request, pk=None):
        
        sorted_products = sorted(
            self.get_queryset(),
            key=lambda x: x.avg_rating,
            reverse=True
        )
        page = self.paginate_queryset(sorted_products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(sorted_products, many=True)
        return Response(serializer.data)
    

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"error": "user must be login for put comments"})
        return super().create(request, *args, **kwargs)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = ProductRatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        user = self.request.user

        rating , created = Rating.objects.get_or_create(
            product=product,
            user=user,
            defaults={'value': serializer.validated_data['value']}
        )
        serializer.instance = rating
