from addresses.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Address
        fields = ["id","state","city","street","postal_code","is_default",]
        extra_kwargs = {
            'country': {'required': False, 'default': 'Iran'},
            'user': {'read_only': True}
        }
    def create(self, validated_data):
        # Ensure existing default addresses are unset if new address is default
        if validated_data.get("is_default"):
            Address.objects.filter(user=validated_data["user"], is_default=True).update(is_default=False)
        return super().create(validated_data)    