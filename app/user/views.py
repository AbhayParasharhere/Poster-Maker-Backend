"""
Views for the user API.
"""

from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    AuthTokenSerializer,
    UserSerializer,
)


class CreateUserApiView(generics.CreateAPIView):
    """View for creating new users."""
    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """View for creating an auth token token."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
