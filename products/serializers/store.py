from rest_framework import serializers

from products.models import Store, StoreInventory


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'address', 'description', 'email', 'phone']






