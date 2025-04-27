from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Product
import random

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product_list.html', {'page_obj': page_obj})
