# Generated by Django 5.1.6 on 2025-02-21 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_rename_product_name_vegetables_vegetables_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vegetables',
            old_name='vegetables',
            new_name='vegetable',
        ),
    ]
