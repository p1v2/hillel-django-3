from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from products.models import Product
from products.serializers import ProductSerializer, ProductReadOnlySerializer


class ProductViewSet(viewsets.ModelViewSet):
    # select_related - for ForeignKey
    # prefetch_related - for ManyToMany
    queryset = Product.objects.select_related('category').prefetch_related('tags').all()

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ProductReadOnlySerializer
        return ProductSerializer
