"""
Tests for the user api.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

CREATE_USER_URL = reverse('user:sign-up')


class PublicUserApiTests(TestCase):
    """Tests for unauthenticated api requests for the user api."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test that with valid payload, user can be created."""
        payload = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'test1234.',
            'designation': 'Test Designation',
            'contact_number': '123456789',
            'employee_id': '1234'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        user = get_user_model().objects.get(email=payload['email'])

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for attr, value in payload.items():
            if attr != 'password':
                self.assertEqual((getattr(user, attr)), value)
        self.assertNotIn('password', res.data)

    def test_create_user_but_user_exists_error(self):
        """Test creating a user returns error,
        that already exists in the system."""
        email = 'test@example.com'
        password = 'test1234.'
        name = 'Test User'
        contact_number = '1234567890'

        get_user_model().objects.create(
            email=email,
            password=password,
            name=name,
            contact_number=contact_number
        )

        payload = {
            'name': name,
            'email': email,
            'contact_number': contact_number,
            'password': password
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(get_user_model().objects.filter(email=email).exists())

    def test_password_too_short_error(self):
        """Test creating a user with short password returns error."""
        payload = {
            'email': 'test@example.com',
            'password': 'Test123.',
            'name': 'Test User',
            'contact_number': '12345657890'
        }

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(get_user_model().objects.filter(
            email=payload['email']).exists())

    def test_too_long_contact_number_raises_error(self):
        """Test that contact number greater than 10 characters
        raises an error."""
        payload = {
            'email': 'test@example.com',
            'password': 'test1234.',
            'contact_number': '123456789012345'
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(
            email=payload['email']).exists())
