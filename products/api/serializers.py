from rest_framework import serializers
from products.models import Category, Product, Comment, ProductImage, Brand, Rating
from decimal import Decimal, ROUND_HALF_UP
class Brandserializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'website'] 

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
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'author', 'content', 'created_at', 'product')
        read_only_fields = ('id', 'created_at','author',)
       

class ProductSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField(read_only=True)
    #avg_rating = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField(read_only=True)
    discounted_price = serializers.DecimalField(max_digits=10,decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'discount_percent',
            'discounted_price',
            'category',
            'details',
            'quantity',
            'final_price',
            'avg_rating',
            'images',
            'comments',
        )
        read_only_fields = (
            'id',
            'name',
            'price',
            'discount_percent',
            'discounted_price',
            'category',
            'details',
            'final_price',
            'avg_rating',
            'quantity',
            'images',
            'comments',
        )
    
    def get_avg_rating(self, obj):
        value = obj.avg_rating if hasattr(obj, 'avg_rating') and obj.avg_rating is not None else obj.average_rating()
        if value is not None:
            return Decimal(str(value)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        return None
    def get_final_price(self, obj):
        return obj.final_price

class ProductRatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'user', 'product', 'value')
        read_only_fields = ('user', 'user',)
    

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'products','parent','subcategories')


    def get_subcategories(self, obj):
        serializer = CategorySerializer(obj.subcategories.all(), many=True, context=self.context) 
        return serializer.data   




       

