from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CustomerSignupSerializer, CustomerLoginSerializer, VerifyOTPSerializer
from accounts.models import OTP
from datetime import datetime
from django.contrib.auth import login
from addresses.models import Address
User = get_user_model()

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

class CustomerLoginView(TokenObtainPairView):
    serializer_class = CustomerLoginSerializer    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({
                "error": "Invalid credentials",
                "detail": str(e)
            }, status=status.HTTP_401_UNAUTHORIZED)
            
        return Response(serializer.validated_data, status=status.HTTP_200_OK)   


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
                # email=email,
                # username=signup_data.get('username'),
                # password=signup_data['password'],
                # first_name=signup_data.get('first_name'),
                # last_name=signup_data.get('last_name'),
                # birth_date=birth_date,
                **user_data,
                user_type='customer'
            )
            if address_data:
                Address.objects.create(user=user, **address_data)
            if 'signup_data' in request.session:
                del request.session['signup_data']
            login(request, user)
            return Response({
                "message": "Registration successful",
                "user_id": user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)
    



from django.contrib.auth import logout
class CustomerLogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(
            {"message": "Successfully logged out"},
            status=status.HTTP_200_OK
        )    
    


from rest_framework.permissions import IsAuthenticated
from .serializers import UserProfileSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = request.user
            addresses = Address.objects.filter(user=user)
            serializer = UserProfileSerializer({
                'user': user,
                'addresses': addresses
            })
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

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