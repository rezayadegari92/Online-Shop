"""
Swagger/OpenAPI schema definitions for accounts API endpoints.
All API documentation decorators are defined here.
"""
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import serializers
from .serializers import (
    CustomerSignupSerializer,
    LoginSerializer,
    VerifyOTPSerializer,
    UserProfileSerializer as RealUserProfileSerializer,
)


# Request/Response Serializers for Swagger
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


# Schema Decorators
def customer_signup_schema():
    """Schema decorator for Customer Signup endpoint."""
    return extend_schema(
        request=CustomerSignupRequestSerializer,
        responses={
            200: CustomerSignupResponseSerializer,
            400: {'description': 'Bad Request'}
        },
        tags=['Authentication'],
        summary="Customer Signup",
        description="Register a new customer and send an OTP for verification.",
        examples=[
            OpenApiExample(
                'Customer Signup Example',
                value={
                    "email": "test@example.com",
                    "password": "password123",
                    "password2": "password123",
                    "first_name": "John",
                    "last_name": "Doe",
                    "birth_date": "1990-01-01",
                    "address": {
                        "street": "123 Main St",
                        "city": "Anytown",
                        "state": "CA",
                        "postal_code": "90210",
                        "phone_number": "+989123456789"
                    }
                },
                request_only=True,
                media_type='application/json',
            )
        ]
    )


def login_schema():
    """Schema decorator for Login endpoint."""
    return extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            401: {'description': 'Unauthorized'}
        },
        tags=['Authentication'],
        summary="Customer Login",
        description="Authenticate a customer and return JWT tokens."
    )


def verify_otp_schema():
    """Schema decorator for Verify OTP endpoint."""
    return extend_schema(
        request=VerifyOTPRequestSerializer,
        responses={
            201: VerifyOTPResponseSerializer,
            400: {'description': 'Bad Request'}
        },
        tags=['Authentication'],
        summary="Verify OTP and Complete Signup",
        description="Verify the OTP sent to the user's email and complete the registration process."
    )


def customer_logout_schema():
    """Schema decorator for Customer Logout endpoint."""
    return extend_schema(
        request=CustomerLogoutRequestSerializer,
        responses={
            205: CustomerLogoutResponseSerializer,
            400: {'description': 'Bad Request'}
        },
        tags=['Authentication'],
        summary="Customer Logout",
        description="Blacklist the refresh token to log out the user."
    )


def get_user_profile_schema():
    """Schema decorator for Get User Profile endpoint."""
    return extend_schema(
        responses={200: UserProfileSerializer},
        tags=['User Profile'],
        summary="Get User Profile",
        description="Retrieve the authenticated user's profile information."
    )


def update_user_profile_schema():
    """Schema decorator for Update User Profile endpoint."""
    return extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        tags=['User Profile'],
        summary="Update User Profile",
        description="Update the authenticated user's profile information."
    )


def forgot_password_schema():
    """Schema decorator for Forgot Password endpoint."""
    return extend_schema(
        request=serializers.Serializer,
        responses={200: {'description': 'OTP sent successfully'}},
        tags=['Authentication'],
        summary="Forgot Password",
        description="Send OTP code to user's email for password reset."
    )


def verify_forgot_password_otp_schema():
    """Schema decorator for Verify Forgot Password OTP endpoint."""
    return extend_schema(
        request=serializers.Serializer,
        responses={200: {'description': 'OTP verified successfully'}},
        tags=['Authentication'],
        summary="Verify Forgot Password OTP",
        description="Verify the OTP code sent to user's email for password reset."
    )


def reset_password_schema():
    """Schema decorator for Reset Password endpoint."""
    return extend_schema(
        request=serializers.Serializer,
        responses={200: {'description': 'Password reset successfully'}},
        tags=['Authentication'],
        summary="Reset Password",
        description="Reset user password after OTP verification."
    )


def change_password_schema():
    """Schema decorator for Change Password endpoint."""
    return extend_schema(
        request=serializers.Serializer,
        responses={200: {'description': 'Password changed successfully'}},
        tags=['User Profile'],
        summary="Change Password",
        description="Change password for authenticated user."
    )
