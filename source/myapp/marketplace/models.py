from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import random


class District(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Vegetable(models.Model):
    name = models.CharField(max_length=50, unique=True)
    default_image = models.ImageField(upload_to="vegetables/defaults/", null=True, blank=True)

    def __str__(self):
        return self.name


class VegetableImage(models.Model):
    vegetable = models.ForeignKey(Vegetable, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="vegetables/")

    def __str__(self):
        return f"{self.vegetable.name} Image"


class Shop(models.Model):
    shop_owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, max_length=100, blank=True)
    # vegetables = models.ManyToManyField(Vegetable, related_name="shops")
    average_rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to="shop/image/",max_length=500)  
    total_ratings = models.PositiveIntegerField(default=0)  
    shop_description = models.TextField(null=True)
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        images = ["https://images.stockcake.com/public/7/b/2/7b208ddd-1125-4d86-b25b-87b124f03469_large/rural-farm-landscape-stockcake.jpg",
                  "https://images.pexels.com/photos/96715/pexels-photo-96715.jpeg?cs=srgb&dl=pexels-alejandro-barron-21404-96715.jpg&fm=jpg",
                  "https://cdn.sanity.io/images/ec9j7ju7/production/f6f10b735cf1c9c7bb494d56af0af099dfd823a5-3884x2594.jpg?w=3840&q=75&fit=clip&auto=format",
                  "https://cdn.pixabay.com/photo/2017/05/19/15/16/countryside-2326787_1280.jpg",
                  "https://www.nifa.usda.gov/sites/default/files/styles/hero_image_small_1024w/public/2023-03/farm-business-rfa.jpg?itok=zN6Xpx7N"]

        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.shop_owner.username}")

        if not self.image:
            self.image = random.choice(images)

        if not self.shop_description:
          self.description = "A farm shop offering fresh, locally sourced produce, dairy, and homemade goods straight from the farm. Enjoy organic fruits, vegetables, and artisanal products while supporting local farmers and sustainable practices."

        super().save(*args, **kwargs)

        
    @property
    def formated_image(self):

        if self.image.__str__().startswith(('http://','https://')):
            url = self.image
        else:
            url = self.image.url
            
        return url

    @property
    def has_products(self):
        return self.products.filter(quantity__gt=0).exists()

    def update_rating(self):
        ratings = self.ratings.all()
        total_ratings = ratings.count()
        average_rating = ratings.aggregate(models.Avg("rating"))["rating__avg"] or 0.0

        self.total_ratings = total_ratings
        self.average_rating = round(average_rating, 2)
        self.save(update_fields=["total_ratings", "average_rating"])


# class ShopImage(models.Model):
#     shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="images")
#     image = models.ImageField(upload_to="shop/")

#     @property
#     def formated_image(self):

#         if self.image.__str__().startswith(('http://','https://')):
#             url = self.image
#         else:
#             url = self.image.url
            
#         return url


#     def __str__(self):
#         return f"{self.shop.name} Image"


class Rating(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="ratings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("shop", "user")  

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.shop.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.shop.update_rating()


class TempUser(models.Model):
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=10)
    token = models.UUIDField(default=uuid.uuid4, unique=True)

    def __str__(self):
        return self.username


class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="products")
    category = models.ForeignKey(Vegetable, on_delete=models.CASCADE)
    price_per_kg = models.FloatField(validators=[MinValueValidator(0.1)])
    quantity = models.PositiveIntegerField(null=False)
    description = models.TextField()
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    slug = models.SlugField(max_length=100)
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = self.category.default_image 

        if not self.description:
            self.description = f"Buy this Fresh and high-quality {self.category} at {self.shop}."

        if not self.slug:
            self.slug = slugify(self.shop.name+self.shop.shop_owner.username+self.category.name)
        super().save(*args, **kwargs)

        

    @property
    def formated_image(self):

        if self.image.__str__().startswith(('http://','https://')):
            url = self.image
        else:
            url = self.image.url
            
        return url
    
    def product_name(self):
        name = self.category.name + self.shop.name

        return name

    def __str__(self):
        return f"{self.category.name} - {self.price_per_kg}"


class Farmer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username
