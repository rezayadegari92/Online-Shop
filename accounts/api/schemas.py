
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import serializers
from .serializers import CustomerSignupSerializer, LoginSerializer, VerifyOTPSerializer, UserProfileSerializer as RealUserProfileSerializer


class CustomerSignupRequestSerializer(CustomerSignupSerializer):
    pass

class CustomerSignupResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    email = serializers.EmailField()


class LoginRequestSerializer(LoginSerializer):
    pass

class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    access = serializers.CharField()
    refresh = serializers.CharField()
    user_type = serializers.CharField()


class VerifyOTPRequestSerializer(VerifyOTPSerializer):
    pass

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


class UserProfileSerializer(RealUserProfileSerializer):
    pass
