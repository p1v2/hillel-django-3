from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Order
from products.tasks import order_send_telegram_message


@receiver(post_save, sender=Order)
def send_order_telegram_message(sender, instance: Order, created, **kwargs):
    # if created:
    #     chat_id = 980106016
    #
    #     order_products = instance.order_products.all()
    #     text = f"new order {instance.uuid} created\n"
    #     for order_product in order_products:
    #         text += f"{order_product.product.title} - {order_product.quantity} - {order_product.price}\n"
    #     send_message(chat_id, text)
    if created:
        order_send_telegram_message.apply_async((instance.uuid,), countdown=10)