from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CustomerSignupSerializer, LoginSerializer, VerifyOTPSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from .schemas import (
    CustomerSignupRequestSerializer,
    CustomerSignupResponseSerializer,
    LoginRequestSerializer,
    LoginResponseSerializer,
    VerifyOTPRequestSerializer,
    VerifyOTPResponseSerializer,
    CustomerLogoutRequestSerializer,
    CustomerLogoutResponseSerializer,
    UserProfileSerializer
)
from accounts.models import OTP
from datetime import datetime
# from django.contrib.auth import login
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken


from addresses.models import Address
User = get_user_model()


@extend_schema(
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
class CustomerSignupView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data.copy()
            address_data = validated_data.pop('address', None)
            validated_data['birth_date'] = validated_data['birth_date'].isoformat()
            email = serializer.validated_data['email']
            request.session['signup_data'] = {
                'user_data': validated_data,
                'address_data': address_data
            }
            # Send OTP
            otp_code = OTP.send_otp_email(email)
            return Response({"message": "OTP sent to your email.", "email": email}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

from rest_framework_simplejwt.views import TokenObtainPairView

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        request=LoginRequestSerializer,
        responses={
            200: LoginResponseSerializer,
            401: {'description': 'Unauthorized'}
        },
        tags=['Authentication'],
        summary="Customer Login",
        description="Authenticate a customer and return JWT tokens."
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
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

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


@extend_schema(
    request=VerifyOTPRequestSerializer,
    responses={
        201: VerifyOTPResponseSerializer,
        400: {'description': 'Bad Request'}
    },
    tags=['Authentication'],
    summary="Verify OTP and Complete Signup",
    description="Verify the OTP sent to the user's email and complete the registration process."
)
class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        # Handle OTP verification and user creation
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            # Retrieve temporary data from session
            signup_data = request.session.get('signup_data')
            if not signup_data:
                return Response({"error": "Signup session expired"}, status=400)

            user_data = signup_data['user_data']
            address_data = signup_data.get('address_data')
            # Verify OTP
            try:
                birth_date = datetime.strptime(
                    user_data['birth_date'], 
                    "%Y-%m-%d"
                ).date()
            except (KeyError, ValueError):
                return Response(
                    {"error": "Invalid birth date format"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            email = serializer.validated_data['email']
            otp_code = serializer.validated_data['otp_code']
            otp = OTP.objects.filter(email=email, otp_code=otp_code).last()
            
            if not otp or otp.is_expired():
                return Response({"error": "Invalid or expired OTP"}, status=400)

            # Create user with stored data
            user = User.objects.create_user(
                **user_data,
                user_type='customer'
                
            )
            if address_data:
                Address.objects.create(user=user, **address_data)
            if 'signup_data' in request.session:
                del request.session['signup_data']
            # login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Registration successful",
                "user_id": user.id,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "email": user.email,
                "user_type": user.user_type,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    



@extend_schema(
    request=CustomerLogoutRequestSerializer,
    responses={
        205: CustomerLogoutResponseSerializer,
        400: {'description': 'Bad Request'}
    },
    tags=['Authentication'],
    summary="Customer Logout",
    description="Blacklist the refresh token to log out the user."
)
class CustomerLogoutView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer


class ProfileAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    
    @extend_schema(
        responses={200: UserProfileSerializer},
        tags=['User Profile'],
        summary="Get User Profile",
        description="Retrieve the authenticated user's profile information."
    )
    def get(self, request):
        try:
            user = request.user
            serializer = UserProfileSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        request=UserProfileSerializer,
        responses={200: UserProfileSerializer},
        tags=['User Profile'],
        summary="Update User Profile",
        description="Update the authenticated user's profile information."
    )
    def patch(self, request):
        try:
            user = request.user
            serializer = UserProfileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)