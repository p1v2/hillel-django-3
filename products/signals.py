from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save, post_delete, m2m_changed, post_init
from django.dispatch import receiver
from products.tasks import order_send_telegram_message, send_welcome_email

from products.models import Order, Product
from telegram.client import send_message


@receiver(post_save, sender=Order)
def send_order_telegram_message(sender, instance: Order, created, **kwargs):
    if created:
        order_send_telegram_message.apply_async((instance.uuid,), countdown=10)


# other types of signals
# pre_save
@receiver(pre_save, sender=Order)
def assign_display_number(sender, instance, **kwargs):
    instance.display_number = datetime.now().timestamp()


# post_delete
# pre_delete
@receiver(post_delete, sender=Order)
def after_order_deleted(sender, instance, **kwargs):
    print('Order deleted')
    chat_id = 192484569
    text = f"Order {instance.uuid} deleted"
    send_message(chat_id, text)


# m2m_changed
def products_tags_change(sender, instance, action, **kwargs):
    print(f'Products tags changed: {action}')
    print(f'instance: {instance}')
    print(f'kwargs: {kwargs}')


m2m_changed.connect(products_tags_change, sender=Order.products.through)


# post_init
# pre_init
# @receiver(post_init, sender=Order)
# def after_order_initialized(sender, instance, **kwargs):
#     print('Order initialized')
#     chat_id = 192484569
#     text = f"Order {instance.uuid} initialized"
#     send_message(chat_id, text)


@receiver(post_save, sender=User)
def user_saved(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.delay(instance.id)
