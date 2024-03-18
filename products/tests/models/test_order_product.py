from django.contrib.auth.models import User
from django.test import TestCase

from products.models import Product, Order


# Create your tests here.
class ProductTestCase(TestCase):
    def test_str(self):
        product = Product.objects.create(title='A product', price=40, summary='A summary')

        self.assertEqual(str(product), 'A product - 40')


class OrderProductTestCase(TestCase):
    def test_price(self):
        product = Product.objects.create(title='A product', price=40.1, summary='A summary')
        order = Order.objects.create(user=User.objects.create(username='test'))

        order_product = product.order_products.create(quantity=2, order=order)

        self.assertEqual(order_product.price, 80.2)