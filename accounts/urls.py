from django.urls import path
from .views import ProfileView, RegistrationView, login_page

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', login_page, name='login'),
    # ... other URLs
]