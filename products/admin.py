from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['country', 'region', 'winery', 'rating', 'price', 'year', 'inventory']
    search_fields = ['name']
