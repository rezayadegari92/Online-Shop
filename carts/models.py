from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product  # Importing Product model
from decimal import Decimal
from orders.models import DiscountCode  # Importing DiscountCode model

User = get_user_model()

# Create your models here.
class Cart(models.Model):
    """ Represents a user's shopping cart """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)

    def calculate_total_price(self):
        """ Calculate total price based on cart items and discount """
        total = sum((item.get_total_price() for item in self.items.all()), Decimal(0))
        if self.discount_code:
            discount_amount = (total * self.discount_code.discount_percent) / 100
            total -= discount_amount
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"




class CartItem(models.Model):
    """ Represents a product in the shopping cart """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        """ Total price for the product in cart (with discount if any) """
        return self.quantity * self.product.discounted_price

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

