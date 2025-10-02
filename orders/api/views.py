# orders/api/v1/views.py

from rest_framework import generics, permissions
from .serializers import OrderSerializer
from .schemas import OrderSerializer as OrderSchemaSerializer
from orders.models import Order
from drf_spectacular.utils import extend_schema, OpenApiParameter

@extend_schema(
    responses={200: OrderSchemaSerializer(many=True)},
    summary="List Orders",
    description="Retrieve a list of orders for the authenticated user.",
    tags=['Orders']
)
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_at')

@extend_schema(
    responses={200: OrderSchemaSerializer},
    parameters=[
        OpenApiParameter(
            name='pk',
            type=int,
            location=OpenApiParameter.PATH,
            description='ID of the order to retrieve.'
        )
    ],
    summary="Retrieve Order Details",
    description="Retrieve the details of a specific order by ID for the authenticated user.",
    tags=['Orders']
)
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
