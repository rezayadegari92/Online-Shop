# cart/api/v1/views.py
import json
import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404

# from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
from drf_spectacular.utils import OpenApiParameter, extend_schema
from apps.products.models import Product
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.carts.models import Cart, CartItem

from .schemas import (
    ApplyDiscountRequestSerializer,
    ApplyDiscountResponseSerializer,
    CartDetailResponseSerializer,
    CartItemUpdateDeleteRequestSerializer,
    CheckoutResponseSerializer,
)
from .schemas import CartItemCreateSerializer as CartItemCreateSchemaSerializer
from .schemas import CartItemSerializer as CartItemSchemaSerializer
from .schemas import CartSerializer as CartSchemaSerializer
from .serializers import (
    ApplyDiscountSerializer,
    CartItemCreateSerializer,
    CartItemSerializer,
    CartSerializer,
)


class CartMixin(object):
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
                cart_data = request.COOKIES.get("cart", "{}")
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
                "cart",
                json.dumps(cart_data),
                max_age=30 * 24 * 60 * 60,  # 30 days
                samesite="Lax",
                secure=not settings.DEBUG,
            )
        except Exception as e:
            logger.error(f"Error saving cart cookie: {str(e)}")


logger = logging.getLogger(__name__)


@extend_schema(
    request=CartItemCreateSchemaSerializer,
    responses={
        200: CartItemSchemaSerializer(many=True),
        201: CartItemSchemaSerializer,
        400: {"description": "Bad Request"},
    },
    summary="List and Add Cart Items",
    description="Retrieve a list of cart items or add a new item to the cart.",
    tags=["Cart Items"],
)
class CartItemListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CartItemCreateSerializer
        return CartItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart.items.select_related(
                "product", "product__brand", "product__category"
            ).prefetch_related("product__images").all()
        return CartItem.objects.none()

    def create(self, request, *args, **kwargs):
        # For anonymous users, redirect to main cart endpoint
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please use /api/cart/ endpoint for cart operations."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)

        # Stock validation with database lock to prevent race conditions
        with transaction.atomic():
            # Lock the product row for update
            product = Product.objects.select_for_update().get(id=product.id)

            # Check stock availability
            if product.quantity < quantity:
                return Response(
                    {
                        "error": f"Insufficient stock. Only {product.quantity} available.",
                        "available_quantity": product.quantity,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Check if item already exists
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={"quantity": quantity}
            )

            if not created:
                total_quantity = cart_item.quantity + quantity
                # Check if total quantity exceeds stock
                if total_quantity > product.quantity:
                    return Response(
                        {
                            "error": f"Cannot add {quantity} more. You already have {cart_item.quantity} in cart. Only {product.quantity} available.",
                            "available_quantity": product.quantity,
                            "current_in_cart": cart_item.quantity,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                cart_item.quantity = total_quantity
                cart_item.save()

        # Reload cart with optimized queries
        cart = Cart.objects.prefetch_related(
            "items__product",
            "items__product__brand",
            "items__product__category",
            "items__product__images"
        ).get(id=cart.id)
        # Return the full cart
        cart_serializer = CartSerializer(cart, context={"request": request})
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=CartItemCreateSchemaSerializer,
    responses={
        200: CartItemSchemaSerializer,
        204: {"description": "No Content"},
        400: {"description": "Bad Request"},
        404: {"description": "Not Found"},
    },
    parameters=[
        OpenApiParameter(
            name="pk",
            type=int,
            location=OpenApiParameter.PATH,
            description="ID of the cart item to retrieve, update or delete.",
        )
    ],
    summary="Retrieve, Update or Delete Cart Item",
    description="Retrieve, update, or delete a specific cart item by ID.",
    tags=["Cart Items"],
)
class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=self.request.user)
            return cart.items.select_related(
                "product", "product__brand", "product__category"
            ).prefetch_related("product__images").all()
        return CartItem.objects.none()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cart = instance.cart
        self.perform_destroy(instance)

        # If cart is empty, clear discount and optionally delete it
        if not cart.items.exists():
            cart.discount_code = None
            cart.discount_percent = 0
            cart.save()
            cart.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# cart/api/v1/views.py (ادامه)

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import CartSerializer


@extend_schema(
    responses={200: CartSchemaSerializer},
    summary="Retrieve Cart Details",
    description="Retrieve the details of the current user's cart.",
    tags=["Cart"],
)
class CartRetrieveView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Clear discount if cart is empty
        if not cart.items.exists():
            cart.discount_code = None
            cart.discount_percent = 0
            cart.save()
        # Optimize query with prefetch_related
        cart = Cart.objects.prefetch_related(
            "items__product",
            "items__product__brand",
            "items__product__category",
            "items__product__images"
        ).get(id=cart.id)
        serializer = CartSerializer(cart, context={"request": request})
        return Response(serializer.data)


# cart/api/v1/views.py (ادامه)


@extend_schema(
    request=ApplyDiscountRequestSerializer,
    responses={
        200: ApplyDiscountResponseSerializer,
        400: {"description": "Bad Request"},
    },
    summary="Apply Discount Code",
    description="Apply a discount code to the user's cart.",
    tags=["Cart"],
)
class ApplyDiscountView(APIView, CartMixin):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = ApplyDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        discount_code = serializer.validated_data["code"]
        if request.user.is_authenticated:
            cart, _ = Cart.objects.get_or_create(user=request.user)
            cart.discount_code = discount_code
            cart.discount_percent = discount_code.discount_percent
            cart.save()

            # Reload cart with optimized queries
            cart = Cart.objects.prefetch_related(
                "items__product",
                "items__product__brand",
                "items__product__category",
                "items__product__images"
            ).get(id=cart.id)
            # Return updated cart with discount applied
            cart_serializer = CartSerializer(cart, context={"request": request})
            return Response(
                {
                    "detail": f"Discount code '{discount_code.code}' applied successfully. {discount_code.discount_percent}% off!",
                    "cart": cart_serializer.data,
                }
            )
        else:
            # For anonymous users, store discount in cookie
            cart_data = self.get_cart_data(request)
            cart_data["discount_code"] = discount_code.code
            cart_data["discount_percent"] = discount_code.discount_percent
            response = Response(
                {
                    "detail": f"Discount code '{discount_code.code}' applied successfully. {discount_code.discount_percent}% off!",
                    "discount_percent": discount_code.discount_percent,
                }
            )
            self.save_cart_cookie(response, cart_data)
            return response


# cart/api/v1/views.py (ادامه)

from apps.addresses.models import Address
from apps.orders.models import Order, OrderItem
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# orders/api/v1/views.py
from rest_framework.views import APIView

from apps.carts.models import Cart


@extend_schema(
    responses={200: CheckoutResponseSerializer, 400: {"description": "Bad Request"}},
    summary="Checkout",
    description="Process the checkout for the authenticated user's cart, creating an order.",
    tags=["Orders"],
)
class CheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Please login to checkout your cart."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user = request.user

        # آدرس پیش‌فرض
        try:
            address = Address.objects.get(user=user, is_default=True)
        except Address.DoesNotExist:
            return Response(
                {"detail": "No default address found. Please add an address."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # بررسی سبد خرید
        try:
            cart = Cart.objects.prefetch_related(
                "items__product",
                "items__product__brand",
                "items__product__category"
            ).get(user=user)
        except Cart.DoesNotExist:
            return Response({"detail": "سبد خرید پیدا نشد!"}, status=400)

        if not cart.items.exists():
            return Response({"detail": "سبد خرید خالی است!"}, status=400)

        # Use transaction with row-level locking to prevent race conditions
        try:
            with transaction.atomic():
                # Validate stock availability for all items with database locks
                out_of_stock_items = []
                for item in cart.items.select_related("product"):
                    # Lock product row to prevent concurrent modifications
                    product = Product.objects.select_for_update().get(
                        id=item.product.id
                    )

                    if product.quantity < item.quantity:
                        out_of_stock_items.append(
                            {
                                "product": product.name,
                                "requested": item.quantity,
                                "available": product.quantity,
                            }
                        )

                # If any item is out of stock, rollback transaction
                if out_of_stock_items:
                    return Response(
                        {
                            "detail": "Some items are out of stock",
                            "out_of_stock_items": out_of_stock_items,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

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

                # انتقال آیتم‌ها از سبد خرید و کاهش موجودی
                # Items are already prefetched from cart query above
                for item in cart.items.all():
                    # Get locked product to ensure we have latest data
                    product = Product.objects.select_for_update().get(
                        id=item.product.id
                    )

                    # Final stock check (double-check)
                    if product.quantity < item.quantity:
                        raise ValueError(f"Product {product.name} is out of stock")

                    # Decrease stock BEFORE creating order item
                    old_quantity = product.quantity
                    product.quantity = product.quantity - item.quantity
                    product.save(update_fields=["quantity"])

                    logger.info(
                        f"Stock reduced for {product.name} (ID: {product.id}): "
                        f"Old: {old_quantity}, Sold: {item.quantity}, New: {product.quantity}"
                    )

                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item.quantity,
                        price_at_purchase=product.discounted_price,
                    )

                # محاسبه قیمت
                order.calculate_total_price()

                # خالی کردن سبد خرید و پاک کردن کد تخفیف
                cart.items.all().delete()
                cart.discount_code = None
                cart.discount_percent = 0
                cart.save()

                return Response(
                    {
                        "detail": "سفارش با موفقیت ثبت شد.",
                        "order_id": order.id,
                        "message": "Order placed successfully and inventory updated.",
                    }
                )

        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Checkout error: {str(e)}")
            return Response(
                {"detail": "An error occurred during checkout. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@extend_schema(
    responses={
        200: CartSchemaSerializer,
        400: {"description": "Bad Request"},
        500: {"description": "Internal Server Error"},
    },
    summary="Get Cart Contents",
    description="Retrieve the contents of the user's cart (authenticated or anonymous).",
    tags=["Cart"],
)
class CartView(APIView, CartMixin):
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]  # Support JWT for authenticated users

    @extend_schema(
        responses={200: CartSchemaSerializer, 400: {"description": "Bad Request"}},
        summary="Get Cart Content",
        description="Retrieve the contents of the user's cart. For anonymous users, cart data is retrieved from cookies.",
        tags=["Cart"],
    )
    def get(self, request):
        """Get cart contents"""
        try:
            cart_data = self.get_cart_data(request)
            if request.user.is_authenticated:
                # Clear discount if cart is empty
                if isinstance(cart_data, Cart) and not cart_data.items.exists():
                    cart_data.discount_code = None
                    cart_data.discount_percent = 0
                    cart_data.save()
                # Optimize query with prefetch_related
                cart_data = Cart.objects.prefetch_related(
                    "items__product",
                    "items__product__brand",
                    "items__product__category",
                    "items__product__images"
                ).get(id=cart_data.id)
                serializer = CartSerializer(cart_data, context={"request": request})
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        request=CartItemCreateSchemaSerializer,
        responses={
            200: CartSchemaSerializer,
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
            500: {"description": "Internal Server Error"},
        },
        summary="Add Item to Cart",
        description="Add a product to the user's cart. For anonymous users, cart data is stored in cookies.",
        tags=["Cart"],
    )
    def post(self, request):
        """Add item to cart"""
        try:
            serializer = CartItemCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if request.user.is_authenticated:
                # Use transaction with locking for authenticated users
                with transaction.atomic():
                    # Lock the product row
                    product = Product.objects.select_for_update().get(id=product_id)

                    # Check stock
                    if product.quantity < quantity:
                        return Response(
                            {
                                "error": f"Insufficient stock. Only {product.quantity} available.",
                                "available_quantity": product.quantity,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    cart = request.user.cart
                    if not cart:
                        cart = Cart.objects.create(user=request.user)

                    cart_item, created = CartItem.objects.select_related(
                        "product", "product__brand", "product__category"
                    ).get_or_create(
                        cart=cart, product=product, defaults={"quantity": quantity}
                    )

                    if not created:
                        total_quantity = cart_item.quantity + quantity
                        # Check total quantity against stock
                        if total_quantity > product.quantity:
                            return Response(
                                {
                                    "error": f"Cannot add {quantity} more. You already have {cart_item.quantity} in cart. Only {product.quantity} available.",
                                    "available_quantity": product.quantity,
                                    "current_in_cart": cart_item.quantity,
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                        cart_item.quantity = total_quantity
                        cart_item.save()

                serializer = CartSerializer(cart, context={"request": request})
                return Response(serializer.data)
            else:
                # For anonymous users, update cookie (basic validation)
                if product.quantity < quantity:
                    return Response(
                        {
                            "error": f"Insufficient stock. Only {product.quantity} available.",
                            "available_quantity": product.quantity,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cart_data = self.get_cart_data(request)
                current_qty = cart_data.get(str(product_id), 0)
                total_qty = current_qty + quantity

                if total_qty > product.quantity:
                    return Response(
                        {
                            "error": f"Cannot add {quantity} more. Only {product.quantity} available.",
                            "available_quantity": product.quantity,
                            "current_in_cart": current_qty,
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                cart_data[str(product_id)] = total_qty

                response = Response(cart_data)
                self.save_cart_cookie(response, cart_data)
                return response

        except Exception as e:
            logger.error(f"Error in POST cart: {str(e)}")
            return Response(
                {"error": "Failed to add item to cart"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        request=CartItemUpdateDeleteRequestSerializer,
        responses={
            200: CartSchemaSerializer,
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
            500: {"description": "Internal Server Error"},
        },
        summary="Update Item Quantity in Cart",
        description="Update the quantity of a product in the user's cart, or remove it if quantity is 0. For anonymous users, cart data is stored in cookies.",
        tags=["Cart"],
    )
    def put(self, request):
        """Update cart item quantity"""
        try:
            serializer = CartItemCreateSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            product_id = serializer.validated_data["product_id"]
            quantity = serializer.validated_data["quantity"]

            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    return Response(
                        {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                try:
                    cart_item = CartItem.objects.select_related(
                        "product", "product__brand", "product__category"
                    ).get(cart=cart, product_id=product_id)
                    if quantity > 0:
                        cart_item.quantity = quantity
                        cart_item.save()
                    else:
                        cart_item.delete()
                        # Clear discount if cart becomes empty
                        if not cart.items.exists():
                            cart.discount_code = None
                            cart.discount_percent = 0
                            cart.save()
                except CartItem.DoesNotExist:
                    return Response(
                        {"error": "Item not found in cart"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                # Reload cart with optimized queries
                cart = Cart.objects.prefetch_related(
                    "items__product",
                    "items__product__brand",
                    "items__product__category",
                    "items__product__images"
                ).get(id=cart.id)
                serializer = CartSerializer(cart, context={"request": request})
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @extend_schema(
        request=CartItemUpdateDeleteRequestSerializer,
        responses={
            200: CartSchemaSerializer,
            400: {"description": "Bad Request"},
            404: {"description": "Not Found"},
            500: {"description": "Internal Server Error"},
        },
        summary="Remove Item from Cart",
        description="Remove a product from the user's cart. For anonymous users, cart data is stored in cookies.",
        tags=["Cart"],
    )
    def delete(self, request):
        """Remove item from cart"""
        try:
            product_id = request.data.get("product_id")
            if not product_id:
                return Response(
                    {"error": "Product ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if request.user.is_authenticated:
                cart = request.user.cart
                if not cart:
                    return Response(
                        {"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND
                    )

                CartItem.objects.filter(cart=cart, product_id=product_id).delete()
                # Clear discount if cart becomes empty
                if not cart.items.exists():
                    cart.discount_code = None
                    cart.discount_percent = 0
                    cart.save()
                # Reload cart with optimized queries
                cart = Cart.objects.prefetch_related(
                    "items__product",
                    "items__product__brand",
                    "items__product__category",
                    "items__product__images"
                ).get(id=cart.id)
                serializer = CartSerializer(cart, context={"request": request})
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
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
