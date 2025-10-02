from django.contrib import admin
from django import forms
from .models import Category, Product, Comment, ProductImage, Brand, Rating
from accounts.admin import RoleBasedAdmin


class ProductImageInline(admin.TabularInline):  
    """ Allows uploading images while adding a product """
    model = ProductImage
    extra = 1  # Always show at least one empty field for new images


@admin.register(Category)
class CategoryAdmin(RoleBasedAdmin):
    """ Admin configuration for categories """
    list_display = ("name", "parent")  # Show category name and parent category
    search_fields = ("name",)  # Enable search by category name

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
    
    # This adds a "+" button next to the brand field
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        widget=admin.widgets.AutocompleteSelect(
            field=Product._meta.get_field('brand'),
            admin_site=admin.site,
        )
    )
@admin.register(Product)
class ProductAdmin(RoleBasedAdmin):
    """ Admin configuration for products """
    form = ProductForm  # Use the custom form for product
    list_display = ("name", "price", "brand","discount_percent", "discounted_price", "category", "quantity", "average_rating")
    list_filter = ("category", "discount_percent","brand")  # Filtering by category and discount percentage
    search_fields = ("name", "category__name", "brand__name")  # Search by product name and category name
    inlines = [ProductImageInline,]  # Inline for uploading product images
    readonly_fields = ("discounted_price",)  # Make discounted price read-only since it is auto-calculated
    autocomplete_fields = ['brand'] 
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['brand'].widget.can_add_related = True
        return form

@admin.register(Comment)
class CommentAdmin(RoleBasedAdmin):
    """ Admin configuration for comments """
    list_display = ("product", "author", "created_at")
    search_fields = ("product__name", "author__username")  # Enable search by product name and author username
    list_filter = ("created_at",)  # Enable filtering by creation date


@admin.register(ProductImage)
class ProductImageAdmin(RoleBasedAdmin):
    """ Admin configuration for product images """
    list_display = ("product", "image")


@admin.register(Brand)
class BrandAdmin(RoleBasedAdmin):
    """ Admin configuration for brands """
    list_display = ("name","website")
    """ Show brand name and website """
    search_fields = ("name",)    


@admin.register(Rating)
class RatingAdmin(RoleBasedAdmin):
    list_display = ['product', 'user', 'value']    