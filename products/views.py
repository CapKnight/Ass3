from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Product

def product_list(request):
    if request.method == 'POST' and request.POST.get('action') == 'toggle_compare':
        product_id = int(request.POST.get('compare_product'))
        compare_list = request.session.get('compare_list', [])
        if product_id in compare_list:
            compare_list.remove(product_id)
        else:
            if len(compare_list) < 4:
                compare_list.append(product_id)
            else:
                pass
        request.session['compare_list'] = compare_list
        request.session.modified = True

    products = Product.objects.all()

    country = request.GET.get('country', '')
    region = request.GET.get('region', '')
    winery = request.GET.get('winery', '')

    if country:
        products = products.filter(country=country)
    if region:
        products = products.filter(region=region)
    if winery:
        products = products.filter(winery=winery)

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(country__icontains=search_query) |
            Q(region__icontains=search_query) |
            Q(winery__icontains=search_query)
        )

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

    sort = request.GET.get('sort', '')
    if sort == 'price_asc':
        products = products.order_by('price')
    elif sort == 'price_desc':
        products = products.order_by('-price')

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

    paginator = Paginator(products, 50)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

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
    if request.method == 'POST' and request.POST.get('action') == 'toggle_compare':
        product_id = int(request.POST.get('compare_product'))
        compare_list = request.session.get('compare_list', [])
        if product_id in compare_list:
            compare_list.remove(product_id)
        else:
            if len(compare_list) < 4:
                compare_list.append(product_id)
            else:
                print("Limitation: 4")
                pass
        request.session['compare_list'] = compare_list
        request.session.modified = True

    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def compare_products(request):
    compare_list = request.session.get('compare_list', [])

    if request.method == 'POST':
        product_id_to_remove = request.POST.get('remove_product')
        if product_id_to_remove:
            product_id_to_remove = int(product_id_to_remove)
            if product_id_to_remove in compare_list:
                compare_list.remove(product_id_to_remove)
                request.session['compare_list'] = compare_list
                request.session.modified = True

    products = Product.objects.filter(id__in=compare_list)

    context = {
        'products': products,
    }
    return render(request, 'compare.html', {'products': products})