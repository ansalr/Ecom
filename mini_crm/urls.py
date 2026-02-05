from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from core.views import HealthCheckView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('health/', HealthCheckView.as_view(), name='health_check'),

    # Frontend Routes
    path('', TemplateView.as_view(template_name='login.html'), name='home'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('organizations/create/', TemplateView.as_view(template_name='org_create.html'), name='org_create'),
    path('contacts/create/', TemplateView.as_view(template_name='contact_create.html'), name='contact_create'),
    path('products/create/', TemplateView.as_view(template_name='product_create.html'), name='product_create'),
    path('products/', TemplateView.as_view(template_name='product_list.html'), name='product_list'),
    path('products/<int:pk>/update/', TemplateView.as_view(template_name='product_update.html'), name='product_update'),
    path('orders/create/', TemplateView.as_view(template_name='order_create.html'), name='order_create'),
    path('orders/<int:pk>/', TemplateView.as_view(template_name='order_detail.html'), name='order_detail'),
]
