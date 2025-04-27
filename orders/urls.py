from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/<int:product_id>/', views.create_order, name='create_order'),
]