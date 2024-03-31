from django.db import models

# from products.models import Order


class OrderProduct(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='order_products')
    quantity = models.FloatField(default=1)

    @property
    def price(self):
        return float(self.product.price) * self.quantity

    def __str__(self):
        # products_list = [str(product) for product in self.order.order_products.all()]
        return f"{self.order} "
