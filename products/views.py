from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from products.models import Product
from products.tasks import hello_world_task


# Create your views here.
def products_view(request, *args, **kwargs):
    # request.GET {'offset': 1, 'limit': 10}
    offset = request.GET.get('offset', 0)
    limit = request.GET.get('limit', 10)

    products = Product.objects.all()[int(offset):int(offset) + int(limit)]

    products_list = []

    for product in products:
        products_list.append({
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'summary': product.summary,
            'is_18_plus': product.is_18_plus,
        })

    # return JsonResponse({'data': products_list})

    return render(request, 'products.html', {'products': products})

def celery_view(request, *args, **kwargs):
    hello_world_task.delay()

    return HttpResponse("OK")
