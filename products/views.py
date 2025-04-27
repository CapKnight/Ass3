from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product

def product_list(request):
    # 获取所有商品
    products = Product.objects.all()

    # 获取筛选参数
    country = request.GET.get('country', '')
    region = request.GET.get('region', '')
    winery = request.GET.get('winery', '')

    # 应用筛选
    if country:
        products = products.filter(country=country)
    if region:
        products = products.filter(region=region)
    if winery:
        products = products.filter(winery=winery)

    # 获取搜索关键字
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(region__icontains=search_query) |
            Q(winery__icontains=search_query)
        )

    # 获取价格范围
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        try:
            min_price = float(min_price)
            products = products.filter(price__gte=min_price)
        except ValueError:
            min_price = ''
    if max_price:
        try:
            max_price = float(max_price)
            products = products.filter(price__lte=max_price)
        except ValueError:
            max_price = ''

    # 获取排序参数
    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

    # 获取筛选选项（增强去重逻辑）
    countries = sorted(set(
        product.country.strip().capitalize()
        for product in Product.objects.all()
        if product.country
    ))
    regions = sorted(set(
        product.region.strip().capitalize()
        for product in Product.objects.all()
        if product.region
    ))
    wineries = sorted(set(
        product.winery.strip().capitalize()
        for product in Product.objects.all()
        if product.winery
    ))

    # 分页
    paginator = Paginator(products, 10)  # 每页显示 10 个商品
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    # 传递上下文
    context = {
        'products': products_page,
        'countries': countries,
        'regions': regions,
        'wineries': wineries,
        'selected_country': country,
        'selected_region': region,
        'selected_winery': winery,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'product_list.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})