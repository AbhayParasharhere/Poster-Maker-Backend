"""
Model definitions for the application.
"""
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    """Manager for the custom user model."""

    def create_user(
            self, email, name,
            password, contact_number=None,
            **extra_fields):
        """Create a user object and return the newly created user."""
        if not email:
            raise ValueError("Email is required for creating users.")
        if not password or len(password) < 8:
            raise ValidationError(
                "Password length must be atleast 8 characters.")
        user = self.model(
            name=name,
            email=self.normalize_email(email),
            contact_number=contact_number,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # def create_super_user(self)


class User(AbstractBaseUser, PermissionsMixin):
    """Custom model for the user."""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    contact_number = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    designation = models.CharField(max_length=255, null=True, blank=True)
    employee_id = models.CharField(max_length=12, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
