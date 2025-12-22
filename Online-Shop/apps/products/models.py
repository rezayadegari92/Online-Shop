from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to="categories/", null=True, blank=True
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    def __str__(self):
        if self.parent:
            return f"{self.parent} → {self.name}"
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    # logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name="products", null=True, blank=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    banner_image = models.ImageField(
        upload_to="products/banners/", null=True, blank=True
    )

    details = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    discounted_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if self.discount_percent > 0:
            discount_amount = (
                self.price * Decimal(str(self.discount_percent))
            ) / Decimal("100")
            self.discounted_price = self.price - discount_amount
        else:
            self.discounted_price = self.price
        super(Product, self).save(*args, **kwargs)

    @property
    def final_price(self):
        if self.discount_percent:
            return self.price - (
                self.price * Decimal(str(self.discount_percent)) / Decimal("100")
            )
        return self.price

    def average_rating(self):
        # Use aggregation for better performance
        from django.db.models import Avg
        avg_rating = self.ratings.aggregate(avg=Avg('value'))['avg']
        if avg_rating is not None:
            return round(avg_rating, 1)
        return 0

    def __str__(self):
        return self.name


class Rating(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)]
    )  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "product",
            "user",
        )  # Ensure a user can only rate a product once

    def __str__(self):
        return f"Rating {self.value} for {self.product.name} by {self.user.username}"


class Comment(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.product.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/")

    def __str__(self):
        return f"Image for {self.product.name}"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, "url"):
            return self.image.url
        return ""
