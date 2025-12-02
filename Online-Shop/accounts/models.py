from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('manager', 'Manager'),
        ('supervisor', 'Supervisor'),
        ('operator', 'Operator'),
        ('customer', 'Customer'),
    )

    username = models.CharField(max_length=150, unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    
    
    email = models.EmailField(unique=True, null=True, blank=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    @property
    def cart(self):
        from carts.models import Cart
        cart, _ = Cart.objects.get_or_create(user=self)
        return cart 

    def save(self, *args, **kwargs):
        
        if self.user_type in ['manager', 'supervisor', 'operator']:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
    



from django.core.mail import send_mail
import random
import logging


from django.db import models
from django.utils import timezone
from datetime import timedelta
from core.tasks import send_otp_email_task

logger = logging.getLogger(__name__)


class OTP(models.Model):
    email = models.EmailField(verbose_name="ایمیل")
    otp_code = models.CharField(max_length=6, verbose_name="کد OTP")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    class Meta :
        unique_together = ("email", "otp_code")
        
    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))
    
    @classmethod
    def send_otp_email(cls,email):
        cls.objects.filter(email=email).delete()
        otp_code = cls.generate_otp()
        otp = cls.objects.create(email=email, otp_code= otp_code )
        
        # Try to send email via Celery task, fallback to synchronous if Redis is unavailable
        import time
        max_retries = 3
        retry_delay = 0.5  # seconds
        
        for attempt in range(max_retries):
            try:
                send_otp_email_task.delay(email, otp_code)
                return otp_code  # Success, return early
            except Exception as e:
                error_msg = str(e).lower()
                # Check if it's a connection/DNS error that might be temporary
                if ('connection' in error_msg or 'name resolution' in error_msg or 
                    'temporary failure' in error_msg) and attempt < max_retries - 1:
                    logger.warning(f"Celery connection attempt {attempt + 1} failed, retrying: {str(e)}")
                    time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                    continue
                else:
                    # If Celery/Redis is unavailable after retries, send email synchronously
                    logger.warning(f"Celery task failed after {attempt + 1} attempts, sending email synchronously: {str(e)}")
                    try:
                        send_mail(
                            subject="Your OTP Code",
                            message=f"Your OTP code is: {otp_code}",
                            from_email="yadegarireza50@gmail.com",
                            recipient_list=[email],
                            fail_silently=False,
                        )
                    except Exception as email_error:
                        logger.error(f"Failed to send OTP email: {str(email_error)}")
                        # Don't raise exception - OTP is still created and can be retrieved
                    return otp_code
        
        return otp_code
    def __str__(self):
        return f"OTP for {self.email}"
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)    