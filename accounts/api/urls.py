from django.urls import path
from .views import CustomerSignupView, CustomerLoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("signup/", CustomerSignupView.as_view(), name="customer-signup"),
    path("login/", CustomerLoginView.as_view(), name="customer-login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]