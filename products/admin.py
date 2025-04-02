from django.contrib import admin
from .models import Category, Product, Comment, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'discount_percent', 'discounted_price','category', 'rating', 'quantity')
    list_filter = ('category', 'rating')
    search_fields = ('name', 'details')
    readonly_fields = ('rating','discounted_price')  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'author', 'created_at')
    list_filter = ('created_at', 'product')
    search_fields = ('author', 'content')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'image_url')
    readonly_fields = ('image_url',)