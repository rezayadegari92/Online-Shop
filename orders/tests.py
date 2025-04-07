from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from orders.models import Order, OrderItem, DiscountCode
from products.models import Product, Category

User = get_user_model()

class ComprehensiveOrderTest(TestCase):
    def setUp(self):
        # ایجاد کاربر تستی
        self.user = User.objects.create_user(username='testuser', password='12345')
        
        # ایجاد دسته‌بندی محصول
        self.category = Category.objects.create(name='Electronics')
        
        # ایجاد دو محصول با مشخصات متفاوت
        # محصول اول دارای تخفیف 10 درصد (بنابراین قیمت نهایی 1000 - 10% = 900.00)
        self.product1 = Product.objects.create(
            name='Smartphone',
            price=Decimal('1000.00'),
            discount_percent=10,
            category=self.category,
            rating=4,
            quantity=10
        )
        # محصول دوم بدون تخفیف (بنابراین قیمت نهایی همان قیمت اصلی 2000.00)
        self.product2 = Product.objects.create(
            name='Laptop',
            price=Decimal('2000.00'),
            discount_percent=0,
            category=self.category,
            rating=5,
            quantity=5
        )
        
        # ایجاد یک کد تخفیف برای سفارش (مثلاً 20 درصد)
        self.discount_code = DiscountCode.objects.create(code="SALE20", discount_percent=20)

    def test_product_discount_calculation(self):
        """تست می‌کند که در ذخیره محصول، discounted_price به درستی محاسبه شود."""
        self.assertEqual(self.product1.discounted_price, Decimal('900.00'))
        self.assertEqual(self.product2.discounted_price, self.product2.price)

    def test_order_item_price_at_purchase_stability(self):
        """
        تست می‌کند که فیلد price_at_purchase در زمان ایجاد آیتم سفارش،
        از discounted_price محصول گرفته شده و پس از تغییر در محصول ثابت بماند.
        """
        order = Order.objects.create(user=self.user, discount_code=self.discount_code)
        order_item = OrderItem.objects.create(order=order, product=self.product1, quantity=2)
        
        # بررسی مقدار ثبت‌شده: باید برابر با 900.00 (discounted_price محصول) باشد
        self.assertEqual(order_item.price_at_purchase, Decimal('900.00'))
        
        # تغییر در تخفیف محصول (مثلاً افزایش تخفیف به 20 درصد)
        self.product1.discount_percent = 20
        self.product1.save()
        
        # با به‌روزرسانی محصول، آیتم سفارش همچنان باید قیمت ثبت‌شده اولیه (900.00) را داشته باشد.
        order_item.refresh_from_db()
        self.assertEqual(order_item.price_at_purchase, Decimal('900.00'))

    def test_order_total_price_calculation_with_discount_code(self):
        """
        تست می‌کند که متد calculate_total_price در سفارش، قیمت کل را با اعمال کد تخفیف (20%)
        به درستی محاسبه کند.
        """
        order = Order.objects.create(user=self.user, discount_code=self.discount_code)
        # ایجاد آیتم سفارش برای محصول1: 1 عدد با قیمت ثبت‌شده 900.00
        OrderItem.objects.create(order=order, product=self.product1, quantity=1)
        # ایجاد آیتم سفارش برای محصول2: 2 عدد با قیمت ثبت‌شده برابر با price اصلی (2000.00)
        OrderItem.objects.create(order=order, product=self.product2, quantity=2)
        
        # محاسبه قیمت کل بدون تخفیف:
        # محصول1: 1 * 900.00 = 900.00
        # محصول2: 2 * 2000.00 = 4000.00
        # مجموع = 900.00 + 4000.00 = 4900.00
        #
        # با کد تخفیف 20%: تخفیف = 4900.00 * 20 / 100 = 980.00
        # قیمت نهایی = 4900.00 - 980.00 = 3920.00
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('3920.00'))

    def test_order_total_price_without_discount_code(self):
        """
        تست می‌کند که در صورت عدم وجود کد تخفیف در سفارش،
        متد calculate_total_price قیمت کل را بدون اعمال تخفیف محاسبه کند.
        """
        order = Order.objects.create(user=self.user)  # بدون discount_code
        OrderItem.objects.create(order=order, product=self.product1, quantity=1)  # 900.00
        OrderItem.objects.create(order=order, product=self.product2, quantity=1)  # 2000.00
        
        # مجموع بدون تخفیف = 900.00 + 2000.00 = 2900.00
        order.calculate_total_price()
        self.assertEqual(order.total_price, Decimal('2900.00'))