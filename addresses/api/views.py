from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from addresses.models import Address
from addresses.api.serializers import AddressSerializer
from .schemas import (
    AddressSerializer as AddressSchemaSerializer,
    SetDefaultAddressResponseSerializer
)
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework import generics, permissions
from addresses.models import Address
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    request=AddressSchemaSerializer,
    responses={
        200: AddressSchemaSerializer(many=True),
        201: AddressSchemaSerializer,
        401: {'description': 'Unauthorized'}
    },
    summary="List and Create Addresses",
    description="Retrieve a list of user addresses or create a new address.",
    tags=['Addresses']
)
class AddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        print("User from JWT:", self.request.user)
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(
    request=AddressSchemaSerializer,
    responses={
        200: AddressSchemaSerializer,
        404: {'description': 'Not Found'},
        401: {'description': 'Unauthorized'}
    },
    summary="Retrieve, Update or Delete Address",
    description="Retrieve, update, or delete a specific address by ID.",
    tags=['Addresses']
)
class AddressUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

@extend_schema(
    responses={
        200: SetDefaultAddressResponseSerializer,
        404: {'description': 'Not Found'},
        401: {'description': 'Unauthorized'}
    },
    parameters=[
        OpenApiParameter(
            name='pk',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID of the address to set as default.'
        )
    ],
    summary="Set Default Address",
    description="Set a specific address as the default address for the authenticated user.",
    tags=['Addresses']
)
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