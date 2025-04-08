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
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'birth_date', 'user_type', 'date_joined', 'addresses'
        ]
        read_only_fields = ['id', 'user_type', 'date_joined']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False}
        }

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        user = super().update(instance, validated_data)
        
        # Process addresses
        
        address_ids = []
        for addr_data in addresses_data:
            addr_id = addr_data.get('id')
            
            if addr_id:  # Update existing address
                self._update_existing_address(user, addr_id, addr_data)
                address_ids.append(addr_id)
            else:  # Create new address
                new_addr = self._create_new_address(user, addr_data)
                address_ids.append(new_addr.id)

        user.address.exclude(id__in=address_ids).delete()        
        return user

    def _update_existing_address(self, user, addr_id, addr_data):
        try:
            address = user.address.get(id=addr_id)
            self._handle_default_address(addr_data, user, addr_id)
            
            for field, value in addr_data.items():
                if field != 'id':
                    setattr(address, field, value)
            address.save()
        except Address.DoesNotExist:
            pass  # Silently ignore invalid addresses

    def _create_new_address(self, user, addr_data):
        self._handle_default_address(addr_data, user)
        return Address.objects.create(user=user, **addr_data)

    def _handle_default_address(self, addr_data, user, exclude_id=None):
        if addr_data.get('is_default', False):
            qs = user.address.filter(is_default=True)
            if exclude_id:
                qs = qs.exclude(id=exclude_id)
            qs.update(is_default=False)

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['addresses'] = AddressSerializer(instance.addresses.all(), many=True).data
        return rep