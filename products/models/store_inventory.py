from django.db import models
from django.core.validators import MinValueValidator


class StoreInventory(models.Model):
    store = models.ForeignKey('Store', on_delete=models.CASCADE, related_name='store_product_list')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='store_product_list')
    quantity = models.FloatField(default=0, validators=[MinValueValidator(0)])

    # ActiveRecord
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.store.name} - {self.product.title} - Quantity: {self.quantity}"

    @property
    def price(self):
        return float(self.product.price) * self.quantity
