from django.db import models
from django.contrib.auth.models import User
import uuid 
from django.utils.text import slugify



class District(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    
class Vegetables(models.Model):
    vegetable = models.CharField(max_length=50)
    images = models.ImageField(null=True,upload_to="vegetables/")

    def __str__(self):
        return self.vegetable


class Shop(models.Model):
    shop_owner = models.ForeignKey(User,on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True,max_length=5)
    image = models.ImageField(null=True,upload_to='shop/',max_length=300)
    slug = models.SlugField(unique=True,max_length=100)
    is_available = models.BooleanField(default=False)
    vegetables = models.ForeignKey(Vegetables,on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name
    
    @property
    def formeted_image(self):

        if self.image.__str__().startswith(('http://','https://')):
            url = self.image
        else:
            url = self.image.url
            
        return url

    def save(self,*args, **kwargs):
        slug = self.shop_name + self.shop_owner.username
        self.slug = slugify(slug)
        super().save(*args, **kwargs)
    

class temp_user(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.TextField()
    contact_number = models.CharField(max_length=10)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

class Product(models.Model):
    price_per_kg = models.FloatField()
    shop_name = models.ForeignKey(Shop,on_delete=models.CASCADE)
    category = models.ForeignKey(Vegetables,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    description = models.TextField(null=False)
    image = models.ImageField(null=True,max_length=300)
    is_available = models.BooleanField(default=True)

    def save(self,*args, **kwargs):
        self.is_available = self.quantity > 0
        if not self.image:
            self.image = self.category.images  
        super().save(*args, **kwargs)
    
    @property
    def formeted_image(self):

        if self.image.__str__().startswith(('http://','https://')):
            url = self.image
        else:
            url = self.image.url
            
        return url
    
    def __str__(self):
        return f"{self.category.vegetables} - {self.prize_per_kg}"
    
class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    
    def __str__(self):
        return self.user.username

    




