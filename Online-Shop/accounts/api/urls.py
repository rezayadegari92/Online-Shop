from django.urls import path
from .views import CustomerSignupView, LoginView, VerifyOTPView, CustomerLogoutView, ProfileAPIView

urlpatterns = [
    path("signup/", CustomerSignupView.as_view(), name="customer-signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp" ),
    path("login/", LoginView.as_view(), name="customer-login"),
    path("logout/", CustomerLogoutView.as_view(), name="customer-logout"),
    path('profile/', ProfileAPIView.as_view(), name='user-profile'),
]