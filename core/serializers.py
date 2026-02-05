from rest_framework import serializers
from .models import User, Organization, Contact, Product, SizePrice, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class ContactSerializer(serializers.ModelSerializer):
    organization_name = serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = Contact
        fields = '__all__'

class SizePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizePrice
        fields = ('id', 'size_name', 'price')

class ProductSerializer(serializers.ModelSerializer):
    size_prices = SizePriceSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'

class CreateSizePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SizePrice
        fields = ('size_name', 'price', 'product')

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    line_total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'size_name', 'qty', 'unit_price', 'extras', 'customization', 'line_total')

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    contact_name = serializers.ReadOnlyField(source='contact.first_name')
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'order_no', 'contact', 'contact_name', 'created_at', 'items', 'total_amount')

class CreateOrderSerializer(serializers.Serializer):
    contact_id = serializers.IntegerField()
    items = serializers.ListField(
        child=serializers.DictField()
    )
