from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User

class UserSignUpTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('signup')

    def test_user_signup_success(self):
        """Test that a user can sign up with valid data"""
        data = {
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "password": "strong_password123"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['full_name'], "John Doe")
        self.assertEqual(response.data['email'], "john.doe@example.com")
        self.assertFalse('password' in response.data)  # Password should not be returned

        # Ensure the user exists in the database
        user_exists = User.objects.filter(email="john.doe@example.com").exists()
        self.assertTrue(user_exists)

    def test_user_signup_missing_fields(self):
        """Test that sign up fails when required fields are missing"""
        data = {
            "full_name": "John Doe",
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 400)

    def test_user_signup_existing_email(self):
        """Test that sign up fails if the email is already taken"""
        User.objects.create_user(full_name="John Doe", email="john.doe@example.com", password="strong_password123")
        data = {
            "full_name": "Jane Doe",
            "email": "john.doe@example.com",
            "password": "strong_password456"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email', response.data)


class LoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')  # Ensure 'login' is your URL name
        self.password = 'strong_password123'
        
        # Create a sample active user
        self.active_user = User.objects.create_user(
            full_name="Active User",
            email="activeuser@example.com",
            password=self.password,
            is_active=True
        )
        
        # Create a sample inactive user
        self.inactive_user = User.objects.create_user(
            full_name="Inactive User",
            email="inactiveuser@example.com",
            password=self.password,
            is_active=False
        )
    
    def test_login_success(self):
        """Test login with valid credentials for an active user"""
        data = {
            "email": "activeuser@example.com",
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data['success'])
        self.assertIn('token', response.data)
        self.assertIn('data', response.data)

    def test_login_missing_email(self):
        """Test login with missing email"""
        data = {
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], "Required email.")
    
    def test_login_missing_password(self):
        """Test login with missing password"""
        data = {
            "email": "activeuser@example.com"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], "Required password.")
    
    def test_login_invalid_email(self):
        """Test login with non-existent email"""
        data = {
            "email": "nonexistent@example.com",
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], "Email not found.")
    
    def test_login_invalid_password(self):
        """Test login with incorrect password"""
        data = {
            "email": "activeuser@example.com",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], "Invalid password.")
    
    def test_login_inactive_user(self):
        """Test login with inactive user account"""
        data = {
            "email": "inactiveuser@example.com",
            "password": self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.data['success'])
        self.assertEqual(response.data['message'], "Your account is inactive. Please contact admin.")
