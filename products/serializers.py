from rest_framework import serializers

from products.models import Product, Category, Tag


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class ProductReadOnlySerializer(serializers.ModelSerializer):
    price_usd = serializers.SerializerMethodField()
    price = serializers.FloatField()
    category = CategorySerializer()
    tags = TagSerializer(many=True)

    def get_price_usd(self, obj: Product):
        price_usd = obj.price / 38

        return round(price_usd, 2)

    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'summary', 'price_usd', 'category', 'tags')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price', 'summary', 'category', 'tags')
