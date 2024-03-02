import uuid
from django.contrib.auth.models import User
from django.db import models

from products.models import Product
from telegram.client import send_message
from django.dispatch import receiver
from django.db.models.signals import post_save


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    # on_delete=models.CASCADE means that if the user is deleted, all of their orders will be deleted
    # on_delete=models.SET_NULL means that if the user is deleted, the order will still exist, but the user will be set to NULL
    # on_delete=models.PROTECT means that if the user is deleted, the order will still exist, but the user will be set to NULL
    # on_delete=models.SET_DEFAULT means that if the user is deleted, the order will still exist, but the user will be set to the default user
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='OrderProduct')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # because we added related_name='orders' in the OrderProduct model, we can access the order_products from the Order model
    # order_products = models.ManyToManyField('OrderProduct')

    @property
    def total_price(self):
        total_price = 0
        for order_product in self.order_products.all():
            total_price += order_product.price
        return total_price

    def __str__(self):
        return f"{self.created_at} : {self.user.username} - {self.total_price}"


@receiver(post_save, sender=Order)
def send_order_telegram_message(sender, instance: Order, created, **kwargs):
    if created:
        chat_id = 968123153
        text = f"New order {instance.uuid} created"
        send_message(chat_id, text)
