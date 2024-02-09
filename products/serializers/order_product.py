from rest_framework import serializers

from products.models import OrderProduct


class OrderProductSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.FloatField()

    class Meta:
        model = OrderProduct
        fields = ['product_id', 'quantity']
