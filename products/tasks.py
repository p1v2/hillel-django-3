
import datetime

from celery import shared_task
import requests
from django.db.models import Sum

from products.models import OrderProduct

from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from rest_framework.authtoken.admin import User

from google_sheets.api import write_to_sheet
from products.models import Product

from products.models.order import Order
from telegram.client import send_message
from hillelDjango3.celery import app

@app.task(bind=True)
def hello_world_task(self):
    print('Hello, World!')

@app.task(bind=True)
def order_send_telegram_message(self, order_id):
    print('Sending telegram message')
    order = Order.objects.get(uuid=order_id)

    chat_id = 192484569

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
        total_quantity=Sum('order_products__quantity')
    ).order_by('-total_quantity')[:3]
    return list(top_products)

@app.task(bind=True)
def today_count_orders(self):
    day = datetime.date.today() - datetime.timedelta(days=0)
    orders = Order.objects.filter(created_at__date=day).count()
    print(f'Orders created yesterday: {orders.get()}')
    # return orders
    # print(f'Orders created yesterday: {orders}') -

@shared_task
def write_google_sheet_products_report():
    products = Product.objects.all()

    # write to google sheet
    products_data = []

    for product in products:
        products_data.append([product.title, float(product.price), product.description])

    # write to google sheet
    write_to_sheet("A:C", products_data)


@shared_task
def send_welcome_email(user_id):
    user = User.objects.get(id=user_id)

    # Send text email
    send_mail(
        'Welcome to our service',
        f'Hello, {user.username}! Welcome to our service!',
        'dy5780356@gmail.com',
        ['dima.ermolenko@gmail.com'], #'vitalii@vitalii.tech', from products.tasks import send_welcome_email
        fail_silently=False,
    )
    #
    # # Send html email
    # send_mail(
    #     'Welcome to our service',
    #     f'Hello, {user.username}! Welcome to our service!',
    #     "dy5780356@gmail.com",
    #     ['vitalii@vitalii.tech'],
    #     html_message=f'<h1>Hello, {user.username}!</h1><p>Welcome to our service!</p>',
    #     fail_silently=False,
    # )
    #
    # # Send html with attachment
    # email_message = EmailMessage(
    #     'Welcome to our service',
    #     f'Hello, {user.username}! Welcome to our service!',
    #     "dy5780356@gmail.com",
    #     ['vitalii@vitalii.tech'],
    # )
    # # attach file
    # email_message.attach_file('img.png')
    # email_message.attach_file("img2.jpg")
    # email_message.send()
    #
    # # Send html with generated attachemnts
    # txt_file_content = 'Hello, World!'
    #
    # email_message = EmailMessage(
    #     'Welcome to our service',
    #     f'Hello, {user.username}! Welcome to our service!',
    #     "pavliuk96@gmail.com",
    #     ['vitalii@vitalii.tech'],
    # )
    # email_message.attach('hello.txt', txt_file_content, 'text/plain')
    # email_message.send()
    #
    # return "LOL!"

