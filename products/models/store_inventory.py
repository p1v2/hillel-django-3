"""
Create the StoreInventory Model:
Establish a Many-to-Many relationship between Store and Product using a model named StoreInventory.
This intermediary model should track the inventory of products in each store,
including fields for quantity, price, or any other relevant inventory details.
"""
from django.db import models


class StoreInventory(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='store_inventory')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='store_inventory')
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.store.name} - {self.product.title} - {self.quantity}"
