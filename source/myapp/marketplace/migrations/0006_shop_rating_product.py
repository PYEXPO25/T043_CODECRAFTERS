# Generated by Django 5.1.6 on 2025-02-21 12:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0005_vegetables_images'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='rating',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prize_per_kg', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.vegetables')),
                ('shop_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='marketplace.shop')),
            ],
        ),
    ]
