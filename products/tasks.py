import datetime

from celery import shared_task
from django.db.models import Sum

from hillelDjango3.celery import app
from products.models.order import Order
from telegram.client import send_message


@shared_task
def hello_world_task():
    print('Hello, World!')


@shared_task
def order_send_telegram_message(order_id):
    print('Sending telegram message')
    order = Order.objects.get(uuid=order_id)

    chat_id = 968123153

    order_products = order.order_products.all()
    text = f"New order {order.uuid} created\n"
    for order_product in order_products:
        text += f"{order_product.product.title} - {order_product.quantity} - {order_product.price}\n"

    send_message(chat_id, text)
    print('Telegram message sent')


@app.task(bind=True)
def top_selling_products_task(self):
    order_products = Order.objects.filter(created_at__date=datetime.date.today()).all()
    top_products = order_products.values('order_products__product__title').annotate(
        total_quantity=Sum('order_products__quantity')).order_by('-total_quantity')[0:3]
    print(top_products)
    return list(top_products)


@app.task(bind=True)
def today_count_orders_task(self):
    day = datetime.date.today() - datetime.timedelta(days=0)
    orders = Order.objects.filter(created_at__date=day).count()
    print(orders)
    return orders
