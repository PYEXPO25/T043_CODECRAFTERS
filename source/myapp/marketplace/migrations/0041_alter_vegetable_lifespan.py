# Generated by Django 5.1.3 on 2025-03-01 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0040_vegetable_lifespan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vegetable',
            name='lifespan',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]
