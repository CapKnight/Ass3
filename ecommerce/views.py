from django.shortcuts import render
from products.models import Product
import random

def home(request):
    all_products = Product.objects.all()
    recommended_products = random.sample(list(all_products), min(10, len(all_products)))
    return render(request, 'index.html', {'recommended_products': recommended_products})