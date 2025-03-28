from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .managers import UserManager
from addresses.models import Address
class User(AbstractUser):
    """Custom user model with different user types and customer-specific fields."""
    
    class UserType(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        SUPERVISOR = 'supervisor', _('Supervisor')
        OPERATOR = 'operator', _('Operator')
        CUSTOMER = 'customer', _('Customer')
    
    username = None  # Remove username field, we'll use email instead
    email = models.EmailField(_('email address'), unique=True)
    user_type = models.CharField(
        _('user type'),
        max_length=20,
        choices=UserType.choices,
        default=UserType.CUSTOMER
    )
    
    # Customer-specific fields (nullable for other user types)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    addresses = models.ManyToManyField(
        Address,
        verbose_name=_('addresses'),
        blank=True,
        related_name='users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # For createsuperuser command
    
    objects = UserManager()

    def clean(self):
        """Validate that customers have first and last names"""
        super().clean()
        if self.is_customer and (not self.first_name or not self.last_name):
            raise ValidationError({
                'first_name': 'First name is required for customers',
                'last_name': 'Last name is required for customers'
            })
    
    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.user_type == self.UserType.ADMIN or self.is_superuser
    
    @property
    def is_supervisor(self):
        return self.user_type == self.UserType.SUPERVISOR
    
    @property
    def is_operator(self):
        return self.user_type == self.UserType.OPERATOR
    
    @property
    def is_customer(self):
        return self.user_type == self.UserType.CUSTOMER
    
    def save(self, *args, **kwargs):
        """Ensure customer-specific fields are null for non-customer users"""
        if not self.is_customer:
            self.birth_date = None
        super().save(*args, **kwargs)