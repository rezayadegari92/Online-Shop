from addresses.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ["id","state","city","street","postal_code","phone_number","is_default",]
        extra_kwargs = {
            'country': {'required': False, 'default': 'Iran'},
            'user': {'read_only': True}
        }
    def create(self, validated_data):
        # Ensure existing default addresses are unset if new address is default
        user = self.context['request'].user
        if validated_data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return Address.objects.create(user=user, **validated_data)   