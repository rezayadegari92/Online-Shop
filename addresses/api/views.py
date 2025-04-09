from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from addresses.models import Address
from addresses.api.serializers import AddressSerializer

class UserAddressViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        try:
            address = Address.objects.get(user=request.user, is_default=True)
        except Address.DoesNotExist:
            return Response({"detail": "آدرسی به عنوان پیش‌فرض ثبت نشده"}, status=404)

        serializer = AddressSerializer(address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request):
        try:
            address = Address.objects.get(user=request.user, is_default=True)
            address.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Address.DoesNotExist:
            return Response({"detail": "آدرس پیش‌فرض پیدا نشد"}, status=404)