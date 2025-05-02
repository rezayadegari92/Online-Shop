from django.shortcuts import render


def home(request):
    """Simple view to render the e-commerce homepage"""
    return render(request, 'home.html')


def products(request):
    return render(request, "test2.html")

def discounts(request):
    return render(request, "discounts.html")

def test(request):
    return render(request, "test.html")


def categories(request):
    return render(request, "products.html")


def category_products(request):
    return render(request, "category_products.html")


def brands(request):
    return render(request, "brands.html")



def brand_products(request):
    return render(request, "brand_products.html")


def cart(request):
    return render(request, "cart.html")


def top_rated(request):
    return render(request, "top_rated.html")