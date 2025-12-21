from django.urls import path
from .views import (
    CustomerSignupView, 
    LoginView, 
    VerifyOTPView, 
    CustomerLogoutView, 
    ProfileAPIView,
    ForgotPasswordView,
    VerifyForgotPasswordOTPView,
    ResetPasswordView,
    ChangePasswordView
)

urlpatterns = [
    path("signup/", CustomerSignupView.as_view(), name="customer-signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp" ),
    path("login/", LoginView.as_view(), name="customer-login"),
    path("logout/", CustomerLogoutView.as_view(), name="customer-logout"),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('verify-forgot-password-otp/', VerifyForgotPasswordOTPView.as_view(), name='verify-forgot-password-otp'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]