from celery import shared_task
from django.core.mail import send_mail, EmailMessage
from rest_framework.authtoken.admin import User
from datetime import datetime, timedelta
from django.db.models import Count

from google_sheets.api import write_to_sheet
from products.models import Product
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
        'pavliuk96@gmail.com',
        ['vitalii@vitalii.tech'],
        fail_silently=False,
    )

    # Send html email
    # send_mail(
    #     'Welcome to our service',
    #     f'Hello, {user.username}! Welcome to our service!',
    #     "pavliuk96@gmail.com",
    #     ['vitalii@vitalii.tech'],
    #     html_message=f'<h1>Hello, {user.username}!</h1><p>Welcome to our service!</p>',
    #     fail_silently=False,
    # )

    # Send html with attachment
    # email_message = EmailMessage(
    #     'Welcome to our service',
    #     f'Hello, {user.username}! Welcome to our service!',
    #     "pavliuk96@gmail.com",
    #     ['vitalii@vitalii.tech'],
    # )
    # # attach file
    # email_message.attach_file('img.png')
    # email_message.attach_file("img2.jpg")
    # email_message.send()

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


@shared_task
def daily_order_count():
    # Get the start and end date for the last day
    end_date = datetime.now()
    start_date = end_date - timedelta(days=1)

    # Count orders created during the last day
    orders_count = Order.objects.filter(created_at__range=(start_date, end_date)).count()

    top_products = Order.objects.filter(created_at__range=(start_date, end_date)) \
                       .values('product_id') \
                       .annotate(count=Count('product_id')) \
                       .order_by('-count')[:3]

    # Log the statistics
    print(f"Orders created during the last day: {orders_count}")
    print("Top 3 ordered products:")
    for product in top_products:
        print(f"Product ID: {product['product_id']}, Count: {product['count']}")
