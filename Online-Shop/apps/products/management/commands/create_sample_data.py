"""
Django management command to create sample data for testing.

Usage:
    python manage.py create_sample_data
    docker-compose exec web python manage.py create_sample_data
"""

from django.core.management.base import BaseCommand

from apps.products.models import Brand, Category, Product


class Command(BaseCommand):
    help = "Create sample products, categories, and brands for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before creating new data",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Product.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Data cleared"))

        self.stdout.write("Creating sample data...")

        # Create categories
        electronics = Category.objects.get_or_create(name="Electronics", parent=None)[0]
        phones = Category.objects.get_or_create(name="Smartphones", parent=electronics)[
            0
        ]
        laptops = Category.objects.get_or_create(name="Laptops", parent=electronics)[0]
        tablets = Category.objects.get_or_create(name="Tablets", parent=electronics)[0]

        clothing = Category.objects.get_or_create(name="Clothing", parent=None)[0]
        men_clothing = Category.objects.get_or_create(
            name="Men's Clothing", parent=clothing
        )[0]
        women_clothing = Category.objects.get_or_create(
            name="Women's Clothing", parent=clothing
        )[0]

        home = Category.objects.get_or_create(name="Home & Kitchen", parent=None)[0]

        self.stdout.write(f"✓ Created {Category.objects.count()} categories")

        # Create brands
        apple = Brand.objects.get_or_create(name="Apple", website="https://apple.com")[
            0
        ]
        samsung = Brand.objects.get_or_create(
            name="Samsung", website="https://samsung.com"
        )[0]
        dell = Brand.objects.get_or_create(name="Dell", website="https://dell.com")[0]
        hp = Brand.objects.get_or_create(name="HP", website="https://hp.com")[0]
        lenovo = Brand.objects.get_or_create(
            name="Lenovo", website="https://lenovo.com"
        )[0]
        nike = Brand.objects.get_or_create(name="Nike", website="https://nike.com")[0]
        adidas = Brand.objects.get_or_create(
            name="Adidas", website="https://adidas.com"
        )[0]

        self.stdout.write(f"✓ Created {Brand.objects.count()} brands")

        # Create products
        products_data = [
            # Smartphones
            {
                "name": "iPhone 15 Pro Max",
                "brand": apple,
                "category": phones,
                "price": 1199.99,
                "discount_percent": 10,
                "quantity": 50,
                "details": "Latest iPhone with A17 Pro chip, 256GB storage, Titanium design",
            },
            {
                "name": "iPhone 14",
                "brand": apple,
                "category": phones,
                "price": 799.99,
                "discount_percent": 15,
                "quantity": 100,
                "details": "iPhone 14 with A15 Bionic chip, 128GB storage",
            },
            {
                "name": "Samsung Galaxy S24 Ultra",
                "brand": samsung,
                "category": phones,
                "price": 1099.99,
                "discount_percent": 5,
                "quantity": 75,
                "details": "Flagship Samsung phone with S Pen, 512GB storage",
            },
            {
                "name": "Samsung Galaxy A54",
                "brand": samsung,
                "category": phones,
                "price": 449.99,
                "discount_percent": 20,
                "quantity": 150,
                "details": "Mid-range Samsung phone with great camera, 128GB",
            },
            # Laptops
            {
                "name": "MacBook Pro 16-inch M3",
                "brand": apple,
                "category": laptops,
                "price": 2499.99,
                "discount_percent": 0,
                "quantity": 30,
                "details": "MacBook Pro with M3 chip, 16GB RAM, 512GB SSD",
            },
            {
                "name": "MacBook Air 13-inch M2",
                "brand": apple,
                "category": laptops,
                "price": 1199.99,
                "discount_percent": 10,
                "quantity": 60,
                "details": "Lightweight MacBook Air with M2 chip, 8GB RAM, 256GB SSD",
            },
            {
                "name": "Dell XPS 15",
                "brand": dell,
                "category": laptops,
                "price": 1799.99,
                "discount_percent": 15,
                "quantity": 40,
                "details": "Dell XPS 15 with Intel i7, 16GB RAM, 512GB SSD, NVIDIA GPU",
            },
            {
                "name": "HP Spectre x360",
                "brand": hp,
                "category": laptops,
                "price": 1399.99,
                "discount_percent": 12,
                "quantity": 35,
                "details": "2-in-1 convertible laptop with Intel i7, 16GB RAM, 512GB SSD",
            },
            {
                "name": "Lenovo ThinkPad X1 Carbon",
                "brand": lenovo,
                "category": laptops,
                "price": 1599.99,
                "discount_percent": 8,
                "quantity": 45,
                "details": "Business laptop with Intel i7, 16GB RAM, 512GB SSD",
            },
            # Tablets
            {
                "name": "iPad Pro 12.9-inch",
                "brand": apple,
                "category": tablets,
                "price": 1099.99,
                "discount_percent": 5,
                "quantity": 40,
                "details": "iPad Pro with M2 chip, 256GB storage, Liquid Retina display",
            },
            {
                "name": "iPad Air",
                "brand": apple,
                "category": tablets,
                "price": 599.99,
                "discount_percent": 10,
                "quantity": 80,
                "details": "iPad Air with M1 chip, 64GB storage",
            },
            {
                "name": "Samsung Galaxy Tab S9",
                "brand": samsung,
                "category": tablets,
                "price": 799.99,
                "discount_percent": 15,
                "quantity": 50,
                "details": "Android tablet with S Pen, 256GB storage",
            },
            # Clothing
            {
                "name": "Nike Air Max 90",
                "brand": nike,
                "category": men_clothing,
                "price": 129.99,
                "discount_percent": 25,
                "quantity": 200,
                "details": "Classic Nike sneakers, available in multiple sizes",
            },
            {
                "name": "Nike Dri-FIT Running Shorts",
                "brand": nike,
                "category": men_clothing,
                "price": 34.99,
                "discount_percent": 20,
                "quantity": 300,
                "details": "Lightweight running shorts with moisture-wicking technology",
            },
            {
                "name": "Adidas Ultraboost 23",
                "brand": adidas,
                "category": men_clothing,
                "price": 189.99,
                "discount_percent": 15,
                "quantity": 150,
                "details": "Premium running shoes with Boost cushioning",
            },
            {
                "name": "Adidas Essentials Hoodie",
                "brand": adidas,
                "category": women_clothing,
                "price": 54.99,
                "discount_percent": 30,
                "quantity": 250,
                "details": "Comfortable cotton hoodie, available in various colors",
            },
            {
                "name": "Nike Pro Leggings",
                "brand": nike,
                "category": women_clothing,
                "price": 44.99,
                "discount_percent": 20,
                "quantity": 400,
                "details": "High-waisted leggings with compression fit",
            },
        ]

        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data["name"], defaults=product_data
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f"✓ Created {created_count} new products"))
        self.stdout.write(
            self.style.SUCCESS(f"✓ Total products: {Product.objects.count()}")
        )

        # Summary
        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Sample Data Summary"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"Categories: {Category.objects.count()}")
        self.stdout.write(f"Brands: {Brand.objects.count()}")
        self.stdout.write(f"Products: {Product.objects.count()}")
        self.stdout.write(
            f"  - Electronics: {Product.objects.filter(category__parent=electronics).count()}"
        )
        self.stdout.write(
            f"  - Clothing: {Product.objects.filter(category__parent=clothing).count()}"
        )
        self.stdout.write(
            f"  - Discounted: {Product.objects.filter(discount_percent__gt=0).count()}"
        )
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("\n✅ Sample data created successfully!"))
        self.stdout.write("\nTest the API:")
        self.stdout.write("  - http://localhost:8000/api/products/")
        self.stdout.write("  - http://localhost:8000/api/products/discounted/")
        self.stdout.write("  - http://localhost:8000/api/categories/")
        self.stdout.write("  - http://localhost:8000/api/brands/")
