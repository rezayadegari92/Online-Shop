from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Wishlist(models.Model):
    """
    Wishlist model to store user's favorite products.
    Each user can have multiple products in their wishlist.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wishlists")
    product = models.ForeignKey(
        "products.Product", on_delete=models.CASCADE, related_name="wishlisted_by"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "product")
        ordering = ["-created_at"]
        verbose_name = "Wishlist"
        verbose_name_plural = "Wishlists"

    def __str__(self):
        return f"{self.user.email} - {self.product.name}"
