"""
Tests for the models.
"""

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.core.exceptions import ValidationError


class ModelTests(TestCase):
    """Tests for the django models."""

    def test_create_user(self):
        """Test creating a user is successful."""
        name = 'Test User'
        email = 'test@example.com'
        password = 'Test123.'
        contact_number = '912912911'
        user = get_user_model().objects.create_user(
            name=name,
            email=email,
            password=password,
            contact_number=contact_number
        )
        self.assertEqual(user.email, email)
        self.assertEqual(user.name, name)
        self.assertEqual(user.contact_number, contact_number)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test that email is normalized when creating a user."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='test123.',
                name='Test User',
                contact_number='123456789'
            )
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating new user without email raise error."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                '',
                password='test123.',
                name='Test User',
                contact_number='123456789'
            )

    def test_password_short_raises_error(self):
        with self.assertRaises(ValidationError):
            get_user_model().objects.create_user(
                email='test@example.com',
                password='1234',
                name='Test User',
                contact_number='123456789'
            )
