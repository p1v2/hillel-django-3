from django.contrib import admin

from products.models import Product, Category, Recipe, Order, OrderProduct
from products.models import Store, StoreInventory

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Recipe)
admin.site.register(Order)
admin.site.register(OrderProduct)
# register new models
@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_number', 'email', 'created_at', 'updated_at')
    search_fields = ('name', 'address')

@admin.register(StoreInventory)
class StoreInventoryAdmin(admin.ModelAdmin):
    list_display = ('store', 'product', 'quantity', 'price', 'updated_at')
    search_fields = ('store__name', 'product__name')