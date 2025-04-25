from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def order_list(request):
    return render(request, 'orders/list.html')

def order_create(request):
    return render(request, 'orders/create.html')

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    Cart.objects.create(user=request.user, product=product)
    return redirect('product_list')