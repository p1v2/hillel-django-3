from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from hillelDjango3.permissions import IsOwnerOrReadOnly
from products.models import Product, Order, Recipe
from products.serializers import ProductSerializer, ProductReadOnlySerializer, OrderSerializer
from products.serializers.recipe import RecipeSerializer


class ProductViewSet(viewsets.ModelViewSet):
    # select_related - for ForeignKey
    # prefetch_related - for ManyToMany
    queryset = Product.objects.select_related('category').prefetch_related('tags').all()

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductReadOnlySerializer
        return ProductSerializer


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
