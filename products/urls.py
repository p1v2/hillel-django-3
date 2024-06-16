from rest_framework.routers import DefaultRouter
from products.viewsets import StoreViewSet, ProductViewSet, OrderViewSet, RecipeViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'recipes', RecipeViewSet)

urlpatterns = router.urls
