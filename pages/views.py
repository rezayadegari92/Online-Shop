from django.shortcuts import render, get_object_or_404
from products.models import Category, Product, Brand
from django.db.models import Avg, Q
from django.core.paginator import Paginator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from products.api.serializers import (
    ProductSerializer,
    CategorySerializer,
    Brandserializer
)
from carts.models import Cart, CartItem
from carts.api.serializers import CartSerializer, CartItemCreateSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from django.utils import timezone
import json
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


def home(request):
    """View for the home page."""
    return render(request, 'home.html')


def products(request):
    # Get all products
    products = Product.objects.all()
    
    # Apply filters
    search = request.GET.get('search', '')
    if search:
        products = products.filter(
            Q(name__icontains=search) |
            Q(brand__name__icontains=search) |
            Q(category__name__icontains=search)
        )
    
    # Category filter
    categories = request.GET.get('categories', '')
    if categories:
        category_ids = categories.split(',')
        products = products.filter(category_id__in=category_ids)
    
    # Brand filter
    brands = request.GET.get('brands', '')
    if brands:
        brand_ids = brands.split(',')
        products = products.filter(brand_id__in=brand_ids)
    
    # Price range filter
    min_price = request.GET.get('min_price')
    if min_price:
        products = products.filter(discounted_price__gte=min_price)
    
    max_price = request.GET.get('max_price')
    if max_price:
        products = products.filter(discounted_price__lte=max_price)
    
    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'price-low':
        products = products.order_by('discounted_price')
    elif sort_by == 'price-high':
        products = products.order_by('-discounted_price')
    elif sort_by == 'rating':
        products = products.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')
    else:  # newest
        products = products.order_by('-id')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)
    
    # Get all categories and brands for filters
    all_categories = Category.objects.all()
    all_brands = Brand.objects.all()
    
    context = {
        'products': products,
        'categories': all_categories,
        'brands': all_brands,
    }
    
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product': product,
    }
    return render(request, 'products/product_detail.html', context)

def discounts(request):
    return render(request, "discounts.html")

def test(request):
    return render(request, "test.html")


def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'products/category_list.html', context)


def category_products(request, pk):
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'products/category_products.html', context)


def brand_list(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands,
    }
    return render(request, 'products/brand_list.html', context)


def brand_products(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    products = Product.objects.filter(brand=brand)
    context = {
        'brand': brand,
        'products': products,
    }
    return render(request, 'products/brand_products.html', context)


def cart(request):
    return render(request, "cart.html")


def top_rated(request):
    return render(request, "top_rated.html")

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get featured categories
        context['featured_categories'] = Category.objects.filter(parent=None)[:6]
        
        # Get top-rated products
        context['top_products'] = Product.objects.annotate(
            avg_rating=Avg('ratings__value')
        ).order_by('-avg_rating')[:8]
        
        # Get all brands
        context['brands'] = Brand.objects.all()[:8]
        
        return context

class ProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.all()
        
        # Apply filters
        search = request.GET.get('search', '')
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(brand__name__icontains=search) |
                Q(category__name__icontains=search)
            )
        
        # Category filter
        categories = request.GET.get('categories', '')
        if categories:
            category_ids = categories.split(',')
            products = products.filter(category_id__in=category_ids)
        
        # Brand filter
        brands = request.GET.get('brands', '')
        if brands:
            brand_ids = brands.split(',')
            products = products.filter(brand_id__in=brand_ids)
        
        # Price range filter
        min_price = request.GET.get('min_price')
        if min_price:
            products = products.filter(discounted_price__gte=min_price)
        
        max_price = request.GET.get('max_price')
        if max_price:
            products = products.filter(discounted_price__lte=max_price)
        
        # Sorting
        sort_by = request.GET.get('sort', 'newest')
        if sort_by == 'price-low':
            products = products.order_by('discounted_price')
        elif sort_by == 'price-high':
            products = products.order_by('-discounted_price')
        elif sort_by == 'rating':
            products = products.annotate(avg_rating=Avg('ratings__value')).order_by('-avg_rating')
        else:  # newest
            products = products.order_by('-id')
        
        # Pagination
        paginator = Paginator(products, 12)
        page = request.GET.get('page', 1)
        products = paginator.get_page(page)
        
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response({
            'products': serializer.data,
            'total_pages': paginator.num_pages,
            'current_page': int(page)
        })

class ProductDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'detail': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ProductSerializer(product, context={'request': request})
        return Response(serializer.data)

class CategoryListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

class CategoryProductsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'detail': 'Category not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        products = category.products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class BrandListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        brands = Brand.objects.all()
        serializer = Brandserializer(brands, many=True)
        return Response(serializer.data)

class BrandProductsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({'detail': 'Brand not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        products = brand.products.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class TopRatedProductsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.annotate(
            avg_rating=Avg('ratings__value')
        ).order_by('-avg_rating')
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class DiscountedProductsView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.exclude(discount_percent=0)
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class CartView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [AllowAny]
    
    def get_cart(self, request):
        """Get or create cart for the current user/session"""
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            # If there's a cart in the session, merge it
            session_cart_data = request.COOKIES.get('cart')
            if session_cart_data:
                try:
                    session_cart = Cart.from_dict(json.loads(session_cart_data))
                    cart.merge_cart(session_cart)
                except (json.JSONDecodeError, Cart.DoesNotExist):
                    pass
        else:
            session_key = request.session.session_key
            if not session_key:
                request.session.create()
                session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key, user=None)
        
        return cart
    
    def get(self, request):
        try:
            cart = self.get_cart(request)
            serializer = CartSerializer(cart)
            response = Response(serializer.data)
            
            # For anonymous users, set cart data in cookie
            if not request.user.is_authenticated:
                response.set_cookie(
                    'cart',
                    json.dumps(cart.to_dict()),
                    expires=timezone.now() + timezone.timedelta(days=7),
                    httponly=True,
                    samesite='Lax'
                )
            
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        try:
            cart = self.get_cart(request)
            serializer = CartItemCreateSerializer(data=request.data)
            
            if serializer.is_valid():
                product_id = serializer.validated_data['product'].id
                quantity = serializer.validated_data['quantity']
                
                try:
                    cart_item = cart.items.get(product_id=product_id)
                    cart_item.quantity += quantity
                    cart_item.save()
                except CartItem.DoesNotExist:
                    cart_item = CartItem.objects.create(
                        cart=cart,
                        product_id=product_id,
                        quantity=quantity
                    )
                
                response = Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
                
                # For anonymous users, update cookie
                if not request.user.is_authenticated:
                    response.set_cookie(
                        'cart',
                        json.dumps(cart.to_dict()),
                        expires=timezone.now() + timezone.timedelta(days=7),
                        httponly=True,
                        samesite='Lax'
                    )
                
                return response
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def put(self, request):
        try:
            cart = self.get_cart(request)
            product_id = request.data.get('product_id')
            quantity = request.data.get('quantity')
            
            if not product_id or quantity is None:
                return Response(
                    {'error': 'product_id and quantity are required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                cart_item = cart.items.get(product_id=product_id)
                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()
                
                response = Response(CartSerializer(cart).data)
                
                # For anonymous users, update cookie
                if not request.user.is_authenticated:
                    response.set_cookie(
                        'cart',
                        json.dumps(cart.to_dict()),
                        expires=timezone.now() + timezone.timedelta(days=7),
                        httponly=True,
                        samesite='Lax'
                    )
                
                return response
            except CartItem.DoesNotExist:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete(self, request):
        try:
            cart = self.get_cart(request)
            product_id = request.data.get('product_id')
            
            if not product_id:
                return Response(
                    {'error': 'product_id is required'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                cart_item = cart.items.get(product_id=product_id)
                cart_item.delete()
                
                response = Response(CartSerializer(cart).data)
                
                # For anonymous users, update cookie
                if not request.user.is_authenticated:
                    response.set_cookie(
                        'cart',
                        json.dumps(cart.to_dict()),
                        expires=timezone.now() + timezone.timedelta(days=7),
                        httponly=True,
                        samesite='Lax'
                    )
                
                return response
            except CartItem.DoesNotExist:
                return Response(
                    {'error': 'Item not found in cart'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)