from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Order
from products.models import Product

# 检查用户是否为管理员
def is_admin(user):
    return user.is_authenticated and user.is_staff

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-order_date')
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def pay_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'Pending':
        messages.error(request, f"Order #{order.id} cannot be paid. Current status: {order.status}.")
    else:
        order.status = 'Paid'
        order.save()
        messages.success(request, f"Order #{order.id} has been paid successfully!")
    return redirect('order_list')

@login_required
def pay_selected_orders(request):
    if request.method == 'POST':
        selected_orders = request.POST.getlist('selected_orders')
        if not selected_orders:
            messages.error(request, "No orders selected for payment.")
            return redirect('order_list')
        
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
        return redirect('order_list')
    return redirect('order_list')

@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status not in ['Pending', 'Paid']:
        messages.error(request, f"Order #{order.id} cannot be cancelled. Current status: {order.status}.")
    else:
        # 恢复库存
        product = order.product
        product.inventory += order.quantity
        product.save()
        order.status = 'Cancelled'
        order.save()
        messages.success(request, f"Order #{order.id} has been cancelled successfully!")
    return redirect('order_list')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    # 订单统计
    total_orders = Order.objects.count()
    total_revenue = sum(order.total_price for order in Order.objects.all())
    status_counts = {
        'Pending': Order.objects.filter(status='Pending').count(),
        'Paid': Order.objects.filter(status='Paid').count(),
        'Cancelled': Order.objects.filter(status='Cancelled').count(),
    }

    # 按日期统计订单（最近 7 天）
    from django.utils import timezone
    from datetime import timedelta
    import json
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=6)  # 最近 7 天
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
        'date_labels': json.dumps(date_labels),  # 转为 JSON 供 Chart.js 使用
        'orders_by_date': json.dumps(orders_by_date),
    }
    return render(request, 'admin_dashboard.html', context)