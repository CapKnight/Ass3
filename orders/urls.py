from django.urls import path
from . import views  # 确保views.py存在且有相应视图函数

urlpatterns = [
    # 示例URL模式
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
]