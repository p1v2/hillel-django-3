from rest_framework import serializers

from products.models import StoreInventory, Product, Store


class StoreInventorySerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product.id', queryset=Product.objects.all())
    # product_name = serializers.CharField(source='product.title', read_only=True)
    store_id = serializers.PrimaryKeyRelatedField(source='store.id', queryset=Store.objects.all())
    # store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = StoreInventory
        fields = '__all__'
        # fields = ['id', 'store_id', 'store_name', 'product_id','product_name', 'quantity', 'price']
        # fields = ['id', 'store_id','product_id','quantity', 'price']