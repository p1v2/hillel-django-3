from rest_framework import serializers

from products.models import StoreInventory


class StoreInventorySerializer(serializers.ModelSerializer):
    store_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.FloatField()

    class Meta:
        model = StoreInventory
        fields = ['store_id', 'product_id', 'quantity']