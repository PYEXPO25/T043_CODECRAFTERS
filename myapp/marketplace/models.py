from django.db import models

class District(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Shop(models.Model):
    shop_name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name

class ShopImage(models.Model):  # Renamed ShopImages → ShopImage (singular)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="images")
    image_url = models.URLField(null=False)

    def __str__(self):
        return f"Image for {self.shop.shop_name}"



