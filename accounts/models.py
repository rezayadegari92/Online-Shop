from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from .managers import AccountManager
from addresses.models import Address

class Account(AbstractUser):
    """Custom user model with different user types and customer-specific fields."""
    
    class Role(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        SUPERVISOR = 'supervisor', _('Supervisor')
        OPERATOR = 'operator', _('Operator')
        CUSTOMER = 'customer', _('Customer')
    
    username = None  # Remove username field, we'll use email instead
    email = models.EmailField(_('email address'), unique=True)
    
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
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    role = models.CharField(_('role'), max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    addresses = models.ManyToManyField(
        Address,
        verbose_name=_('addresses'),
        blank=True,
        related_name='accounts'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # For createsuperuser command
    
    objects = AccountManager()

    
    def __str__(self):
        return self.email
    
    @property
    def is_admin(self):
        return self.user_type == self.Role.ADMIN or self.is_superuser
    
    @property
    def is_supervisor(self):
        return self.user_type == self.Role.SUPERVISOR
    
    @property
    def is_operator(self):
        return self.user_type == self.Role.OPERATOR
    
    @property
    def is_customer(self):
        return self.user_type == self.Role.CUSTOMER
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
    
    
    def clean(self):
        super().clean()
        if self.is_customer:
            if not self.first_name:
                raise ValidationError({'first_name': _('First name is required for customers')})
            if not self.last_name:
                raise ValidationError({'last_name': _('Last name is required for customers')})
            if not self.birth_date:
                raise ValidationError({'birth_date': _('Birth date is required for customers')})