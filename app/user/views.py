"""
Views for the user API.
"""

from rest_framework import generics
from user.serializers import UserSerializer


class CreateUserApiView(generics.CreateAPIView):
    """View for creating new users."""
    serializer_class = UserSerializer
