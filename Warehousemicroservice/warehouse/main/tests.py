from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Product
from .serializers import ProductSerializer
from django.urls import reverse
import json

# Create your tests here.
class ProductAPITest(APITestCase):
    def setUp(self):
        # Create a test product
        self.product_data = {
            'product_name': 'Test Product',
            'product_price': 10,
            'product_quantity': 100,
            'product_description': 'This is a test product',
        }
        self.product = Product.objects.create(**self.product_data)
        self.url = reverse('product-list')  # Assuming you have named the URL pattern for list view as 'product-list'

    def test_create_product(self):
        # Ensure we can create a new product
        data = {
            'product_name': 'New Product',
            'product_price': 20,
            'product_quantity': 50,
            'product_description': 'This is a new product',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)  # Check if the product was actually created in the database

    def test_create_product_invalid_data(self):
        # Ensure we can't create a product with invalid data (missing required fields)
        data = {
            'product_name': 'Invalid Product',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        # Ensure we can update an existing product
        data = {
            'product_name': 'Updated Product',
            'product_price': 15,
            'product_quantity': 200,
            'product_description': 'This product has been updated',
        }
        update_url = reverse('product-detail', args=[self.product.product_id])
        response = self.client.put(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.product_name, 'Updated Product')

    def test_update_nonexistent_product(self):
        # Ensure updating a non-existent product returns a 404
        data = {
            'product_name': 'Updated Product',
            'product_price': 15,
            'product_quantity': 200,
            'product_description': 'This product has been updated',
        }
        update_url = reverse('product-detail', args=['nonexistent_uuid'])  # Use a non-existent UUID
        response = self.client.put(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_only_unauthenticated(self):
        # Ensure unauthenticated users can only read (GET) the products and not create/update
        self.client.logout()
        data = {
            'product_name': 'New Product',
            'product_price': 20,
            'product_quantity': 50,
            'product_description': 'This is a new product',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        update_url = reverse('product-detail', args=[self.product.product_id])
        response = self.client.put(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_write_authenticated(self):
        # Ensure authenticated users can read (GET) and write (POST, PUT) products
        # Assuming you have a test user, replace 'testuser' and 'testpassword' with the actual credentials
        self.client.login(username='testuser', password='testpassword')

        data = {
            'product_name': 'New Product',
            'product_price': 20,
            'product_quantity': 50,
            'product_description': 'This is a new product',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        update_url = reverse('product-detail', args=[self.product.product_id])
        response = self.client.put(update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
