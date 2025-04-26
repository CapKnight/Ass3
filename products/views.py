from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Product

def product_list(request):
    products = Product.objects.all()
    paginator = Paginator(products, 50)  # 每页显示 50 个商品
    page_number = request.GET.get('page')  # 从 URL 参数中获取页码
    page_obj = paginator.get_page(page_number)  # 获取当前页的数据
    return render(request, 'list.html', {'page_obj': page_obj})