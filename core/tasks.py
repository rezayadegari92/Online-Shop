from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email_task(email, otp_code):
    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is: {otp_code}",
        from_email="yadegarireza50@gmail.com",
        recipient_list=[email],
        fail_silently=False,
    )