# cart/api/v1/views.py
from rest_framework import generics, permissions
from carts.models import Cart, CartItem
from .serializers import CartItemSerializer, CartItemCreateSerializer, ApplyDiscountSerializer, CartSerializer
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
import json
from products.models import Product
import logging

logger = logging.getLogger(__name__)

class CartItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Remove authentication requirement

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemCreateSerializer
        return CartItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart.items.all()
        return CartItem.objects.none()

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']
        existing_item = cart.items.filter(product=product).first()
        if existing_item:
            raise ValidationError("این محصول قبلاً در سبد شما وجود دارد.")
        serializer.save(cart=cart)

class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Remove authentication requirement
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart.items.all()
        return CartItem.objects.none()



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
    authentication_classes = []  # Remove authentication requirement

    def post(self, request):
        serializer = ApplyDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        discount_code = serializer.validated_data['code']
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart.discount_code = discount_code
            cart.save()
            return Response({"detail": f"Discount code '{discount_code.code}' applied successfully."})
        else:
            # For anonymous users, store discount in cookie
            cart_data = request.COOKIES.get('cart', '{}')
            try:
                cart_data = json.loads(cart_data)
                cart_data['discount_code'] = discount_code.code
                response = Response({"detail": f"Discount code '{discount_code.code}' applied successfully."})
                return self.save_cart_cookie(response, cart_data)
            except json.JSONDecodeError:
                return Response({"error": "Invalid cart data"}, status=status.HTTP_400_BAD_REQUEST)

    def save_cart_cookie(self, response, cart_data):
        response.set_cookie(
            'cart',
            json.dumps(cart_data),
            expires=timezone.now() + timezone.timedelta(days=7),
            httponly=True,
            samesite='Lax'
        )
        return response





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

class CartView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []  # Allow anonymous access

    def get_cart_data(self, request):
        """Get cart data from either database or cookies"""
        try:
            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    cart = Cart.objects.create(user=request.user)
                return cart
            else:
                # For anonymous users, get cart from cookie
                cart_data = request.COOKIES.get('cart', '{}')
                try:
                    return json.loads(cart_data)
                except json.JSONDecodeError:
                    logger.warning("Invalid cart data in cookie")
                    return {}
        except Exception as e:
            logger.error(f"Error getting cart data: {str(e)}")
            return {}

    def save_cart_cookie(self, response, cart_data):
        """Save cart data to cookie"""
        try:
            response.set_cookie(
                'cart',
                json.dumps(cart_data),
                max_age=30 * 24 * 60 * 60,  # 30 days
                samesite='Lax',
                secure=True
            )
        except Exception as e:
            logger.error(f"Error saving cart cookie: {str(e)}")

    def get(self, request):
        """Get cart contents"""
        try:
            cart_data = self.get_cart_data(request)
            if request.user.is_authenticated:
                serializer = CartSerializer(cart_data)
                return Response(serializer.data)
            else:
                # For anonymous users, return cart data from cookie
                response = Response(cart_data)
                self.save_cart_cookie(response, cart_data)
                return response
        except Exception as e:
            logger.error(f"Error in GET cart: {str(e)}")
            return Response(
                {"error": "Failed to retrieve cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        """Add item to cart"""
        try:
            serializer = CartItemCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"},
                    status=status.HTTP_404_NOT_FOUND
                )

            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    cart = Cart.objects.create(user=request.user)

                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    product=product,
                    defaults={'quantity': quantity}
                )

                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()

                serializer = CartSerializer(cart)
                return Response(serializer.data)
            else:
                # For anonymous users, update cookie
                cart_data = self.get_cart_data(request)
                cart_data[str(product_id)] = cart_data.get(str(product_id), 0) + quantity
                
                response = Response(cart_data)
                self.save_cart_cookie(response, cart_data)
                return response

        except Exception as e:
            logger.error(f"Error in POST cart: {str(e)}")
            return Response(
                {"error": "Failed to add item to cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request):
        """Update cart item quantity"""
        try:
            serializer = CartItemCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']

            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    return Response(
                        {"error": "Cart not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                try:
                    cart_item = CartItem.objects.get(cart=cart, product_id=product_id)
                    if quantity > 0:
                        cart_item.quantity = quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                except CartItem.DoesNotExist:
                    return Response(
                        {"error": "Item not found in cart"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                serializer = CartSerializer(cart)
                return Response(serializer.data)
            else:
                # For anonymous users, update cookie
                cart_data = self.get_cart_data(request)
                if quantity > 0:
                    cart_data[str(product_id)] = quantity
                else:
                    cart_data.pop(str(product_id), None)
                
                response = Response(cart_data)
                self.save_cart_cookie(response, cart_data)
                return response

        except Exception as e:
            logger.error(f"Error in PUT cart: {str(e)}")
            return Response(
                {"error": "Failed to update cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request):
        """Remove item from cart"""
        try:
            product_id = request.data.get('product_id')
            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    return Response(
                        {"error": "Cart not found"},
                        status=status.HTTP_404_NOT_FOUND
                    )

                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
                serializer = CartSerializer(cart)
                return Response(serializer.data)
            else:
                # For anonymous users, update cookie
                cart_data = self.get_cart_data(request)
                cart_data.pop(str(product_id), None)
                
                response = Response(cart_data)
                self.save_cart_cookie(response, cart_data)
                return response

        except Exception as e:
            logger.error(f"Error in DELETE cart: {str(e)}")
            return Response(
                {"error": "Failed to remove item from cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
