from django.db import models
from products.models import Product


class Store(models.Model):
    name = models.CharField(max_length=120)
    address = models.TextField()
    description = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    products = models.ManyToManyField(Product, through='StoreInventory')


    # ActiveRecord
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.address}"

