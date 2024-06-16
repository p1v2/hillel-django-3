from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from hillelDjango3.permissions import IsOwnerOrReadOnly
from products.filters import ProductFilter
from products.models import Product, Order, Recipe, Store
from products.pagination import PagePerPagePagination
from products.serializers import ProductSerializer, ProductReadOnlySerializer, OrderSerializer, StoreSerializer
from products.serializers.recipe import RecipeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    # select_related - for ForeignKey
    # prefetch_related - for ManyToMany
    queryset = Product.objects.exclude(is_18_plus=True).select_related(
        'category').prefetch_related('tags').all()

    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_class = ProductFilter
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    pagination_class = PagePerPagePagination

    ordering_fields = ['price', 'title']
    ordering = ['title']

    # Viewset method caching
    # def list(self, request, *args, **kwargs):
    #     get_params = request.query_params
    #     get_params_string = "/".join([f"{key}/{value}" for key, value in dict(get_params).items()])
    #
    #     cache_key = f"api_products/{get_params_string}"
    #     cached_products = cache.get(cache_key)
    #
    #     if cached_products:
    #         return Response(cached_products)
    #     else:
    #         response = super().list(request, *args, **kwargs)
    #         cache.set(cache_key, response.data)
    #         return response

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductReadOnlySerializer
        return ProductSerializer

    @action(detail=False, methods=['get'])
    def latest(self, request, *args, **kwargs):
        latest_product = self.queryset.latest('created_at')

        return Response(ProductReadOnlySerializer(latest_product).data)

    @action(detail=True, methods=['get'])
    def tags(self, request, *args, **kwargs):
        product = self.get_object()
        tags = product.tags.all()

        return Response([{'id': tag.id, 'name': tag.name} for tag in tags])


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related(
        'order_products', 'order_products__product')
    serializer_class = OrderSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsOwnerOrReadOnly]


class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
