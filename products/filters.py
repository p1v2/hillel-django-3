import django_filters

from products.models import Product


class ProductFilter(django_filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='price', lookup_expr='gte')
    category_name = django_filters.CharFilter(
        field_name='category__name', lookup_expr='icontains')
    adult = django_filters.BooleanFilter(field_name='is_18_plus')

    class Meta:
        model = Product
        fields = {
            # contains, i - case insensitive
            'title': ['icontains'],
            # less than, greater than
            'price': ['lt', 'gt'],
            'category': ['exact'],
            'tags': ['exact'],
            'created_at': ['date__gt', 'date__lt'],
        }
