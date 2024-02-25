from rest_framework import serializers

from products.models import StoreInventory


class StoreInventorySerializer(serializers.ModelSerializer):
    inventory_id = serializers.IntegerField()
    quantity = serializers.FloatField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = StoreInventory
        fields = ['inventory_id', 'quantity', 'amount']