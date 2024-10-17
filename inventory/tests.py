from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from AuthApp.models import User


class ItemViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            full_name="John Doe",
            email="john.doe@example.com",
            password="strong_password123",
            is_active=True
        )

        self.login_url = reverse('login')  # Ensure this is the correct URL for your login endpoint
        self.item_url = reverse('item-list')  # Assuming your ItemViewSet is registered as 'item-list'

        # Perform login to get the token
        login_data = {
            'email': 'john.doe@example.com',
            'password': 'strong_password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        
        self.assertEqual(response.status_code, 200)
        self.token = response.data['token']

        # Set the authorization header with the token for authenticated requests
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_create_item_authenticated(self):
        """Test creating an item while authenticated."""
        item_data = {
            'name': 'Test Item',
            'description': 'A description for test item',
            'quantity': 10
        }
        response = self.client.post(self.item_url, item_data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_create_item_unauthenticated(self):
        """Test creating an item without authentication should fail."""
        self.client.credentials()  # Remove the token to simulate an unauthenticated request
        item_data = {
            'name': 'Unauthenticated Item',
            'description': 'A description for test item',
            'quantity': 5
        }
        response = self.client.post(self.item_url, item_data, format='json')
        self.assertEqual(response.status_code, 401)  # Expect 401 Unauthorized for unauthenticated requests

    def test_retrieve_item_authenticated(self):
        """Test retrieving an item while authenticated."""
        # Create an item first
        item_data = {
            'name': 'Another Item',
            'description': 'A description',
            'quantity': 5
        }
        create_response = self.client.post(self.item_url, item_data, format='json')
        item_id = create_response.data['id']
        retrieve_url = reverse('item-detail', args=[item_id])

        # Retrieve the item
        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Another Item')

    def test_retrieve_item_unauthenticated(self):
        """Test retrieving an item without authentication should fail."""
        # Create an item first
        item_data = {
            'name': 'Unauthenticated Retrieve Item',
            'description': 'A description',
            'quantity': 5
        }
        create_response = self.client.post(self.item_url, item_data, format='json')
        item_id = create_response.data['id']
        retrieve_url = reverse('item-detail', args=[item_id])

        # Simulate unauthenticated request by removing the token
        self.client.credentials()

        # Try to retrieve the item
        response = self.client.get(retrieve_url, format='json')
        self.assertEqual(response.status_code, 401)  # 401 Unauthorized
