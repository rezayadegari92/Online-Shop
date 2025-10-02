from django.urls import path
from .views import (
    ProfileView, 
    RegisterView, 
    CustomLoginView, 
    CustomLogoutView,
    OrderListView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('orders/', OrderListView.as_view(), name='orders'),
    # ... other URLs
]