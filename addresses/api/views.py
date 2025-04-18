from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from addresses.models import Address
from addresses.api.serializers import AddressSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, permissions
from addresses.models import Address

class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        print("User from JWT:", self.request.user)
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class SetDefaultAddressView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        try:
            address = Address.objects.get(pk=pk, user=request.user)
        except Address.DoesNotExist:
            return Response({"detail": " address not found  "}, status=status.HTTP_404_NOT_FOUND)

        Address.objects.filter(user=request.user, is_default=True).update(is_default=False)
        address.is_default = True
        address.save()

        return Response({"detail": "addess choosed as default."}, status=status.HTTP_200_OK)    