from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OrganizationViewSet, ContactViewSet, ProductViewSet, OrderViewSet,
    TokenView, AdminStatsView, SizePriceViewSet
)

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'contacts', ContactViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sizeprices', SizePriceViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('auth/login/', TokenView.as_view(), name='token_obtain_pair'),
    path('admin/stats/', AdminStatsView.as_view(), name='admin_stats'),
    path('', include(router.urls)),
]
