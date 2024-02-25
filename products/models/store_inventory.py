from django.db import models
from .product import Product


class StoreInventory(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='store_inventory')
    # inventory = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='store_inventory')

    inventory = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)

    class Meta:
        verbose_name_plural = "Store Inventories"
    def amount(self):
        return float(self.inventory.price) * self.quantity


    def __str__(self):
        return f"{self.quantity} of {self.inventory.title}"
