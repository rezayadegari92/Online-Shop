from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from accounts.models import OTP
User = get_user_model()

class CustomerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    username = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True)
    
    class Meta:
        model = User
        fields = ["email", "username","first_name", "last_name", "password","birth_date"]




from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomerLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token

 
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField()