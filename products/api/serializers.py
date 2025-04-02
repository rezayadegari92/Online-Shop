from rest_framework import serializers
from products.models import Category, Product, Comment, ProductImage

class ProductImageSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ProductImage
        fields = ('id', 'image_url',) 

    def get_image_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.image.url)
        return obj.image.url    

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'product')
        read_only_fields = ('id', 'created_at',)
       

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'discount_percent',
            'category',
            'rating',
            'details',
            'quantity',
            'images',
            'comments',
        )
        read_only_fields = (
            'id',
            'name',
            'price',
            'discount_percent',
            'category',
            'details',
            'quantity',
            'images',
            'comments',
        )

class ProductRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('rating',)

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'products',)