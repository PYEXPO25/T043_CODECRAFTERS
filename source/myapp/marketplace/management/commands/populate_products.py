from marketplace.models import Product, Shop, Vegetable
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
       
        Product.objects.all().delete()

        prices = [
            25.0, 40.0, 35.0, 50.0, 45.0, 30.0, 38.0, 28.0, 32.0, 20.0, 60.0, 42.0, 
            150.0, 200.0, 30.0, 70.0, 25.0, 55.0, 22.0, 80.0, 10.0, 500.0, 35.0, 15.0, 
            120.0, 90.0, 20.0, 150.0, 40.0, 25.0, 75.0, 35.0, 300.0, 50.0, 45.0, 55.0, 200.0
        ]
        quantities = [200,250,100,500,1000]
        # Fetch all available shops and vegetable categories
        shop_names = list(Shop.objects.all())
        vegetables = list(Vegetable.objects.all())

        for price in prices:

            Product.objects.create(shop=random.choice(shop_names),category=random.choice(vegetables),price_per_kg=price,quantity = random.choice(quantities))

            
