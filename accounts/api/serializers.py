from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from accounts.models import OTP
from addresses.api.serializers import AddressSerializer
from addresses.models import Address
User = get_user_model()


class CustomerSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    username = serializers.CharField(required=True)
    birth_date = serializers.DateField(required=True)
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = ["email", "username","first_name", "last_name", "password","birth_date", "address",]

        extra_kwargs = { 'address': {'required': False} }



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
class CustomerLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_type'] = user.user_type
        return token
    username = serializers.CharField()
    password = serializers.CharField()
    def validate(self, attrs):
        
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        refresh = RefreshToken.for_user(user)
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'user_type': user.user_type,
        }
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
