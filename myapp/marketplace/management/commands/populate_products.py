from marketplace.models import Product, Shop, Vegetables
from django.core.management.base import BaseCommand
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Clear existing products (optional)
        Product.objects.all().delete()

        # List of predefined prices
        prices = [
            25.0, 40.0, 35.0, 50.0, 45.0, 30.0, 38.0, 28.0, 32.0, 20.0, 60.0, 42.0, 
            150.0, 200.0, 30.0, 70.0, 25.0, 55.0, 22.0, 80.0, 10.0, 500.0, 35.0, 15.0, 
            120.0, 90.0, 20.0, 150.0, 40.0, 25.0, 75.0, 35.0, 300.0, 50.0, 45.0, 55.0, 200.0
        ]

        # Fetch all available shops and vegetable categories
        shop_names = list(Shop.objects.all())
        vegetables = list(Vegetables.objects.all())

        if not shop_names or not vegetables:
            self.stdout.write(self.style.ERROR("No Shops or Vegetables found! Please populate them first."))
            return

        # Generate mock data for each price
        for price in prices:
            shop = random.choice(shop_names)  
            category = random.choice(vegetables)
            image = category.images  # Using category image as default

            quantity = random.randint(1, 100)  
            description = f"Fresh {category.vegetable} available at {shop.shop_name}."

            # Create Product entry
            Product.objects.create(
                price_per_kg=price,
                shop_name=shop,
                category=category,
                quantity=quantity,
                description=description,
                image=image
            )

        self.stdout.write(self.style.SUCCESS(f"Inserted {len(prices)} mock products successfully!"))
