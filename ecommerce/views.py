from django.shortcuts import render
from products.models import Product
import random

def home(request):
    # 获取所有商品
    all_products = Product.objects.all()
    # 随机选择 10 个商品（如果总数少于 10 个，则返回所有商品）
    recommended_products = random.sample(list(all_products), min(10, len(all_products)))
    return render(request, 'index.html', {'recommended_products': recommended_products})