"""
API views for authentication and user profile management.
Business logic is kept here, Swagger documentation is in schemas.py
"""
import logging
from datetime import datetime

from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import OTP
from addresses.models import Address

from .schemas import (
    change_password_schema,
    customer_logout_schema,
    customer_signup_schema,
    forgot_password_schema,
    get_user_profile_schema,
    login_schema,
    reset_password_schema,
    update_user_profile_schema,
    verify_forgot_password_otp_schema,
    verify_otp_schema,
)
from .serializers import (
    ChangePasswordSerializer,
    CustomerSignupSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    ResetPasswordSerializer,
    UserProfileSerializer,
    VerifyForgotPasswordOTPSerializer,
    VerifyOTPSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class CustomerSignupView(APIView):
    """Handle customer registration with OTP verification."""
    permission_classes = [permissions.AllowAny]

    @customer_signup_schema()
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data.copy()
        address_data = validated_data.pop('address', None)
        validated_data['birth_date'] = validated_data['birth_date'].isoformat()
        email = serializer.validated_data['email']

        request.session['signup_data'] = {
            'user_data': validated_data,
            'address_data': address_data
        }

        OTP.send_otp_email(email)
        return Response(
            {"message": "OTP sent to your email.", "email": email},
            status=status.HTTP_200_OK
        )


class LoginView(APIView):
    """Handle customer authentication."""
    permission_classes = [permissions.AllowAny]

    @login_schema()
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful",
            "user_id": user.id,
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user_type": user.user_type,
        }, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """Verify OTP and complete user registration."""
    permission_classes = [permissions.AllowAny]

    @verify_otp_schema()
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        signup_data = request.session.get('signup_data')
        if not signup_data:
            return Response(
                {"error": "Signup session expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user_data = signup_data['user_data'].copy()
        address_data = signup_data.get('address_data')

        try:
            birth_date = datetime.strptime(
                user_data['birth_date'],
                "%Y-%m-%d"
            ).date()
            user_data['birth_date'] = birth_date
        except (KeyError, ValueError):
            return Response(
                {"error": "Invalid birth date format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        otp = OTP.objects.filter(email=email, otp_code=otp_code).last()

        if not otp or otp.is_expired():
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(**user_data, user_type='customer')
        except Exception as e:
            logger.error(f"Failed to create user: {str(e)}")
            return Response(
                {"error": f"Failed to create user: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if address_data:
            try:
                Address.objects.create(user=user, **address_data)
            except Exception as e:
                logger.error(f"Failed to create address for user {user.id}: {str(e)}")

        if 'signup_data' in request.session:
            del request.session['signup_data']

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Registration successful",
            "user_id": user.id,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "user_type": user.user_type,
        }, status=status.HTTP_201_CREATED)


class CustomerLogoutView(APIView):
    """Handle customer logout by blacklisting refresh token."""
    permission_classes = [permissions.AllowAny]

    @customer_logout_schema()
    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"message": "Logout successful"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ProfileAPIView(APIView):
    """Handle user profile retrieval and updates."""
    authentication_classes = [JWTAuthentication]

    @get_user_profile_schema()
    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            logger.error(f"Error retrieving profile: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @update_user_profile_schema()
    def patch(self, request):
        try:
            serializer = UserProfileSerializer(
                request.user,
                data=request.data,
                partial=True
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Error updating profile: {str(e)}")
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ForgotPasswordView(APIView):
    """Send OTP for password reset."""
    permission_classes = [permissions.AllowAny]

    @forgot_password_schema()
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass

        OTP.send_otp_email(email)
        request.session['forgot_password_email'] = email

        return Response(
            {"message": "If an account exists with this email, an OTP has been sent.", "email": email},
            status=status.HTTP_200_OK
        )


class VerifyForgotPasswordOTPView(APIView):
    """Verify OTP for password reset."""
    permission_classes = [permissions.AllowAny]

    @verify_forgot_password_otp_schema()
    def post(self, request):
        serializer = VerifyForgotPasswordOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        otp = OTP.objects.filter(email=email, otp_code=otp_code).last()

        if not otp or otp.is_expired():
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        request.session['forgot_password_email'] = email
        request.session['forgot_password_otp'] = otp_code
        request.session['forgot_password_verified'] = True

        return Response(
            {"message": "OTP verified successfully. You can now reset your password."},
            status=status.HTTP_200_OK
        )


class ResetPasswordView(APIView):
    """Reset user password after OTP verification."""
    permission_classes = [permissions.AllowAny]

    @reset_password_schema()
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        email = serializer.validated_data['email']
        otp_code = serializer.validated_data['otp_code']
        new_password = serializer.validated_data['new_password']

        otp = OTP.objects.filter(email=email, otp_code=otp_code).last()
        if not otp or otp.is_expired():
            return Response(
                {"error": "Invalid or expired OTP"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        user.set_password(new_password)
        user.save()
        otp.delete()

        request.session.pop('forgot_password_email', None)
        request.session.pop('forgot_password_otp', None)
        request.session.pop('forgot_password_verified', None)

        return Response(
            {"message": "Password reset successfully. You can now login with your new password."},
            status=status.HTTP_200_OK
        )


class ChangePasswordView(APIView):
    """Change password for authenticated user."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @change_password_schema()
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        user = request.user
        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not user.check_password(old_password):
            return Response(
                {"error": "Current password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password changed successfully"},
            status=status.HTTP_200_OK
        )
