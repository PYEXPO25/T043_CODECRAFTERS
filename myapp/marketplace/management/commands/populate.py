from marketplace.models import Vegetables
from typing import Any
from django.core.management.base import BaseCommand
class Command(BaseCommand):

    def handle(self, *args, **options):
        Vegetables.objects.all().delete()
        vegetables = ["Tomato","Potato","Carrot","Pumpkin","Brinjal"]
        for vegetable in vegetables:
            Vegetables.objects.create(vegetable = vegetable)

        self.stdout.write(self.style.SUCCESS("Successfully insereted."))