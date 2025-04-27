from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/<int:product_id>/', views.create_order, name='create_order'),
    path('pay/<int:order_id>/', views.pay_order, name='pay_order'),
    path('cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('pay-selected/', views.pay_selected_orders, name='pay_selected_orders'),
]