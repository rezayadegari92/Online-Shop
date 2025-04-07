from addresses.models import Address
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model:Address
        fields = ["state","city","street","postal_code","is_default",]