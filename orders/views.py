from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from products.models import Product

def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = []
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def create_order(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        if quantity > product.inventory:
            messages.error(request, "Not enough inventory available.")
            return redirect('product_list')
        total_price = product.price * quantity
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        product.inventory -= quantity
        product.save()
        messages.success(request, "Order created successfully!")
    return redirect('order_list')