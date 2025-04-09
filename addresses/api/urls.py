from django.urls import path
from addresses.api.views import UserAddressViewSet

user_address = UserAddressViewSet.as_view({
    'get': 'list',
    'post': 'create',
    'put': 'update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', user_address, name='user-address'),
]