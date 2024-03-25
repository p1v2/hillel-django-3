import graphene
import graphene_django

from products.models import Product, Order


class ProductObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Product
        fields = ['title', 'price', 'summary']


class OrderObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Order
        fields = ['uuid']


class Query(graphene.ObjectType):
    products = graphene.List(ProductObjectType, offset=graphene.Int(), limit=graphene.Int())
    orders = graphene.List(OrderObjectType, user_id=graphene.Int())

    def resolve_products(self, info, offset=None, limit=None):
        return Product.objects.all()[offset:offset+limit]

    def resolve_orders(self, info, user_id=None):
        if user_id is None:
            return Order.objects.all()
        return Order.objects.filter(user_id=user_id)


schema = graphene.Schema(query=Query)
