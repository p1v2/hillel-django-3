# from django.test import TestCase
#
# from products.models import Product
#
#
# # Create your tests here.
# class ProductTestCase(TestCase):
#     def test_str(self):
#         product = Product.objects.create(title='A product', price=40, summary='A summary')
#
#         self.assertEqual(str(product), 'A product - 40')
#
#
import redis

rs = redis.Redis("localhost")

try:
    response = rs.ping()
    print("Redis server is running: ", response)
except redis.ConnectionError:
    print("Redis server is not running")
