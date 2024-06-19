from datetime import datetime, timedelta

from celery import shared_task
from django.db.models import Count

from products.models import Order

from telegram.client import send_message


@shared_task
def hello_world_task():
    print('Hello World!')


@shared_task
def order_send_telegram_message(order_id):
    print("Sending telegram message")
    order = Order.objects.get(uuid=order_id)
    chat_id = 980106016

    order_products = order.order_products.all()
    text = f"New order {order.uuid} created\n"
    for order_product in order_products:
        text += f"{order_product.title} - {order_product.quantity} - {order_product.price}\n"

    send_message(chat_id, text)
    print("Message sent")


@shared_task
def daily_orders_count():
    print("Daily orders counting")
    amount_of_orders = Order.objects.filters(
        created_at__range=(datetime.today() - timedelta(days=1), datetime.today())).count()

    top_products_from_orders = Order.objects.filter(
        created_at__range=(datetime.today() - timedelta(days=1))
        .values('product_id')
        .annotate(count=Count('product_id'))
        .order_by('-count')[:3]
    )

    print(f"{amount_of_orders} orders created by day\n")
    print(f"{top_products_from_orders} top 3 products from orders\n")
    for product in top_products_from_orders:
        print(f"{product['product_id']}")