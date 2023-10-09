"""
Tests for the user api.
"""

from unittest.mock import patch
import os
import tempfile

from core import models

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from PIL import Image

CREATE_USER_URL = reverse('user:sign-up')
TOKEN_URL = reverse('user:token')
USER_DETAILS_URL = reverse('user:me')
BACKGROUND_UPLOAD_URL = reverse('user:user-background-upload-image')


def background_image_upload_url(user_id):
    """Return the url for background image upload for a specific user."""
    return reverse('user:user-background-upload-image', args=[user_id])


def create_user(**params):
    """Create and return a sample user."""
    sample_values = {
        'email': 'testing@example.com',
        'password': 'test1234.',
        'name': 'Test User',
        'designation': 'Test Designation',
        'contact_number': '123467890',
        'employee_id': '1234',
    }
    sample_values.update(params)
    return get_user_model().objects.create_user(**sample_values)


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
        """Test that contact number greater than 10 characters \
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

    def test_create_token_success(self):
        """Test that user can get token after successful log in."""
        email = 'test@example.com'
        password = 'test1234.'
        create_user(email=email,
                    password=password)
        payload = {
            'email': email,
            'password': password
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)

    def test_create_token_fails_bad_credentials(self):
        """Test that token is not returned when \
        user provides bad credentials."""
        userDetails = {
            'email': 'test@example.com',
            'password': 'test1234.',
        }
        create_user(**userDetails)

        payload = {
            'email': userDetails['email'],
            'password': 'wrongPassword123'
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_create_token_fails_blank_password(self):
        """Test that token is not created with a blank password."""
        payload = {
            'email': 'test@example.com',
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', res.data)

    def test_get_user_details_without_token_raises_error(self):
        """Test that token is required for getting user details."""
        res = self.client.get(USER_DETAILS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('email', res.data)

    def test_upload_background_image_requires_token(self):
        """Test that token is requried for uploading \
        background image to a user."""

        payload = {'background_image': 'not_image'}
        res = self.client.post(BACKGROUND_UPLOAD_URL,
                               payload, format='multipart')

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('background_image', res.data)


class PrivateUserApiTests(TestCase):
    """Tests for authenticated api requests to the user api."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_get_user_details_success(self):
        """Test to get user details for the logged in user."""
        res = self.client.get(USER_DETAILS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
            'contact_number': self.user.contact_number,
            'designation': self.user.designation,
            'employee_id': self.user.employee_id,
        })

    def test_post_user_details_not_allowed(self):
        """Test that post request is not allowed \
        for the user details endpoint."""
        res = self.client.post(USER_DETAILS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_put_user_details_not_allowed(self):
        """Test that put request is not allowed \
        for the user details endpoint."""
        res = self.client.put(USER_DETAILS_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_partial_update_user_details(self):
        """Test that the user can update the details \
        partially"""
        payload = {
            'name': 'New Name',
            'password': 'New Password',
            'designation': 'New Designation',
            'employee_id': '5678',
        }

        res = self.client.patch(USER_DETAILS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()

        for attr, value in payload.items():
            if attr != 'password':
                self.assertEqual(getattr(self.user, attr), value)

        self.assertTrue(self.user.check_password(payload['password']))

    def test_email_update_not_allowed(self):
        """Test that the user cannot update the email."""
        payload = {
            'email': 'newemail@example.com',
        }

        self.client.patch(USER_DETAILS_URL, payload)

        self.user.refresh_from_db()

        self.assertNotEqual(self.user.email, payload['email'])

    @patch('core.models.uuid.uuid4')
    def test_background_image_file_name_uuid(self, mock_uuid):
        """Test generating image path."""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.background_image_file_path(None, 'example.jpg')

        self.assertEqual(file_path, f'uploads/user/backgroundImage/{uuid}.jpg')


class ImageUploadTests(TestCase):
    """Tests for the image upload API."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        """Clean up after every test to delete image."""
        self.user.background_image.delete()

    def test_upload_background_image(self):
        """Test uploading an background image to a user."""
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='jpeg')
            image_file.seek(0)
            payload = {'background_image': image_file}
            res = self.client.post(BACKGROUND_UPLOAD_URL,
                                   payload, format='multipart')

        self.user.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('background_image', res.data)
        self.assertTrue(os.path.exists(self.user.background_image.path))

    def test_upload_background_image_bad_request(self):
        """Test uploading an invalid image gives bad request."""
        payload = {'background_image': 'notanimage'}

        res = self.client.post(BACKGROUND_UPLOAD_URL,
                               payload, format='multipart')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
