from django.utils.deprecation import MiddlewareMixin
from .models import Cart, CartItem
import json

class CartMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """Handle cart merging after login"""
        if request.user.is_authenticated and 'cart' in request.COOKIES:
            try:
                # Get cart data from cookie
                cart_data = json.loads(request.COOKIES.get('cart', '{}'))
                
                # Get or create user's cart
                cart, _ = Cart.objects.get_or_create(user=request.user)
                
                # Merge items from cookie into user's cart
                for product_id, item_data in cart_data.items():
                    # Handle both dictionary and integer quantity formats
                    quantity = item_data.get('quantity', 1) if isinstance(item_data, dict) else item_data
                    
                    cart_item, created = cart.items.get_or_create(
                        product_id=product_id,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                
                # Clear the cart cookie
                response.delete_cookie('cart')
                
            except (json.JSONDecodeError, ValueError):
                # If there's any error, just clear the cookie
                response.delete_cookie('cart')
        
        return response 