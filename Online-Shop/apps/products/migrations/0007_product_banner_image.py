# Generated migration for adding banner_image to Product model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_alter_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='banner_image',
            field=models.ImageField(blank=True, null=True, upload_to='products/banners/'),
        ),
    ]

