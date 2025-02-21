from django.db import models


class District(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class ShopImages(models.Model):
    image_1 = models.URLField(null=False)
    image_2 = models.URLField(null=False)
    image_3 = models.URLField(null=False)
    image_4 = models.URLField(null=False)
    image_5 = models.URLField(null=False)

# Create your models here.
class Shop(models.Model):
    shop_name = models.CharField(max_length = 50)
    district = models.ForeignKey(District,on_delete=models.CASCADE)
    images = models.ForeignKey(ShopImages,on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name





