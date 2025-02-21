from marketplace.models import Vegetables
from typing import Any
from django.core.management.base import BaseCommand
class Command(BaseCommand):

    def handle(self, *args, **options):
        Vegetables.objects.all().delete()
        vegetables = [
    "Potato",
    "Okra",
    "Brinjal",
    "Carrot",
    "Cauliflower",
    "Bottle Gourd",
    "Ridge Gourd",
    "Bitter Gourd",
    "Fenugreek",
    "Spinach",
    "Mustard Greens",
    "Turnip",
    "Radish",
    "Tomato",
    "Bell Pepper",
    "Apple Gourd",
    "Beetroot",
    "Ginger",
    "Garlic",
    "Onion",
    "Raw Mango",
    "Ash Gourd",
    "Carandas",
    "Taro Root",
    "Pumpkin",
    "Chickpea",
    "Coriander Leaves",
    "Green Chickpeas",
    "Black Cumin",
    "Potato Fenugreek Leaves",
    "Chickpea Leaves",
    "Leafy Greens",
    "Fennel",
    "Drumstick",
    "Indian Spinach",
    "Kidney Beans",
    "Corn",
    "Indian Cucumber",
    "Indian Berry",
    "Cucumber-like Vegetable",
    "Dried Fenugreek Leaves",
    "Cluster Beans",
    "Raw Banana",
    "Bitter Gourd-like Vegetable",
    "Fenugreek Seeds"
]
        for vegetable in vegetables:
            Vegetables.objects.create(vegetable = vegetable)
            
        self.stdout.write(self.style.SUCCESS("Successfully insereted."))