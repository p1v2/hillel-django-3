import random
from datetime import datetime, timedelta

from django.core.management import BaseCommand

from products.factories import ProductFactory, TagFactory, CategoryFactory
from products.models import Product


class Command(BaseCommand):
    def handle(self, *args, **options):
        # tags = TagFactory.create_batch(1000)
        # categories = CategoryFactory.create_batch(100)
        #
        # products = ProductFactory.create_batch(1000)
        #
        # for product in products:
        #     random_category = random.choice(categories)
        #     random_tags = random.sample(tags, random.randint(1, 10))
        #
        #     product.category = random_category
        #     product.tags.set(random_tags)
        #
        #     product.save()
        products = Product.objects.all()
        for prodict in products:

            random_date = datetime.now() - timedelta(days=random.random() * 30)
            prodict.created_at = random_date
            prodict.save()