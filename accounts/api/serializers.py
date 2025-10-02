from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from accounts.models import OTP
from addresses.api.serializers import AddressSerializer
from addresses.models import Address
User = get_user_model()


class CustomerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    username = serializers.CharField(required=False, allow_blank=True)
    birth_date = serializers.DateField(required=True)
    address = AddressSerializer(required=False)
    
    class Meta:
        model = User
        fields = ["email", "username","first_name", "last_name", "password","birth_date", "address",]

        extra_kwargs = { 'address': {'required': False} }

    def validate(self, attrs):
        email = attrs.get("email")
        username = attrs.get("username")
        if not username and email:
            base = email.split("@")[0]
            candidate = base
            idx = 1
            while User.objects.filter(username=candidate).exists():
                idx += 1
                candidate = f"{base}{idx}"
            attrs["username"] = candidate
        return attrs



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class LoginSerializer(serializers.Serializer):
    email_or_username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Accept either email_or_username or separate email/username fields
        email_or_username = data.get('email_or_username') or data.get('email') or data.get('username')
        password = data.get('password')

        
        if '@' in email_or_username:
            user = User.objects.filter(email=email_or_username).first()
        else:
            user = User.objects.filter(username=email_or_username).first()

        if not user:
            raise serializers.ValidationError("User not found")

        if not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled")

        # لاگین موفق
        data['user'] = user
        return data

 
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp_code = serializers.CharField()





class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'birth_date', 'user_type', 'date_joined'
        ]
        read_only_fields = ['id', 'user_type', 'date_joined']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False}
        }
