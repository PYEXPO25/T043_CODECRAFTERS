# Generated by Django 5.1.3 on 2025-02-24 06:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0028_alter_shop_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShopImage',
        ),
    ]
