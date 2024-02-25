from rest_framework import serializers

from products.models import StoreInventory


class StoreInventorySerializer(serializers.ModelSerializer):
    inventory_id = serializers.IntegerField()
    quantity = serializers.FloatField()

    class Meta:
        model = StoreInventory
        fields = ['inventory_id', 'quantity']