import random
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import OTP

def generate_random_otp():
    """
    یک کد OTP ۶ رقمی به صورت رندوم تولید می‌کند.
    """
    return str(random.randint(100000, 999999))

def create_and_send_otp(email):
    """
    برای ایمیل داده شده یک کد OTP تولید کرده، رکورد آن را ذخیره می‌کند
    و ایمیل ارسال می‌کند.
    """
    # تولید کد OTP
    otp_code = generate_random_otp()
    now = timezone.now()
    valid_until = now + timedelta(minutes=10)
    
    # ایجاد رکورد OTP در پایگاه داده
    otp_record = OTP.objects.create(
        email=email,
        otp_code=otp_code,
        valid_until=valid_until
    )
    
    # تنظیم محتوای ایمیل
    subject = 'کد تایید OTP'
    message = f'کد OTP شما: {otp_code}. این کد تا {valid_until.strftime("%H:%M")} معتبر است.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    # ارسال ایمیل
    send_mail(subject, message, from_email, recipient_list)
    
    return otp_record