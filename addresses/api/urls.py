from django.urls import path
from .views import AddressListCreateView, AddressUpdateDeleteView, SetDefaultAddressView

urlpatterns = [
    path('', AddressListCreateView.as_view(), name='address-list-create'),
    path('<int:pk>/', AddressUpdateDeleteView.as_view(), name='address-update-delete'),
    path('<int:pk>/set-default/', SetDefaultAddressView.as_view(), name='set-default-address'),
]