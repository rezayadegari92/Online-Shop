
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model() 
class Address(models.Model):
    """Address model for customers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="address")
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
   
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Iran")
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"