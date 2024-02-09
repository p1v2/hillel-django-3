from django.contrib.auth.models import User
from django.db import models

from products.models import Product


class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    name = models.CharField(max_length=255)

    # ...
    def __str__(self):
        return self.name
