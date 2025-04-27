from django.urls import path
from products.views import product_list, product_detail
from orders.views import order_list, pay_order, pay_selected_orders, cancel_order, admin_dashboard

urlpatterns = [
    path('', product_list, name='product_list'),
    path('products/<int:product_id>/', product_detail, name='product_detail'),
    path('products/<int:product_id>/create_order/', pay_order, name='create_order'),
    path('orders/', order_list, name='order_list'),
    path('orders/<int:order_id>/pay/', pay_order, name='pay_order'),
    path('orders/pay_selected/', pay_selected_orders, name='pay_selected_orders'),
    path('orders/<int:order_id>/cancel/', cancel_order, name='cancel_order'),
    path('admin/dashboard/', admin_dashboard, name='admin_dashboard'),
]