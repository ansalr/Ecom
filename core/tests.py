from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import Product, SizePrice, Organization, Contact, User
from .services import calculate_item_price, create_order_from_data
from decimal import Decimal

class LogicTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Coffee", sku="COF001", base_price=100.00, offer_percent=10.00
        )
        self.size_small = SizePrice.objects.create(
            product=self.product, size_name="Small", price=120.00
        )

    def test_price_calculation_with_size_and_offer(self):
        """
        Test that price uses SizePrice and applies offer.
        Size Price = 120. Offer = 10%. Expected = 120 * 0.9 = 108.
        """
        price = calculate_item_price(self.product, "Small")
        self.assertEqual(price, Decimal("108.00"))

    def test_price_calculation_base_price_fallback(self):
        """
        Test fallback to base_price if size not found.
        Base = 100. Offer = 10%. Expected = 90.
        """
        price = calculate_item_price(self.product, "Large")
        self.assertEqual(price, Decimal("90.00"))

    def test_cart_merge_logic(self):
        """
        Test that two items with same details merge into one line item.
        """
        org = Organization.objects.create(name="Test Org")
        contact = Contact.objects.create(
            first_name="John", last_name="Doe", email="j@d.com", phone="123", organization=org
        )
        
        items_data = [
            {'product_id': self.product.id, 'size_name': 'Small', 'qty': 1},
            {'product_id': self.product.id, 'size_name': 'Small', 'qty': 2}
        ]
        
        order = create_order_from_data(contact.id, items_data)
        
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().qty, 3)

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='admin', password='password', role='admin')
        self.client.force_authenticate(user=self.user)
        
        self.org = Organization.objects.create(name="Test Org")
        self.contact = Contact.objects.create(
            first_name="Jane", last_name="Doe", email="jane@d.com", phone="555", organization=self.org
        )
        self.product = Product.objects.create(
            name="Tea", sku="TEA001", base_price=50.00
        )
        
    def test_create_order_api(self):
        url = reverse('order-list')
        data = {
            'contact_id': self.contact.id,
            'items': [
                {'product_id': self.product.id, 'size_name': 'Standard', 'qty': 2}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['items'][0]['qty'], 2)
        self.assertEqual(response.data['total_amount'], "100.00")
