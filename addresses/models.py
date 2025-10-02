from django.core.validators import RegexValidator

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
iran_phone_regex = RegexValidator(
    regex=r'^(?:\+98|0)9\d{9}$',
    message="شماره تلفن معتبر وارد کنید. مانند: 09123456789 یا +989123456789"
)

User = get_user_model() 
class Address(models.Model):
    """Address model for customers"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="addresses")
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
   
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default="Iran")
    phone_number = models.CharField(
        validators=[iran_phone_regex],
        max_length=13,  # برای +98 هم جا داره
        unique=True,
        verbose_name="شماره تلفن"
    )

    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"