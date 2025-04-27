from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order
from products.models import Product
from decimal import Decimal

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
        total_price = product.price * Decimal(quantity)
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        product.inventory -= quantity
        product.save()
        messages.success(request, "Order created successfully!")
    return redirect('order_list')

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Paid'
        order.save()
        messages.success(request, f"Order #{order.id} has been paid successfully!")
    else:
        messages.error(request, f"Order #{order.id} cannot be paid. Current status: {order.status}.")
    return redirect('order_list')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status in ['Pending', 'Paid']:
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled successfully!")
    else:
        messages.error(request, f"Order #{order.id} cannot be cancelled. Current status: {order.status}.")
    return redirect('order_list')

@login_required
def pay_selected_orders(request):
    if request.method == 'POST':
        selected_orders = request.POST.getlist('selected_orders')
        if not selected_orders:
            messages.error(request, "No orders selected.")
            return redirect('order_list')
        orders = Order.objects.filter(id__in=selected_orders, user=request.user)
        paid_count = 0
        for order in orders:
            if order.status == 'Pending':
                order.status = 'Paid'
                order.save()
                paid_count += 1
        messages.success(request, f"{paid_count} order(s) paid successfully!")
    return redirect('order_list')