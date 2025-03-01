from marketplace.models import Vegetable
from typing import Any
from django.core.management.base import BaseCommand
class Command(BaseCommand):

    def handle(self, *args, **options):
        Vegetable.objects.all().delete()
        vegetables = [
    "Potato", "Okra", "Brinjal", "Carrot", "Cauliflower", "Bottle Gourd",
    "Ridge Gourd", "Turnip", "Radish", "Tomato", "Bell Pepper", "Beetroot",
    "Ginger", "Garlic", "Onion", "Raw Mango", "Ash Gourd", "Taro Root",
    "Pumpkin", "Chickpea", "Coriander Leaves", "Black Cumin", "Chickpea Leaves",
    "Leafy Greens", "Fennel", "Drumstick", "Indian Spinach", "Kidney Beans",
    "Corn", "Indian Cucumber", "Indian Berry", "Cucumber-like Vegetable",
    "Dried Fenugreek Leaves", "Cluster Beans", "Raw Banana",
    "Bitter Gourd-like Vegetable", "Fenugreek Seeds"
]

        vegetable_images = [
    "vegetables/potato.jpeg", "vegetables/okra.jpeg", "vegetables/brinjal.jpeg",
    "vegetables/carrot.jpeg", "vegetables/cauliflower.jpg", "vegetables/Bottle-gourd-.jpg",
    "vegetables/ridge_gourd.webp", "vegetables/turnip.jpg", "vegetables/radish.jpeg",
    "vegetables/tomato.webp", "vegetables/bell_pepper.jpeg", "vegetables/beetroot.jpeg",
    "vegetables/ginger.jpg", "vegetables/garlic.jpg", "vegetables/onion.jpeg",
    "vegetables/raw_mango.jpeg", "vegetables/ash_gourd.jpeg", "vegetables/taro_root.jpg",
    "vegetables/pumpkins.jpg", "vegetables/chickpea.jpeg", "vegetables/coriander_leaves_zWMZP6c.jpeg",
    "vegetables/cumin-seeds.webp", "vegetables/chickpea_leaves_zoW6sMG.jpg", "vegetables/green_vegetables.jpeg",
    "vegetables/Fennel.jpg", "vegetables/Drumstick.jpg", "vegetables/spinach.jpeg",
    "vegetables/kidney_beans.jpg", "vegetables/corn.webp", "vegetables/indian_cucumber.jpg",
    "vegetables/indian_berry.webp", "vegetables/cucumbers.jpg", "vegetables/Dried-Fenugreek-Leaves.jpg",
    "vegetables/clustter_beans.jpg", "vegetables/raw_banana.jpg", "vegetables/Bitter_gourd.jpeg",
    "vegetables/Fengureek_seeds.webp"
]
        lifespans = [
    30, 4, 4, 7, 5, 10, 7, 5, 4, 7, 7, 7, 14, 30, 30, 5, 20, 7,  
    20, 60, 3, 180, 3, 3, 180, 5, 3, 30, 10, 3, 3, 90, 5, 3, 3, 365  
]

        for vegetable,image,lifespan in zip(vegetables,vegetable_images,lifespans):
            Vegetable.objects.create(name = vegetable,default_image = image,lifespan=lifespan)
            
        self.stdout.write(self.style.SUCCESS("Successfully insereted."))