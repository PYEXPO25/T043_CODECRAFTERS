from django.contrib import admin
from .models import Product,District,Vegetables,Shop
# Register your models here.

admin.site.register(Product)
admin.site.register(District)
admin.site.register(Shop)
admin.site.register(Vegetables)

