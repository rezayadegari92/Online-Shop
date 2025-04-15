from django.contrib import admin
from .models import Category, Product, Comment, ProductImage, Brand


class ProductImageInline(admin.TabularInline):  
    """ Allows uploading images while adding a product """
    model = ProductImage
    extra = 1  # Always show at least one empty field for new images

class BrandInline(admin.TabularInline):
    """ Allows uploading brand logo while adding a product """
    model = Brand
    extra = 1  # Always show at least one empty field for new brands

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """ Admin configuration for categories """
    list_display = ("name", "parent")  # Show category name and parent category
    search_fields = ("name",)  # Enable search by category name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """ Admin configuration for products """
    list_display = ("name", "price", "discount_percent", "discounted_price", "category", "quantity")
    list_filter = ("category", "discount_percent")  # Filtering by category and discount percentage
    search_fields = ("name", "category__name")  # Search by product name and category name
    inlines = [ProductImageInline, BrandInline]  # Inline for uploading product images
    readonly_fields = ("discounted_price",)  # Make discounted price read-only since it is auto-calculated


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """ Admin configuration for comments """
    list_display = ("product", "author", "created_at")
    search_fields = ("product__name", "author__username")  # Enable search by product name and author username
    list_filter = ("created_at",)  # Enable filtering by creation date


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """ Admin configuration for product images """
    list_display = ("product", "image")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    """ Admin configuration for brands """
    list_display = ("name", "logo")
    search_fields = ("name",)    