from addresses.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ["id","state","city","street","postal_code","phone_number","is_default","country"]
        extra_kwargs = {
            'country': {'required': False, 'default': 'Iran'},
            'postal_code': {'required': False},
            'phone_number': {'required': False},
            'user': {'read_only': True}
        }
    def create(self, validated_data):
        # Ensure existing default addresses are unset if new address is default
        request = self.context.get('request')
        if request is None:
            raise serializers.ValidationError("Request object is missing in context")
            
        user = request.user
        validated_data['user'] = user
        if validated_data.get("is_default", False) or not Address.objects.filter(user=user).exists():
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
            validated_data['is_default'] = True
        return Address.objects.create(**validated_data)
    

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        if validated_data.get("is_default", False):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)

        return super().update(instance, validated_data)