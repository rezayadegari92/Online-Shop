from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product  # Importing Product model
from decimal import Decimal
from orders.models import DiscountCode  # Importing DiscountCode model
import json
from django.conf import settings

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    """ Represents a user's shopping cart """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'session_key')

    def calculate_total_price(self):
        """ Calculate total price based on cart items and discount """
        total = sum((item.get_total_price() for item in self.items.all()), Decimal(0))
        if self.discount_code:
            discount_amount = (total * self.discount_code.discount_percent) / 100
            total -= discount_amount
        return total

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

    def get_final_price(self):
        total = self.get_total_price()
        if self.discount_percent:
            discount = total * (self.discount_percent / 100)
            return total - discount
        return total

    def merge_cart(self, other_cart):
        """Merge another cart's items into this cart"""
        for item in other_cart.items.all():
            try:
                existing_item = self.items.get(product=item.product)
                existing_item.quantity += item.quantity
                existing_item.save()
            except CartItem.DoesNotExist:
                item.cart = self
                item.save()
        other_cart.delete()

    def to_dict(self):
        """Convert cart to dictionary for cookie storage"""
        return {
            'items': [
                {
                    'product_id': item.product.id,
                    'quantity': item.quantity
                } for item in self.items.all()
            ],
            'discount_code': self.discount_code.code if self.discount_code else None
        }

    @classmethod
    def from_dict(cls, data, user=None, session_key=None):
        """Create or update cart from dictionary"""
        cart, created = cls.objects.get_or_create(
            user=user,
            session_key=session_key
        )
        
        # Clear existing items
        cart.items.all().delete()
        
        # Add items from dictionary
        for item_data in data.get('items', []):
            try:
                product = Product.objects.get(id=item_data['product_id'])
                CartItem.objects.create(
                    cart=cart,
                    product=product,
                    quantity=item_data['quantity']
                )
            except Product.DoesNotExist:
                continue
        
        # Set discount code if exists
        if data.get('discount_code'):
            try:
                cart.discount_code = DiscountCode.objects.get(code=data['discount_code'])
            except DiscountCode.DoesNotExist:
                pass
        
        cart.save()
        return cart

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Anonymous Cart ({self.session_key})"

    def clear(self):
        self.items.all().delete()
        self.discount_percent = 0
        self.save()




class CartItem(models.Model):
    """ Represents a product in the shopping cart """
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product')

    def get_total_price(self):
        """ Total price for the product in cart (with discount if any) """
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in {self.cart}"

