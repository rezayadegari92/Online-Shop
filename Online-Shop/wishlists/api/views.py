from drf_spectacular.utils import extend_schema
from products.models import Product
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from wishlists.models import Wishlist

from .serializers import WishlistSerializer, WishlistToggleSerializer


@extend_schema(
    tags=["Wishlist"],
    summary="List user's wishlist",
    description="Get all products in authenticated user's wishlist",
    responses={200: WishlistSerializer(many=True)},
)
class WishlistListView(APIView):
    """List all wishlist items for authenticated user."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """Get user's wishlist."""
        wishlists = Wishlist.objects.filter(user=request.user).select_related(
            "product", "product__brand", "product__category"
        )
        serializer = WishlistSerializer(
            wishlists, many=True, context={"request": request}
        )
        return Response(serializer.data)


@extend_schema(
    tags=["Wishlist"],
    summary="Add product to wishlist",
    description="Add a product to authenticated user's wishlist",
    request=WishlistToggleSerializer,
    responses={
        201: WishlistSerializer,
        400: {"description": "Bad Request"},
        404: {"description": "Product not found"},
    },
)
class WishlistAddView(APIView):
    """Add product to wishlist."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """Add product to wishlist."""
        serializer = WishlistToggleSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]

            # Check if product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Check if already in wishlist
            if Wishlist.objects.filter(user=request.user, product=product).exists():
                return Response(
                    {"message": "Product already in wishlist"},
                    status=status.HTTP_200_OK,
                )

            # Add to wishlist
            wishlist = Wishlist.objects.create(user=request.user, product=product)
            response_serializer = WishlistSerializer(
                wishlist, context={"request": request}
            )
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Wishlist"],
    summary="Remove product from wishlist",
    description="Remove a product from authenticated user's wishlist by product ID",
    responses={
        200: {"description": "Product removed from wishlist"},
        404: {"description": "Product not in wishlist"},
    },
)
class WishlistRemoveView(APIView):
    """Remove product from wishlist."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request, product_id):
        """Remove product from wishlist."""
        try:
            wishlist = Wishlist.objects.get(user=request.user, product_id=product_id)
            wishlist.delete()
            return Response(
                {"message": "Product removed from wishlist"},
                status=status.HTTP_200_OK,
            )
        except Wishlist.DoesNotExist:
            return Response(
                {"error": "Product not in wishlist"}, status=status.HTTP_404_NOT_FOUND
            )


@extend_schema(
    tags=["Wishlist"],
    summary="Toggle product in wishlist",
    description="Add or remove a product from wishlist (if exists, remove; if not, add)",
    request=WishlistToggleSerializer,
    responses={
        200: {"description": "Product toggled in wishlist", "type": "object"},
        400: {"description": "Bad Request"},
        404: {"description": "Product not found"},
    },
)
class WishlistToggleView(APIView):
    """Toggle product in wishlist (add if not exists, remove if exists)."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """Toggle product in wishlist."""
        serializer = WishlistToggleSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data["product_id"]

            # Check if product exists
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
                )

            # Check if in wishlist
            wishlist = Wishlist.objects.filter(user=request.user, product=product)

            if wishlist.exists():
                # Remove from wishlist
                wishlist.delete()
                return Response(
                    {
                        "message": "Product removed from wishlist",
                        "in_wishlist": False,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Add to wishlist
                Wishlist.objects.create(user=request.user, product=product)
                return Response(
                    {
                        "message": "Product added to wishlist",
                        "in_wishlist": True,
                    },
                    status=status.HTTP_200_OK,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Wishlist"],
    summary="Check if product is in wishlist",
    description="Check if a specific product is in authenticated user's wishlist",
    responses={
        200: {
            "description": "Wishlist status",
            "type": "object",
            "properties": {
                "in_wishlist": {"type": "boolean"},
                "product_id": {"type": "integer"},
            },
        }
    },
)
class WishlistCheckView(APIView):
    """Check if product is in user's wishlist."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, product_id):
        """Check if product is in wishlist."""
        in_wishlist = Wishlist.objects.filter(
            user=request.user, product_id=product_id
        ).exists()

        return Response(
            {"in_wishlist": in_wishlist, "product_id": product_id},
            status=status.HTTP_200_OK,
        )


@extend_schema(
    tags=["Wishlist"],
    summary="Clear all wishlist items",
    description="Remove all products from authenticated user's wishlist",
    responses={200: {"description": "Wishlist cleared"}},
)
class WishlistClearView(APIView):
    """Clear all items from user's wishlist."""

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def delete(self, request):
        """Clear user's wishlist."""
        count = Wishlist.objects.filter(user=request.user).count()
        Wishlist.objects.filter(user=request.user).delete()

        return Response(
            {"message": f"Cleared {count} items from wishlist"},
            status=status.HTTP_200_OK,
        )
