from rest_framework import serializers
from products.models import Product, Category, Comment, Rating, ProductImage



class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = ['user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['user', 'value', 'product']
        read_only_fields = ['user']
        extra_kwargs = {'product': {'write_only': True}}

class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.StringRelatedField()
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'children']

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    current_price = serializers.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'category', 'price', 'current_price',
            'discount', 'quantity', 'detail', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']