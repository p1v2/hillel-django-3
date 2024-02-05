from django.http import JsonResponse

from products.models import Product


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
