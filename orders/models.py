from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product  # Importing Product model
from decimal import Decimal

User = get_user_model()

class DiscountCode(models.Model):
    """ Represents discount codes that can be applied to an order """
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField()  # Percentage discount

    def __str__(self):
        return f"{self.code} - {self.discount_percent}% Off"


class Order(models.Model):
    """ Represents a user's order """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.SET_NULL, null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        """ Calculate total price based on items and discount code """
        total = sum((item.get_total_price() for item in self.items.all()), Decimal(0))
        if self.discount_code:
            discount_amount = (total * self.discount_code.discount_percent) / 100
            total -= discount_amount
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    """ Represents individual product items within an order """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """ Set the price of the product when added to order """
        self.price_at_purchase = self.product.discounted_price
        super(OrderItem, self).save(*args, **kwargs)

    def get_total_price(self):
        """ Get total price for this item (quantity * unit price) """
        return self.quantity * self.price_at_purchase

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"