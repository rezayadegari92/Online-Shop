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





from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomerLoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['user_type'] = user.user_type
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        data.update({
            'user_id': self.user.id,
            'email': self.user.email,
            'user_type': self.user.user_type
        })
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
