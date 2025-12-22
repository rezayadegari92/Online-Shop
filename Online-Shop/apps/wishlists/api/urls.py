from django.urls import path

from .views import (
    WishlistAddView,
    WishlistCheckView,
    WishlistClearView,
    WishlistListView,
    WishlistRemoveView,
    WishlistToggleView,
)

app_name = "wishlist"

urlpatterns = [
    # List all wishlist items
    path("", WishlistListView.as_view(), name="list"),
    # Add product to wishlist
    path("add/", WishlistAddView.as_view(), name="add"),
    # Toggle product in wishlist (add/remove)
    path("toggle/", WishlistToggleView.as_view(), name="toggle"),
    # Remove product from wishlist by product ID
    path("remove/<int:product_id>/", WishlistRemoveView.as_view(), name="remove"),
    # Check if product is in wishlist
    path("check/<int:product_id>/", WishlistCheckView.as_view(), name="check"),
    # Clear all wishlist items
    path("clear/", WishlistClearView.as_view(), name="clear"),
]
