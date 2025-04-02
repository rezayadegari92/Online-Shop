from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Category, Product, Comment
from .serializers import (
    ProductSerializer, 
    ProductRatingSerializer, 
    CommentSerializer, 
    CategorySerializer
)

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['patch'], url_path='update-rating')
    def update_rating(self, request, pk=None):
        product = self.get_object()
        serializer = ProductRatingSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'rating updated', 'rating': serializer.data['rating']})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer