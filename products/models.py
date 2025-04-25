from django.db import models

class Product(models.Model):
    # 原有字段
    name = models.CharField(max_length=200)

    country = models.CharField(max_length=100, blank=True)      # Country
    region = models.CharField(max_length=100, blank=True)       # Region
    winery = models.CharField(max_length=100, blank=True)       # Winery
    rating = models.FloatField(default=0.0)                     # Rating
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField(null=True, blank=True)           # Year（允许为空）
    inventory = models.IntegerField(default=0)                  # Inventory

    def __str__(self):
        return self.name