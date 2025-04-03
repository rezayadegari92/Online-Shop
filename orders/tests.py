from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Product
from .models import DiscountCode, Order, OrderItem

User = get_user_model()

class DiscountCodeModelTest(TestCase):
    def test_str_representation(self):
        discount_code = DiscountCode.objects.create(code='TEST10', discount_percent=10)
        self.assertEqual(str(discount_code), 'TEST10 - 10% Off')

class OrderModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            discounted_price=80.00
        )
        self.order = Order.objects.create(user=self.user)

    def test_order_creation_defaults(self):
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total_price, 0)

    def test_calculate_total_price_without_discount(self):
        # Create order items
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.order.calculate_total_price()
        # Expected total: 2 * 80 = 160
        self.assertEqual(self.order.total_price, 160.00)

    def test_calculate_total_price_with_discount(self):
        discount_code = DiscountCode.objects.create(code='TEST20', discount_percent=20)
        self.order.discount_code = discount_code
        self.order.save()
        OrderItem.objects.create(order=self.order, product=self.product, quantity=2)
        self.order.calculate_total_price()
        # Expected total: 160 - (160 * 0.2) = 128
        self.assertEqual(self.order.total_price, 128.00)

    def test_str_representation(self):
        self.assertEqual(str(self.order), f'Order {self.order.id} - testuser')

class OrderItemModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.product = Product.objects.create(
            name='Test Product',
            price=100.00,
            discounted_price=80.00
        )
        self.order = Order.objects.create(user=self.user)

    def test_price_auto_set_from_product_on_save(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1
        )
        self.assertEqual(order_item.price, self.product.discounted_price)

    def test_get_total_price_calculation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=80.00
        )
        self.assertEqual(order_item.get_total_price(), 240.00)

    def test_str_representation(self):
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )
        self.assertEqual(str(order_item), 'Test Product x 2')