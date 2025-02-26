from django.core.management.base import BaseCommand
from marketplace.models import Rating, User, Shop
import random

class Command(BaseCommand):
    help = "Populate the Rating model with sample data."

    def handle(self, *args, **options):
        Rating.objects.all().delete()
        
        shops = list(Shop.objects.all())  # Convert to list to avoid multiple queries
        users = list(User.objects.all())
        reviews = ['Good Product', 'Nice one', 'Not that good', 'Poor']

        if not shops or not users:  # Check if shops and users exist
            self.stdout.write(self.style.WARNING("No shops or users found. Populate them first."))
            return

        unique_pairs = set()
        for _ in range(min(30, len(shops) * len(users))):  # Limit to avoid duplicates
            shop = random.choice(shops)
            user = random.choice(users)
            
            if (shop.id, user.id) in unique_pairs:  # Ensure unique shop-user pairs
                continue
            
            unique_pairs.add((shop.id, user.id))
            review = random.choice(reviews)
            
            Rating.objects.create(shop=shop, user=user, review=review, rating=random.randint(1, 5))

        self.stdout.write(self.style.SUCCESS("Successfully inserted ratings."))
