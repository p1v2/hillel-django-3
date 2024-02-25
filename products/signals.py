# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from products.tasks import order_send_telegram_message
#
# from products.models import Order
#
#
# @receiver(post_save, sender=Order)
# def send_order_telegram_message(sender, instance: Order, created, **kwargs):
#     if created:
#         order_send_telegram_message.apply_async((instance.uuid,), countdown=10)
