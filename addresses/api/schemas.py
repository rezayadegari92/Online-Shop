
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers


class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    street = serializers.CharField()
    city = serializers.CharField()
    state = serializers.CharField()
    zip_code = serializers.CharField()
    phone_number = serializers.CharField()
    is_default = serializers.BooleanField(read_only=True)


class SetDefaultAddressRequestSerializer(serializers.Serializer):
    # No request body needed, as pk is in the URL
    pass

class SetDefaultAddressResponseSerializer(serializers.Serializer):
    detail = serializers.CharField()
