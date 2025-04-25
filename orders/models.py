from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 关联用户
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 关联商品
    quantity = models.IntegerField(default=1)       # 购买数量
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # 总价
    created_at = models.DateTimeField(auto_now_add=True)  # 下单时间
    status_choices = [
        ('pending', '待支付'),
        ('completed', '已完成'),
    ]
    status = models.CharField(max_length=20, choices=status_choices, default='pending')

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)