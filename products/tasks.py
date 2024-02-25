import datetime

from celery import shared_task
import requests
from django.db.models import Sum

from products.models import OrderProduct
from products.models.order import Order
from telegram.client import send_message


@shared_task
def hello_world_task():
    print('Hello, World!')

@shared_task
def order_send_telegram_message(order_id):
    print('Sending telegram message')
    order = Order.objects.get(uuid=order_id)

    chat_id = 192484569

    order_products = order.order_products.all()
    text = f"New order {order.uuid} created\n"
    for order_product in order_products:
        text += f"{order_product.product.title} - {order_product.quantity} - {order_product.price}\n"

    send_message(chat_id, text)
    print('Telegram message sent')


# Celery task in  project that runs daily at 10 . Count how many orders were created during the day.
# @shared_task
# def today_count_orders():
#     # day = datetime.date.today() - datetime.timedelta(days=1)
#     # orders = Order.objects.filter(create_at__date=day).count()
#     # orders_today = Order.objects.filter(create_at__date=datetime.date.today()).count()
#     orders_today = Order.objects.filter(create_at__date=datetime.date.today()).all()
#     print(f'Orders created yesterday: {orders_today}')

# @shared_task
# def top_selling_products():
#     order_today = Order.objects.filter(created_at__date=datetime.date.today()).all()
#     top_products = order_today.values('order_products__product__title').annotate(
#         total_quantity=Sum('order_products__quantity')
#     ).order_by('-total_quantity')
#     # print(top_products[:3])
#     return top_products
@shared_task
def top_selling_products_task():
    order_products = OrderProduct.objects.filter(created_at__date=datetime.date.today()).all()
    top_products = order_products.values('order_products__product__title').annotate(
        total_quantity=Sum('order_products__quantity')
    ).order_by('-total_quantity')[:3]
    return list(top_products)

@shared_task
def today_count_orders():
    day = datetime.date.today() - datetime.timedelta(days=2)
    orders = Order.objects.filter(created_at__date=day).count()
    # print(f'Orders created yesterday: {orders}')
    return orders.get()
    # print(f'Orders created yesterday: {orders}')