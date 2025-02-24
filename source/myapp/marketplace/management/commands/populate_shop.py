from marketplace.models import Shop
from typing import Any
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from marketplace.models import District,Vegetable
import random
class Command(BaseCommand):

    def handle(self, *args, **options):
        Shop.objects.all().delete()
        shops = [
    "Fresh Harvest",
    "Green Basket",
    "Nature’s Bounty",
    "Organic Haven",
    "The Veggie Spot",
    "Fruit Fiesta",
    "Farm Fresh",
    "Crisp & Juicy",
    "Purely Natural",
    "Bloom Grocers",
    "Garden Goodies",
    "Roots & Shoots",
    "Sunny Orchard",
    "Berry Bliss",
    "Citrus Delights",
    "Tropical Treats",
    "Healthy Harvest",
    "The Green Cart",
    "Nutri Picks",
    "Farm to Fork"
]
        # images = ["https://images.stockcake.com/public/7/b/2/7b208ddd-1125-4d86-b25b-87b124f03469_large/rural-farm-landscape-stockcake.jpg","https://images.pexels.com/photos/96715/pexels-photo-96715.jpeg?cs=srgb&dl=pexels-alejandro-barron-21404-96715.jpg&fm=jpg","https://cdn.sanity.io/images/ec9j7ju7/production/f6f10b735cf1c9c7bb494d56af0af099dfd823a5-3884x2594.jpg?w=3840&q=75&fit=clip&auto=format"]
        shop_owners = User.objects.all()
        districts = District.objects.all()
        for shop in shops:
            shop_owner = random.choice(shop_owners)
            district = random.choice(districts)
            # vegetable = random.choice(vegetables)
            Shop.objects.create(shop_owner=shop_owner,district=district,name=shop)

        self.stdout.write(self.style.SUCCESS("Successfully insereted."))