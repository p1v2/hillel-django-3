import graphene
import graphene_django
from django.db import transaction
from graphene import Field
from rest_framework.authtoken.admin import User
from graphene import Mutation, Field, List, String
from graphene_django.types import DjangoObjectType

from products.models import Product, Order, Category, Tag, OrderProduct


class CategoryObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TagObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'summary', 'is_18_plus', 'category', 'tags']


class PaginatedProductObjectType(graphene.ObjectType):
    nodes = graphene.List(ProductObjectType)
    total_count = graphene.Int()


class OrderObjectType(graphene_django.DjangoObjectType):
    class Meta:
        model = Order
        fields = ['uuid', 'products']


class Query(graphene.ObjectType):
    products = graphene.Field(PaginatedProductObjectType, offset=graphene.Int(), limit=graphene.Int())
    product = graphene.Field(ProductObjectType, id=graphene.ID())
    orders = graphene.List(OrderObjectType, user_id=graphene.Int())

    def resolve_product(self, info, id):
        # If category selected, then select_related('category')
        selections = info.field_nodes[0].selection_set.selections
        category_selected = any(selection.name.value == 'category' for selection in selections)
        tags_selected = any(selection.name.value == 'tags' for selection in selections)

        query = Product.objects.all()
        if category_selected:
            query = query.select_related('category')
        if tags_selected:
            query = query.prefetch_related('tags')

        try:
            return query.get(id=id)
        except Product.DoesNotExist:
            return None

    def resolve_products(self, info, offset=None, limit=None):
        total_count = Product.objects.count()

        product_qs = Product.objects.all()

        if offset is not None:
            product_qs = product_qs[offset:]
        if limit is not None:
            product_qs = product_qs[:limit]

        return {
            "nodes": product_qs,
            "total_count": total_count,
        }

    def resolve_orders(self, info, user_id=None):
        if user_id is None:
            return Order.objects.all()
        return Order.objects.filter(user_id=user_id)


class CreateProductMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        summary = graphene.String(required=True)
        is_18_plus = graphene.Boolean(required=True)

    product = graphene.Field(ProductObjectType)
    user_errors = graphene.List(graphene.String)
    error = graphene.String()

    def mutate(self, info, title, price, summary, is_18_plus):
        if price < 0:
            return CreateProductMutation(product=None, user_errors=['Price must be greater than 0'])

        try:
            product = Product.objects.create(title=title, price=price, summary=summary, is_18_plus=is_18_plus)
            return CreateProductMutation(product=product)
        except Exception as e:
            print(e)
            return CreateProductMutation(product=None, error=str(e))


class UpdateProductMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        price = graphene.Decimal()
        summary = graphene.String()
        is_18_plus = graphene.Boolean()

    product = graphene.Field(ProductObjectType)
    user_errors = graphene.List(graphene.String)
    error = graphene.String()

    def mutate(self, info, id, title=None, price=None, summary=None, is_18_plus=None):
        try:
            product = Product.objects.get(id=id)

            if title is not None:
                product.title = title
            if price is not None:
                product.price = price
            if summary is not None:
                product.summary = summary
            if is_18_plus is not None:
                product.is_18_plus = is_18_plus

            product.save()
            return UpdateProductMutation(product=product)
        except Product.DoesNotExist:
            return UpdateProductMutation(product=None, user_errors=['Product not found'])
        except Exception as e:
            return UpdateProductMutation(product=None, error=str(e))



class CreateOrderMutation(Mutation):
    '''
    mutation {
      createOrder(userId: 1, productIds: [8, 88, 888]) {
        order {
          uuid
          products {
            id
            title
            price

          }
        }
        error
        userErrors
      }
    }
    '''
    class Arguments:
        user_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    order = Field(OrderObjectType)
    user_errors = List(String)
    error = String()

    @transaction.atomic  # Забезпечує цілісність даних
    def mutate(self, info, user_id, product_ids):
        try:
            user = User.objects.get(pk=user_id)
            products = Product.objects.filter(pk__in=product_ids)

            if len(products) != len(product_ids):
                # перевірка на присутність ID товарів
                missing_product_ids = []
                for product_id in product_ids:
                    try:
                        Product.objects.get(pk=product_id)
                    except Product.DoesNotExist:
                        missing_product_ids.append(product_id)
                if missing_product_ids:
                    raise Exception(
                        f"Товар с ID {', '.join(str(product_id) for product_id in missing_product_ids)} не знайдені.")

            with transaction.atomic():  # Вкладена транзакція для узгодженості даних
                order = Order.objects.create(user=user)
                for product in products:
                    OrderProduct.objects.create(order=order, product=product)

            return CreateOrderMutation(order=order)
        except User.DoesNotExist as e:
            return CreateOrderMutation(user_errors=["Хибний ID користувача"], error=str(e))
        except Exception as e:
            return CreateOrderMutation(error=str(e))


class Mutation(graphene.ObjectType):
    create_product = CreateProductMutation.Field()
    update_product = UpdateProductMutation.Field()
    delete_product = graphene.Boolean(id=graphene.ID(required=True))

    create_order = CreateOrderMutation.Field()

    def resolve_delete_product(self, info, id):
        try:
            Product.objects.get(id=id).delete()
            return True
        except Product.DoesNotExist:
            return False

    def resolve_create_order(self, info, user_id, product_ids):

        return CreateOrderMutation(user_id=user_id, product_ids=product_ids)


schema = graphene.Schema(query=Query, mutation=Mutation)


