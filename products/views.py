from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from .tasks import hello_world_task, daily_orders_count
from .models import Product, Order


# Create your views here.


def products_view(request, *args, **kwargs):
    products = Product.objects.all()
    products_lists = []

    for product in products:
        products_lists.append({
            'title': product.title,
            'description': product.description,
            'price': product.price,
            'summary': product.summary,
            'is_18_plus': product.is_18_plus,

        })
        return JsonResponse({'data': products_lists})
        # return render(request, 'products.html', {'products': products_lists})


def celery_view(request, *args, **kwargs):
    hello_world_task.delay()

    return HttpResponse("OK")


def daily_order_count_view(request, *args, **kwargs):
    daily_orders_count.delay()

    return HttpResponse("OK")