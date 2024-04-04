# Create your models here.
import time

from django.core.cache import cache
from django.db import models

from products.models.tag import Tag
from products.models.category import Category


class Product(models.Model):
    title = models.CharField(max_length=120)  # max_length = required
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)  # null=True, default=True
    is_18_plus = models.BooleanField(default=False)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='products')
    tags = models.ManyToManyField(Tag, blank=True, related_name='products')

    orders = models.ManyToManyField('Order', through='OrderProduct')

    # ActiveRecord
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def additional_metadata(self):
        cache_key = f"product_supplier_data_{self.id}"

        cached_data = cache.get(cache_key)

        if cached_data:
            return cached_data

        time.sleep(1)
        supplier_data = {
            "storage_type": "fridge",
            "allegriens": [],
        }

        cache.set(f"product_supplier_data_{self.id}", supplier_data, 60 * 60 * 24)
        return supplier_data

    def __str__(self):
        return f"{self.title} - {self.price}"
