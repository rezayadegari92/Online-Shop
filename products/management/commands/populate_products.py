from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, Category, Brand
from orders.models import DiscountCode
from decimal import Decimal
import random
import io
from PIL import Image


class Command(BaseCommand):
    help = 'Populate database with 50 test products'

    def create_placeholder_image(self, color, text):
        """Create a simple colored image with text"""
        img = Image.new('RGB', (400, 400), color=color)
        return img

    def handle(self, *args, **options):
        self.stdout.write('Starting database population...')

        # Create Categories
        categories_data = [
            'Electronics', 'Smartphones', 'Laptops', 'Tablets', 'Audio',
            'Wearables', 'Gaming', 'Cameras'
        ]

        categories = {}
        for cat_name in categories_data:
            cat, created = Category.objects.get_or_create(name=cat_name)
            categories[cat.name] = cat
            if created:
                self.stdout.write(f'✓ Created category: {cat.name}')

        # Create Brands
        brands_data = [
            'Apple', 'Samsung', 'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 
            'Asus', 'Microsoft', 'Google', 'Xiaomi', 'OnePlus', 'Huawei',
            'Canon', 'Nikon', 'Bose', 'JBL', 'Logitech', 'Razer', 'Corsair'
        ]

        brands = {}
        colors = [
            (52, 152, 219), (231, 76, 60), (46, 204, 113), (155, 89, 182),
            (241, 196, 15), (230, 126, 34), (149, 165, 166), (52, 73, 94)
        ]

        for i, brand_name in enumerate(brands_data):
            brand, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                self.stdout.write(f'✓ Created brand: {brand.name}')
            brands[brand.name] = brand

        # Create Products
        products_data = [
            # Smartphones
            ('iPhone 15 Pro Max', 'Smartphones', 'Apple', 1299, 10),
            ('iPhone 15 Pro', 'Smartphones', 'Apple', 1099, 15),
            ('iPhone 15', 'Smartphones', 'Apple', 899, 5),
            ('Samsung Galaxy S24 Ultra', 'Smartphones', 'Samsung', 1199, 12),
            ('Samsung Galaxy S24', 'Smartphones', 'Samsung', 999, 8),
            ('Google Pixel 8 Pro', 'Smartphones', 'Google', 999, 10),
            ('OnePlus 12 Pro', 'Smartphones', 'OnePlus', 899, 20),
            ('Xiaomi 14 Pro', 'Smartphones', 'Xiaomi', 799, 15),
            
            # Laptops
            ('MacBook Pro 16"', 'Laptops', 'Apple', 2499, 5),
            ('MacBook Air M2', 'Laptops', 'Apple', 1199, 10),
            ('Dell XPS 15', 'Laptops', 'Dell', 1799, 8),
            ('HP Spectre x360', 'Laptops', 'HP', 1499, 12),
            ('Lenovo ThinkPad X1', 'Laptops', 'Lenovo', 1699, 7),
            ('Asus ROG Zephyrus', 'Laptops', 'Asus', 2199, 15),
            ('Microsoft Surface Laptop', 'Laptops', 'Microsoft', 1299, 10),
            
            # Tablets
            ('iPad Pro 12.9"', 'Tablets', 'Apple', 1099, 8),
            ('iPad Air', 'Tablets', 'Apple', 599, 12),
            ('Samsung Galaxy Tab S9', 'Tablets', 'Samsung', 799, 10),
            ('Microsoft Surface Pro 9', 'Tablets', 'Microsoft', 999, 15),
            
            # Audio
            ('AirPods Pro 2', 'Audio', 'Apple', 249, 5),
            ('Sony WH-1000XM5', 'Audio', 'Sony', 399, 20),
            ('Bose QuietComfort 45', 'Audio', 'Bose', 329, 15),
            ('JBL Flip 6', 'Audio', 'JBL', 129, 10),
            ('Bose SoundLink', 'Audio', 'Bose', 179, 12),
            
            # Wearables
            ('Apple Watch Series 9', 'Wearables', 'Apple', 429, 8),
            ('Apple Watch SE', 'Wearables', 'Apple', 279, 12),
            ('Samsung Galaxy Watch 6', 'Wearables', 'Samsung', 349, 10),
            
            # Gaming
            ('PlayStation 5', 'Gaming', 'Sony', 499, 15),
            ('Xbox Series X', 'Gaming', 'Microsoft', 499, 12),
            ('Nintendo Switch OLED', 'Gaming', 'Microsoft', 349, 20),
            ('Razer DeathAdder V3', 'Gaming', 'Razer', 69, 5),
            ('Logitech G Pro X', 'Gaming', 'Logitech', 129, 10),
            ('Corsair K95 RGB', 'Gaming', 'Corsair', 199, 8),
            
            # Cameras
            ('Canon EOS R5', 'Cameras', 'Canon', 3899, 10),
            ('Sony A7 IV', 'Cameras', 'Sony', 2498, 15),
            ('Nikon Z9', 'Cameras', 'Nikon', 5499, 5),
            ('Canon EOS R6', 'Cameras', 'Canon', 2499, 12),
            
            # More Electronics
            ('LG OLED TV 55"', 'Electronics', 'LG', 1499, 20),
            ('Samsung QLED 65"', 'Electronics', 'Samsung', 1799, 15),
            ('Sony Bravia XR', 'Electronics', 'Sony', 2199, 10),
            ('Dell UltraSharp Monitor', 'Electronics', 'Dell', 699, 8),
            ('HP Omen Monitor', 'Electronics', 'HP', 799, 12),
            ('Asus ProArt Display', 'Electronics', 'Asus', 899, 10),
            ('Logitech MX Master 3', 'Electronics', 'Logitech', 99, 5),
            ('Razer Huntsman Elite', 'Electronics', 'Razer', 189, 15),
            ('Sony WF-1000XM5', 'Audio', 'Sony', 299, 10),
            ('Samsung Galaxy Buds Pro', 'Audio', 'Samsung', 199, 12),
            ('Google Nest Hub', 'Electronics', 'Google', 99, 20),
            ('Amazon Echo Dot', 'Electronics', 'Google', 49, 25),
        ]

        created_count = 0
        for product_data in products_data:
            name, cat_name, brand_name, price, discount = product_data
            
            product, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': categories[cat_name],
                    'brand': brands[brand_name],
                    'price': Decimal(str(price)),
                    'discount_percent': discount,
                    'details': f'High-quality {name} from {brand_name}. Perfect for your needs.',
                    'quantity': random.randint(10, 100)
                }
            )
            
            if created:
                # Create product image
                color = random.choice(colors)
                img = self.create_placeholder_image(color, name[:2])
                buffer = io.BytesIO()
                img.save(buffer, format='PNG')
                
                # Import ProductImage model
                from products.models import ProductImage
                ProductImage.objects.create(
                    product=product,
                    image=ContentFile(buffer.getvalue(), name=f'{name.lower().replace(" ", "_")}.png')
                )
                
                created_count += 1
                self.stdout.write(f'✓ Created product: {name} (${price}, {discount}% off)')

        # Create Discount Codes
        discount_codes = [
            ('SAVE10', 10),
            ('SAVE20', 20),
            ('SAVE30', 30),
            ('WELCOME15', 15),
            ('SUMMER25', 25),
        ]

        for code, discount in discount_codes:
            dc, created = DiscountCode.objects.get_or_create(
                code=code,
                defaults={'discount_percent': discount}
            )
            if created:
                self.stdout.write(f'✓ Created discount code: {code} ({discount}%)')

        self.stdout.write(self.style.SUCCESS(f'\n✅ Successfully created {created_count} products!'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total products in database: {Product.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total categories: {Category.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'✅ Total brands: {Brand.objects.count()}'))

