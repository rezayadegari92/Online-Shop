"""
Django management command to create sample discount codes.

Usage:
    python manage.py create_discount_codes
    docker-compose exec web python manage.py create_discount_codes
"""

from django.core.management.base import BaseCommand

from apps.orders.models import DiscountCode


class Command(BaseCommand):
    help = "Create sample discount codes for testing"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing discount codes before creating new ones",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing discount codes..."))
            DiscountCode.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("✓ Discount codes cleared"))

        self.stdout.write("Creating sample discount codes...")

        discount_codes = [
            {"code": "WELCOME10", "discount_percent": 10},
            {"code": "SAVE20", "discount_percent": 20},
            {"code": "SUMMER25", "discount_percent": 25},
            {"code": "MEGA50", "discount_percent": 50},
            {"code": "VIP15", "discount_percent": 15},
            {"code": "NEWYEAR30", "discount_percent": 30},
            {"code": "FLASH40", "discount_percent": 40},
            {"code": "STUDENT5", "discount_percent": 5},
        ]

        created_count = 0
        for code_data in discount_codes:
            discount_code, created = DiscountCode.objects.get_or_create(
                code=code_data["code"], defaults=code_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    f"  ✓ Created: {discount_code.code} - {discount_code.discount_percent}% off"
                )
            else:
                self.stdout.write(
                    f"  - Exists: {discount_code.code} - {discount_code.discount_percent}% off"
                )

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(self.style.SUCCESS("Discount Codes Summary"))
        self.stdout.write("=" * 60)
        self.stdout.write(f"Created: {created_count} new discount codes")
        self.stdout.write(f"Total: {DiscountCode.objects.count()} discount codes")
        self.stdout.write("=" * 60)

        self.stdout.write("\n✅ Sample discount codes created successfully!")
        self.stdout.write("\nAvailable discount codes:")
        for code in DiscountCode.objects.all().order_by("-discount_percent"):
            self.stdout.write(f"  • {code.code} → {code.discount_percent}% OFF")

        self.stdout.write("\n\nTest in API:")
        self.stdout.write("  POST /api/cart/apply-discount/")
        self.stdout.write('  {"code": "WELCOME10"}')
