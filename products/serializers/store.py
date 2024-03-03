from rest_framework import serializers
from products.models import Store
from products.serializers.store_inventory import StoreInventorySerializer


class StoreSerializer(serializers.ModelSerializer):
    store_product_list = StoreInventorySerializer(many=True)

    class Meta:
        model = Store
        fields = ['name', 'address', 'description', 'phone_number', 'email', 'website', 'store_product_list']


