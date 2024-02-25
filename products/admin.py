from django.contrib import admin

from products.models import Product, Category, Recipe, Order, OrderProduct, StoreInventory, Store

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(StoreInventory)
admin.site.register(Store)