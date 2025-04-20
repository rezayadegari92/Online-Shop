# cart/api/v1/views.py
from rest_framework import generics, permissions
from orders.models import Cart, CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer ,ApplyDiscountSerializer
from rest_framework.exceptions import ValidationError

class CartItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return CartItemSerializer

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        existing_item = cart.items.filter(product=product).first()
        if existing_item:
            raise ValidationError("این محصول قبلاً در سبد شما وجود دارد.")
        serializer.save(cart=cart)

class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        return cart.items.all()



# cart/api/v1/views.py (ادامه)

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CartSerializer

class CartRetrieveView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# cart/api/v1/views.py (ادامه)

class ApplyDiscountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ApplyDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        discount_code = serializer.validated_data['code']
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.discount_code = discount_code
        cart.save()

        return Response({"detail": f"کد تخفیف '{discount_code.code}' با موفقیت اعمال شد."})





# cart/api/v1/views.py (ادامه)

from orders.models import Order, OrderItem

class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)

        if not cart.items.exists():
            return Response({"detail": "سبد خرید شما خالی است."}, status=400)

        # 1. ساخت Order
        order = Order.objects.create(
            user=user,
            discount_code=cart.discount_code,
        )

        total = Decimal(0)
        for item in cart.items.all():
            # ساخت OrderItem
            order_item = OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.discounted_price,
            )
            total += order_item.get_total_price()

        # 2. اعمال تخفیف
        if cart.discount_code:
            discount_amount = (total * cart.discount_code.discount_percent) / 100
            total -= discount_amount

        order.total_price = total
        order.save()

        # 3. پاک‌سازی سبد خرید
        cart.items.all().delete()
        cart.discount_code = None
        cart.save()

        return Response({"detail": f"سفارش {order.id} با موفقیت ثبت شد."})
