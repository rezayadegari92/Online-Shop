from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem, DiscountCode
from products.models import Product, Category

User = get_user_model()

class ComprehensiveOrderTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='12345')

        # Create a product category
        self.category = Category.objects.create(name='Electronics')

        # Create two products with different discount settings
        self.product1 = Product.objects.create(
            name='Smartphone',
            price=Decimal('1000.00'),
            discount_percent=10,  # Should result in discounted_price = 900.00
            category=self.category,
            rating=4,
            quantity=10
        )

        self.product2 = Product.objects.create(
            name='Laptop',
            price=Decimal('2000.00'),
            discount_percent=0,  # No discount
            category=self.category,
            rating=5,
            quantity=5
        )

        # Create a discount code for orders
        self.discount_code = DiscountCode.objects.create(code="SALE20", discount_percent=20)

    def test_product_discount_calculation(self):
        """Ensure discounted_price is correctly calculated when product is saved."""
        self.assertEqual(self.product1.discounted_price, Decimal('900.00'))
        self.assertEqual(self.product2.discounted_price, self.product2.price)

    def test_order_item_price_at_purchase_stability(self):
        """
        Ensure that price_at_purchase in OrderItem stores the product's discounted price
        at the time of creation and remains unchanged after the product is updated.
        """
        order = Order.objects.create(user=self.user, discount_code=self.discount_code)
        order_item = OrderItem.objects.create(order=order, product=self.product1, quantity=2)

        # The stored price should be the original discounted price
        self.assertEqual(order_item.price_at_purchase, Decimal('900.00'))

        # Update product's discount and save again
        self.product1.discount_percent = 20
        self.product1.save()

        # price_at_purchase should remain unchanged
        order_item.refresh_from_db()
        self.assertEqual(order_item.price_at_purchase, Decimal('900.00'))

    def test_order_total_price_calculation_with_discount_code(self):
        """
        Test Order.calculate_total_price() with a discount code.
        """
        order = Order.objects.create(user=self.user, discount_code=self.discount_code)

        # Add items to order
        OrderItem.objects.create(order=order, product=self.product1, quantity=1)  # 900.00
        OrderItem.objects.create(order=order, product=self.product2, quantity=2)  # 2 * 2000 = 4000.00

        # Total before discount = 900.00 + 4000.00 = 4900.00
        # 20% discount = 980.00 -> Final total = 3920.00
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('3920.00'))

    def test_order_total_price_without_discount_code(self):
        """
        Test Order.calculate_total_price() without a discount code.
        """
        order = Order.objects.create(user=self.user)

        # Add items to order
        OrderItem.objects.create(order=order, product=self.product1, quantity=1)  # 900.00
        OrderItem.objects.create(order=order, product=self.product2, quantity=1)  # 2000.00

        # Total = 900.00 + 2000.00 = 2900.00
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('2900.00'))