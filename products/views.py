from django.http import JsonResponse, HttpResponse

from products.models import Product
from products.tasks import hello_world_task, today_count_orders, top_selling_products


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


def today_count_orders_view():
    result = today_count_orders().delay()
    # orders_count = result.get() if result.ready() else 'Task not yet complete'
    return HttpResponse(f'Orders created yesterday: {result}')



# def today_count_orders_view(request):
#     orders_count = today_count_orders.delay().get()
#     return HttpResponse(f'Orders created yesterday: {orders_count}')

def top_selling_products_view(request, *args, **kwargs):
    top_selling_products.delay()
    return HttpResponse('Task top_selling_products викликано!')
