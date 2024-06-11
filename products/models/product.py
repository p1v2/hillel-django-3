from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    summary = models.TextField(blank=False, null=False)
    featured = models.BooleanField(default=False)
    is_18_plus = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True, related_name='products')
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')
    orders = models.ManyToManyField('Order', through='OrderProduct')
    stores = models.ManyToManyField('Store', through='StoreInventory', related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.price}"
