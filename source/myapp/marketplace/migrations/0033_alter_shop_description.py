# Generated by Django 5.1.3 on 2025-02-24 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0032_alter_shop_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shop',
            name='description',
            field=models.TextField(default=None, null=True),
        ),
    ]
