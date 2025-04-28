from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
import json
from products.models import Product
from django.utils import timezone
from datetime import timedelta

def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def create_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=product.price * quantity,
            status='Pending'
        )
        product.inventory -= quantity
        product.save()
        return redirect('orders:order_list')
    return redirect('products:product_detail', product_id=product.id)

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status == 'Pending':
        order.status = 'Paid'
        order.save()
    return redirect('orders:order_list')

@login_required
def pay_selected_orders(request):
    if request.method == 'POST':
        selected_orders = request.POST.getlist('selected_orders')
        if not selected_orders:
            messages.error(request, "No orders selected for payment.")
            return redirect('orders:order_list')
        
        orders = Order.objects.filter(id__in=selected_orders, user=request.user)
        paid_count = 0
        for order in orders:
            if order.status == 'Pending':
                order.status = 'Paid'
                order.save()
                paid_count += 1
            else:
                messages.warning(request, f"Order #{order.id} cannot be paid. Current status: {order.status}.")
        
        if paid_count > 0:
            messages.success(request, f"{paid_count} order(s) paid successfully!")
        return redirect('orders:order_list')
    return redirect('orders:order_list')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status not in ['Pending', 'Paid']:
        messages.error(request, f"Order #{order.id} cannot be cancelled. Current status: {order.status}.")
    else:
        product = order.product
        product.inventory += order.quantity
        product.save()
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled successfully!")
    return redirect('orders:order_list')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue = sum(order.total_price for order in Order.objects.all())
    status_counts = {
        'Pending': Order.objects.filter(status='Pending').count(),
        'Paid': Order.objects.filter(status='Paid').count(),
        'Cancelled': Order.objects.filter(status='Cancelled').count(),
    }

    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)
    date_range = [start_date + timedelta(days=x) for x in range(7)]
    orders_by_date = [
        Order.objects.filter(order_date__date=date).count()
        for date in date_range
    ]
    date_labels = [date.strftime('%Y-%m-%d') for date in date_range]
    
    context = {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'status_counts': status_counts,
        'date_labels': json.dumps(date_labels),
        'orders_by_date': json.dumps(orders_by_date),
    }
    return render(request, 'admin_dashboard.html', context)