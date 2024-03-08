import datetime

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt

from products.models import Product, Order
from products.tasks import hello_world_task, today_count_orders, top_selling_products_task


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

    return HttpResponse("Працює")

# @csrf_exempt
# def count_orders_view(request):
#     if request.method == 'GET':
#         # Вызываем вашу задачу и получаем количество заказов за сегодня
#         orders_count = today_count_orders.delay().get()  # Вызываем задачу асинхронно и получаем результат
#
#         # Возвращаем количество заказов в формате JSON
#         return JsonResponse({'today_orders_count': orders_count})
#     else:
#         return JsonResponse({'error': 'Method not allowed'}, status=405)
def today_count_orders_view(request):
    # day = datetime.date.today() - datetime.timedelta(days=1)
    # result = Order.objects.filter(created_at__date=day).count()
    result = today_count_orders.delay()
    # orders_count = result.get() if result.ready() else 'Task not yet complete'
    # print(result.get(timeout=10))
    return HttpResponse(f'Orders created today: {result}')
    # return HttpResponse({'today_orders_count': result})



# def today_count_orders_view(request):
#     orders_count = today_count_orders.delay().get()
#     return HttpResponse(f'Orders created yesterday: {orders_count}')

# def top_selling_products_view(request, *args, **kwargs):
#     return top_selling_products.delay()
#     # return HttpResponse('Task top_selling_products викликано!')




def top_selling_products_view(request):
    if request.method == 'GET':
        # Вызов задачи для получения топ-продуктов
        top_products = top_selling_products_task.delay()

        # Возвращаем JSON ответ с топ-продуктами
        return JsonResponse({'top_products': top_products.get()})

# def top_selling_products_view(request):
#     if request.method == 'GET':
#
#         task_result = top_selling_products_task.AsyncResult(task_id)
#
#
#         if task_result.ready():
#             top_products = task_result.get()
#             return JsonResponse({'top_products': top_products})
#         else:
#
#             return JsonResponse({'status': 'Task is still in progress'})