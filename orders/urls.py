from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:order_id>/pay/', views.pay_order, name='pay_order'),
    path('pay_selected/', views.pay_selected_orders, name='pay_selected_orders'),
    path('<int:order_id>/cancel/', views.cancel_order, name='cancel_order'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create/<int:product_id>/', views.create_order, name='create_order'),
]