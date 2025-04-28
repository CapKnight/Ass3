from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Order
from products.models import Product

class OrderTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.admin = User.objects.create_user(
            username='admin',
            password='adminpass123',
            is_staff=True
        )
        
        self.product = Product.objects.create(
            name="Test Wine",
            price=20.00,
            country="France",
            region="Bordeaux",
            winery="Test Winery",
            inventory=100
        )
        
        self.order = Order.objects.create(
            user=self.user,
            product=self.product,
            quantity=2,
            total_price=40.00,
            status='Pending'
        )

    def test_order_model(self):
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.product, self.product)
        self.assertEqual(order.quantity, 2)
        self.assertEqual(order.total_price, 40.00)
        self.assertEqual(order.status, 'Pending')

    def test_order_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Wine")

    def test_order_list_unauthenticated(self):
        response = self.client.get(reverse('orders:order_list'))
        self.assertEqual(response.status_code, 302)

    def test_create_order(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('orders:create_order', args=[self.product.id]), {
            'quantity': 3
        })
        self.assertEqual(response.status_code, 302)
        order = Order.objects.last()
        self.assertEqual(order.quantity, 3)
        self.assertEqual(order.total_price, 60.00)
        self.assertEqual(order.status, 'Pending')
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.inventory, 97)

    def test_pay_order(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:pay_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.status, 'Paid')

    def test_cancel_order(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:cancel_order', args=[self.order.id]))
        self.assertEqual(response.status_code, 302)
        order = Order.objects.get(id=self.order.id)
        self.assertEqual(order.status, 'Cancelled')
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.inventory, 102)

    def test_admin_dashboard_access(self):
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get(reverse('orders:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin Dashboard")

    def test_admin_dashboard_unauthorized(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('orders:admin_dashboard'))
        self.assertEqual(response.status_code, 302)