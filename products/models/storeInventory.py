from django.db import models

from products.models import Product
from products.models import Store


class StoreInventory(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_inventorys')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='store_inventorys')
    quantity = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store.name} have {self.quantity} of {self.product.title}"

    @property
    def price(self):
        return float(self.product.price) * self.quantity
