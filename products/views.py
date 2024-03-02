import datetime

from django.http import JsonResponse, HttpResponse

from products.models import Product, Order
from products.tasks import hello_world_task, top_selling_products_task, today_count_orders_task


# Create your views here.
def products_view(request, *args, **kwargs):
    products = Product.objects.filter(featured=True)

    products_list = []

    for product in products:
        products_list.append({
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'summary': product.summary,
            'is_18_plus': product.is_18_plus,
        })

    return JsonResponse({'data': products_list})


def celery_view(request, *args, **kwargs):
    hello_world_task.delay()

    return HttpResponse("Усьо Добре!")


def top_selling_products_view(request):
    if request.method == 'GET':
        top_products = top_selling_products_task.delay()
        return JsonResponse({'top_products': top_products.get()})


def today_count_orders_view(request):
    if request.method == 'GET':
        today_count_orders = today_count_orders_task.delay()
        return JsonResponse({'today_count_orders': today_count_orders.get()})
