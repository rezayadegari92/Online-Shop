#!/usr/bin/env python
"""
Add new sample data with different and same categories.
Run with: docker compose exec web python add_new_sample_data.py
"""

import os
from decimal import Decimal

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from products.models import Brand, Category, Product


def add_new_sample_data():
    print("Adding new sample data with mixed categories...")

    # Get existing categories
    electronics = Category.objects.get(name="Electronics")
    phones = Category.objects.get(name="Smartphones")
    laptops = Category.objects.get(name="Laptops")
    clothing = Category.objects.get(name="Clothing")
    men_clothing = Category.objects.get(name="Men's Clothing")
    women_clothing = Category.objects.get(name="Women's Clothing")
    home = Category.objects.get(name="Home & Kitchen")

    # Create new categories
    books = Category.objects.get_or_create(name="Books", parent=None)[0]
    fiction = Category.objects.get_or_create(name="Fiction", parent=books)[0]
    sports = Category.objects.get_or_create(name="Sports & Outdoors", parent=None)[0]
    beauty = Category.objects.get_or_create(name="Beauty & Personal Care", parent=None)[0]
    gaming = Category.objects.get_or_create(name="Gaming", parent=electronics)[0]

    print(f"✓ Categories ready (total: {Category.objects.count()})")

    # Get existing brands
    apple = Brand.objects.get(name="Apple")
    samsung = Brand.objects.get(name="Samsung")
    dell = Brand.objects.get(name="Dell")
    nike = Brand.objects.get(name="Nike")
    adidas = Brand.objects.get(name="Adidas")

    # Create new brands
    sony = Brand.objects.get_or_create(name="Sony", website="https://sony.com")[0]
    microsoft = Brand.objects.get_or_create(name="Microsoft", website="https://microsoft.com")[0]
    xiaomi = Brand.objects.get_or_create(name="Xiaomi", website="https://xiaomi.com")[0]
    puma = Brand.objects.get_or_create(name="Puma", website="https://puma.com")[0]
    loreal = Brand.objects.get_or_create(name="L'Oreal", website="https://loreal.com")[0]

    print(f"✓ Brands ready (total: {Brand.objects.count()})")

    # Create 10 new products with mixed categories
    products_data = [
        # Using existing categories
        {
            "name": "Sony Xperia 1 V",
            "brand": sony,
            "category": phones,  # Existing category
            "price": Decimal("999.99"),
            "discount_percent": 12,
            "quantity": 60,
            "details": "Sony flagship smartphone with 4K display and professional camera system",
        },
        {
            "name": "Xiaomi Redmi Note 13 Pro",
            "brand": xiaomi,
            "category": phones,  # Existing category
            "price": Decimal("349.99"),
            "discount_percent": 18,
            "quantity": 120,
            "details": "Budget-friendly smartphone with 200MP camera and fast charging",
        },
        {
            "name": "Microsoft Surface Laptop 5",
            "brand": microsoft,
            "category": laptops,  # Existing category
            "price": Decimal("1299.99"),
            "discount_percent": 10,
            "quantity": 45,
            "details": "Premium laptop with touchscreen, Intel i7, 16GB RAM, 512GB SSD",
        },
        {
            "name": "Puma RS-X3 Sneakers",
            "brand": puma,
            "category": men_clothing,  # Existing category
            "price": Decimal("89.99"),
            "discount_percent": 25,
            "quantity": 180,
            "details": "Retro-inspired sneakers with modern comfort technology",
        },
        {
            "name": "Nike Sportswear Tech Fleece Joggers",
            "brand": nike,
            "category": men_clothing,  # Existing category
            "price": Decimal("79.99"),
            "discount_percent": 20,
            "quantity": 150,
            "details": "Lightweight joggers with Tech Fleece insulation",
        },
        # Using new categories
        {
            "name": "Sony PlayStation 5",
            "brand": sony,
            "category": gaming,  # New category
            "price": Decimal("499.99"),
            "discount_percent": 0,
            "quantity": 25,
            "details": "Next-gen gaming console with 4K gaming and ray tracing support",
        },
        {
            "name": "Xbox Series X",
            "brand": microsoft,
            "category": gaming,  # New category
            "price": Decimal("499.99"),
            "discount_percent": 5,
            "quantity": 30,
            "details": "Most powerful Xbox console with 4K gaming and Game Pass",
        },
        {
            "name": "L'Oreal Paris Revitalift Anti-Aging Cream",
            "brand": loreal,
            "category": beauty,  # New category
            "price": Decimal("24.99"),
            "discount_percent": 30,
            "quantity": 500,
            "details": "Anti-aging face cream with Pro-Retinol and SPF protection",
        },
        {
            "name": "The Great Gatsby - Hardcover Edition",
            "brand": None,
            "category": fiction,  # New category
            "price": Decimal("19.99"),
            "discount_percent": 15,
            "quantity": 200,
            "details": "Classic American novel by F. Scott Fitzgerald, premium hardcover edition",
        },
        {
            "name": "Adidas Terrex Hiking Boots",
            "brand": adidas,
            "category": sports,  # New category
            "price": Decimal("149.99"),
            "discount_percent": 22,
            "quantity": 100,
            "details": "Waterproof hiking boots with Continental rubber outsole for superior grip",
        },
    ]

    created_count = 0
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data["name"], defaults=product_data
        )
        if created:
            created_count += 1
            print(f"  ✓ Created: {product.name} ({product.category.name})")
        else:
            print(f"  - Exists: {product.name}")

    print(f"\n✓ Created {created_count} new products")
    print(f"✓ Total products: {Product.objects.count()}")

    # Summary
    print("\n" + "=" * 60)
    print("New Sample Data Summary")
    print("=" * 60)
    print(f"Categories: {Category.objects.count()}")
    print(f"Brands: {Brand.objects.count()}")
    print(f"Products: {Product.objects.count()}")
    print(f"  - Using existing categories: 5 products")
    print(f"  - Using new categories: 5 products")
    print(f"  - New categories added: Gaming, Books, Sports & Outdoors, Beauty & Personal Care")
    print("=" * 60)
    print("\n✅ New sample data added successfully!")


if __name__ == "__main__":
    add_new_sample_data()

