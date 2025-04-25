from django.core.paginator import Paginator
from .models import Product
from django.db.models import Q

def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()


    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(country__icontains=query) |
            Q(year__icontains=query)
        )

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/list.html', {'page_obj': page_obj})


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'products/detail.html', {'product': product})