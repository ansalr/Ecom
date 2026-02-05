from django.contrib import admin
from .models import Organization, Contact, Product, SizePrice, Order, OrderItem, User 

# Register your models here.
admin.site.register(Organization)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(SizePrice)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(User)