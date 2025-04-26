from django.shortcuts import render
from .models import Order

def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = []
    return render(request, 'list.html', {'orders': orders})