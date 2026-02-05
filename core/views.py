from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Organization, Contact, Product, SizePrice, Order
from .serializers import (
    OrganizationSerializer, ContactSerializer, ProductSerializer, SizePriceSerializer,
    CreateSizePriceSerializer, OrderSerializer, CreateOrderSerializer
)
from .services import create_order_from_data

class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        return data

class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def sizes(self, request, pk=None):
        product = self.get_object()
        serializer = CreateSizePriceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SizePriceViewSet(viewsets.ModelViewSet):
    queryset = SizePrice.objects.all()
    serializer_class = SizePriceSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = create_order_from_data(
                    serializer.validated_data['contact_id'],
                    serializer.validated_data['items']
                )
                read_serializer = OrderSerializer(order)
                return Response(read_serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminStatsView(views.APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_orders = Order.objects.count()
        total_revenue = sum(order.total_amount for order in Order.objects.all())
        total_products = Product.objects.count()
        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "total_products": total_products
        })

class HealthCheckView(views.APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        return Response({
            "status": "ok",
            "app": "crm",
            "version": "v1.0.0"
        })
