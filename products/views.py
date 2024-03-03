from django.http import JsonResponse, HttpResponse

from products.models import Product
from products.tasks import hello_world_task
from products.tasks import daily_order_count


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

    return HttpResponse("OK")


def daily_order_count_view(request, *args, **kwargs):
    daily_order_count.delay()

    return HttpResponse("OK")