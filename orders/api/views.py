from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Order, OrderItem, DiscountCode
from .serializers import OrderSerializer, OrderItemSerializer, DiscountCodeSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """ API View for managing orders """
    queryset = Order.objects.all().order_by("-created_at")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """ Filter orders so users only see their own """
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """ Set the current user as the order owner before saving """
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def apply_discount(self, request, pk=None):
        """ Apply a discount code to an order """
        order = self.get_object()
        code = request.data.get("code")

        try:
            discount = DiscountCode.objects.get(code=code)
            order.discount_code = discount
            order.calculate_total_price()
            return Response({"message": "Discount applied successfully!", "total_price": order.total_price})
        except DiscountCode.DoesNotExist:
            return Response({"error": "Invalid discount code"}, status=400)


class DiscountCodeViewSet(viewsets.ReadOnlyModelViewSet):
    """ API View for listing discount codes """
    queryset = DiscountCode.objects.all()
    serializer_class = DiscountCodeSerializer
    permission_classes = [permissions.IsAuthenticated]