from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from addresses.models import Address
class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
        ('customer', 'Customer'),
    )

    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    # فیلدهای مربوط به مشتریان
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    # فرض بر این است که مدل Address در اپ address تعریف شده است.
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # مشخص می‌کند که کاربر به پنل ادمین دسترسی دارد یا خیر.
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # در صورت نیاز می‌توانید فیلدهای اضافی برای ساخت سوپر یوزر اضافه کنید.

    def save(self, *args, **kwargs):
        # تنظیم is_staff برای کاربران بخش ادمین
        if self.user_type in ['manager', 'supervisor', 'operator']:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    




from django.db import models
from django.utils import timezone
from datetime import timedelta

class OTP(models.Model):
    email = models.EmailField(verbose_name="ایمیل")
    otp_code = models.CharField(max_length=6, verbose_name="کد OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    valid_until = models.DateTimeField(verbose_name="تاریخ اعتبار")

    def save(self, *args, **kwargs):
        # تنظیم زمان اعتبار (مثلاً ۱۰ دقیقه از زمان ایجاد)
        if not self.valid_until:
            self.valid_until = self.created_at + timedelta(minutes=10)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP برای {self.email}"    