from django.db import models
import uuid 



class District(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Rating(models.Model):
    rating = models.IntegerField(max_length=5)
    def __str__(self):
        return self.rating


class ShopImage(models.Model):  
    image = models.ImageField(null=False,upload_to='shop/')

class Shop(models.Model):
    shop_name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    rating = models.ForeignKey(Rating,on_delete=models.CASCADE)
    image = models.ForeignKey(ShopImage, on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name


    
    
class Vegetables(models.Model):
    vegetable = models.CharField(max_length=50)
    images = models.ImageField(null=True,upload_to="vegetables/")

    def __str__(self):
        return self.vegetable

class temp_user(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.TextField()
    contact_number = models.CharField(max_length=10)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

class Product(models.Model):
    prize_per_kg = models.FloatField()
    shop_name = models.ForeignKey(Shop,on_delete=models.CASCADE)
    category = models.ForeignKey(Vegetables,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=False)
    

    def __str__(self):
        return f"{self.category.vegetables} - {self.prize_per_kg}"

    




