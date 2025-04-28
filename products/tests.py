from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product
from orders.models import Order

class ProductTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.product1 = Product.objects.create(
            name="Test Wine 1",
            price=20.00,
            country="France",
            region="Bordeaux",
            winery="Test Winery",
            inventory=100
        )
        self.product2 = Product.objects.create(
            name="Test Wine 2",
            price=30.00,
            country="Italy",
            region="Tuscany",
            winery="Test Winery 2",
            inventory=50
        )

    def test_product_model(self):
        product = Product.objects.get(id=self.product1.id)
        self.assertEqual(product.name, "Test Wine 1")
        self.assertEqual(product.price, 20.00)
        self.assertEqual(product.country, "France")
        self.assertEqual(product.inventory, 100)

    def test_product_list_view(self):
        response = self.client.get(reverse('products:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Wine 1")
        self.assertContains(response, "Test Wine 2")

    def test_product_list_search(self):
        response = self.client.get(reverse('products:product_list'), {'search': 'France'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Wine 1")
        self.assertNotContains(response, "Test Wine 2")

    def test_product_detail_view(self):
        response = self.client.get(reverse('products:product_detail', args=[self.product1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Wine 1")
        self.assertContains(response, "France")

    def test_product_detail_invalid_id(self):
        response = self.client.get(reverse('products:product_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_compare_products_view(self):
        session = self.client.session
        session['compare_list'] = [self.product1.id, self.product2.id]
        session.save()

        response = self.client.get(reverse('products:compare_products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Wine 1")
        self.assertContains(response, "Test Wine 2")

    def test_compare_products_remove(self):
        session = self.client.session
        session['compare_list'] = [self.product1.id, self.product2.id]
        session.save()

        response = self.client.post(reverse('products:compare_products'), {
            'remove_product': self.product1.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Test Wine 1")
        self.assertContains(response, "Test Wine 2")

    def test_add_to_compare(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('products:product_list'), {
            'action': 'toggle_compare',
            'compare_product': self.product1.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product1.id, self.client.session.get('compare_list', []))