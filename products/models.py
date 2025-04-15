from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories') 
    def __str__(self):
        if self.parent :
            return f"{self.parent} → {self.name}"
        return self.name 
    
class Brand(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  

    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=1)
    details = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=0)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2,  blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.discount_percent > 0:
            discount_amount = (self.price * self.discount_percent) / 100
            self.discounted_price = self.price - discount_amount
        else :
            self.discounted_price = self.price
        super(Product, self).save(*args, **kwargs)     


    
    def __str__(self):
        return self.name
    

class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.product.name}"

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return ''