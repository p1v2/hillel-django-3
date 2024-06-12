'''Create the Store Model:
Design and implement a Store model within the Django application.
The Store model should at least include fields for the store's name,
address, and any other attributes you find relevant.
'''
from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name
