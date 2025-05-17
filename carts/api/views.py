# cart/api/v1/views.py
from rest_framework import generics, permissions
from carts.models import Cart, CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer ,ApplyDiscountSerializer
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from django.shortcuts import get_object_or_404

class CartItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]

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
    permission_classes = [permissions.AllowAny]
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
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)


# cart/api/v1/views.py (ادامه)

class ApplyDiscountView(APIView):
    permission_classes = [permissions.AllowAny]

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

# orders/api/v1/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from addresses.models import Address
from carts.models import Cart
from orders.models import Order, OrderItem

class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        # آدرس پیش‌فرض
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            return Response({"detail": "هیچ آدرس پیش‌فرضی ثبت نشده!"}, status=400)

        # بررسی سبد خرید
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "سبد خرید پیدا نشد!"}, status=400)

        if not cart.items.exists():
            return Response({"detail": "سبد خرید خالی است!"}, status=400)

        # ایجاد سفارش با snapshot آدرس
        order = Order.objects.create(
            user=user,
            shipping_city=address.city,
            shipping_state=address.state,
            shipping_street=address.street,
            shipping_postal_code=address.postal_code,
            shipping_country=address.country,
            shipping_phone_number=address.phone_number,
            discount_code=cart.discount_code,
        )

        # انتقال آیتم‌ها از سبد خرید
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price_at_purchase=item.product.discounted_price
            )

        # محاسبه قیمت
        order.calculate_total_price()

        # خالی کردن سبد خرید
        cart.items.all().delete()
        cart.discount_code = None
        cart.save()

        return Response({"detail": "سفارش با موفقیت ثبت شد.", "order_id": order.id})
