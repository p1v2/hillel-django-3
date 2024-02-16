from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.name} : {self.address} : {self.phone}"
