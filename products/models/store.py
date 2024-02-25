from django.db import models

from products.models import Product


class Store(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    is_open = models.BooleanField(default=True)

    products = models.ManyToManyField(Product, through='StoreInventory')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.address} - {self.description} - {self.is_open} - {self.name}"

