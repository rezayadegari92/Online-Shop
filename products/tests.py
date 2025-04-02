from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Product, Comment, ProductImage

User = get_user_model()

class CategoryModelTest(TestCase):
    def setUp(self):
        
        self.parent_category = Category.objects.create(name="Electronics")
        
        self.child_category = Category.objects.create(name="Smartphones", parent=self.parent_category)

    def test_category_creation(self):
        
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertEqual(self.child_category.name, "Smartphones")
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_category_str(self):
        
        self.assertEqual(str(self.parent_category), "Electronics")
        expected_str = f"{self.parent_category} → {self.child_category.name}"
        self.assertEqual(str(self.child_category), expected_str)

    def test_subcategories_relation(self):
        
        self.assertIn(self.child_category, self.parent_category.subcategories.all())

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Clothing")
        self.product = Product.objects.create(
            name="T-Shirt",
            price=200,
            discount_percent=10,
            category=self.category,
            quantity=5
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "T-Shirt")
        self.assertEqual(self.product.price, 200)
        self.assertEqual(self.product.discount_percent, 10)
        self.assertEqual(self.product.category.name, "Clothing")
        self.assertEqual(self.product.quantity, 5)

    def test_discounted_price_calculation(self):
        expected_price = self.product.price - (self.product.price * self.product.discount_percent / 100)
        self.assertEqual(self.product.discounted_price, expected_price)

    def test_product_str(self):
        self.assertEqual(str(self.product), "T-Shirt")

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.category = Category.objects.create(name="Books")
        self.product = Product.objects.create(
            name="Python Book",
            price=150,
            category=self.category
        )
        self.comment = Comment.objects.create(
            product=self.product,
            author=self.user,
            content="Great book!"
        )

    def test_comment_creation(self):
        self.assertEqual(self.comment.product.name, "Python Book")
        self.assertEqual(self.comment.author.username, "testuser")
        self.assertEqual(self.comment.content, "Great book!")

    def test_comment_str(self):
        expected_str = f"Comment by testuser on Python Book"
        self.assertEqual(str(self.comment), expected_str)

class ProductImageModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Furniture")
        self.product = Product.objects.create(
            name="Chair",
            price=500,
            category=self.category
        )
        self.image = ProductImage.objects.create(
            product=self.product,
            image="products/chair.jpg"
        )

    def test_product_image_creation(self):
        self.assertEqual(self.image.product.name, "Chair")
        self.assertEqual(self.image.image, "products/chair.jpg")

    def test_product_image_str(self):
        expected_str = "Image for Chair"
        self.assertEqual(str(self.image), expected_str)