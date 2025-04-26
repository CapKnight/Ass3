from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    region = models.CharField(max_length=50)
    winery = models.CharField(max_length=100)
    rating = models.FloatField()
    number_of_ratings = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    year = models.IntegerField(null=True, blank=True)
    inventory = models.IntegerField(default=100)  # 默认库存

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']