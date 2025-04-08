from django.urls import path
from .views import CustomerSignupView, CustomerLoginView, VerifyOTPView, CustomerLogoutView, UserProfileView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", CustomerSignupView.as_view(), name="customer-signup"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp" ),
    path("login/", CustomerLoginView.as_view(), name="customer-login"),
    path("logout/", CustomerLogoutView.as_view(), name="customer-logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]