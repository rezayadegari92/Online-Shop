
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers


class CustomerSignupRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField(required=False)
    birth_date = serializers.DateField()
    address = serializers.JSONField(required=False, help_text="Address details as a JSON object")

class CustomerSignupResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.EmailField()


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField()

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user_type = serializers.CharField()


class VerifyOTPRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField()

class VerifyOTPResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    email = serializers.EmailField()
    user_type = serializers.CharField()


class CustomerLogoutRequestSerializer(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh token to blacklist")

class CustomerLogoutResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


class UserProfileSerializer(serializers.Serializer):
    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    phone_number = serializers.CharField(required=False)
    birth_date = serializers.DateField(required=False)
    user_type = serializers.CharField(read_only=True)
