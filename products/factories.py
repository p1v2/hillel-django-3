from factory.django import DjangoModelFactory
import factory

from products.models import Product, Category, Tag


class CategoryFactory(DjangoModelFactory):
    name = factory.Faker('word')
    description = factory.Faker('text')

    class Meta:
        model = Category


class TagFactory(DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Tag


class ProductFactory(DjangoModelFactory):
    title = factory.Faker('word')
    summary = factory.Faker('text')
    price = factory.Faker('random_number', digits=3)

    class Meta:
        model = Product
