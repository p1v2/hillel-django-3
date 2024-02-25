from django.db import models
from .product import Product
from .store_inventory import StoreInventory

class Store(models.Model):
    name = models.CharField(max_length=120)
    country = models.CharField(max_length=120)
    city = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    square = models.DecimalField(max_digits=10, decimal_places=2)
    employees_num = models.IntegerField()
    notes = models.TextField(blank=True, null=True)
    opened_date = models.DateField(blank=False, null=False)
    
    inventory = models.ManyToManyField(Product, through='StoreInventory', related_name='stores')
    #stock = models.ManyToManyField(StoreInventory, through='StoreInventory')

    def inventory_amount(self):
        total_amount = 0
        for store_inventory in self.store_inventory.all():
            total_amount += store_inventory.amount()
        return total_amount

    class Meta:
        verbose_name_plural = "Stores"
