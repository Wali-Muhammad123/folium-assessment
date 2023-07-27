from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Order
from .serializers import OrderSerializer
from django.contrib.auth.models import User

class OrderAPITest(APITestCase):

    def setUp(self):
        # Create a user and authenticate for testing authentication scenarios
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_list_orders(self):
        # Test GET request to list orders
        # Create some sample orders for testing
        Order.objects.create(item_name='Item 1', quantity=10)
        Order.objects.create(item_name='Item 2', quantity=5)

        response = self.client.get('/your-api-url/')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Assuming two sample orders were created

    def test_create_order_valid_data(self):
        # Test POST request to create a new order with valid data
        data = {'item_name': 'New Item', 'quantity': 15}

        response = self.client.post('/your-api-url/', data, format='json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify that the order was created in the database
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.item_name, 'New Item')
        self.assertEqual(order.quantity, 15)

    def test_create_order_insufficient_quantity(self):
        # Test POST request with insufficient quantity
        data = {'item_name': 'Item with Insufficient Quantity', 'quantity': 0}  # Assuming 0 quantity is insufficient

        response = self.client.post('/your-api-url/', data, format='json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'error': 'Insufficient Quantity available'})

    def test_create_order_invalid_data(self):
        # Test POST request with invalid data (missing required fields)
        data = {}  # Empty data, which is invalid

        response = self.client.post('/your-api-url/', data, format='json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_order_unauthenticated(self):
        # Test POST request without authentication
        self.client.logout()  # Log out the authenticated user

        data = {'item_name': 'New Item', 'quantity': 5}
        response = self.client.post('/your-api-url/', data, format='json')  # Replace with your actual API endpoint
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
