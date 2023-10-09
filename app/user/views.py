"""
Views for the user API.
"""

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import (
    authentication,
    permissions,
    generics,
)

from rest_framework.settings import api_settings

from user.serializers import (
    AuthTokenSerializer,
    UserSerializer,
    UserTextDetailSerializer,
)


class CreateUserApiView(generics.CreateAPIView):
    """View for creating new users."""
    serializer_class = UserSerializer


class CreateAuthTokenView(ObtainAuthToken):
    """View for creating an auth token token."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class GetUpdateUserDetailsView(generics.RetrieveUpdateAPIView):
    """View for getting and updating logged in user details."""
    http_method_names = ['get', 'patch']

    serializer_class = UserTextDetailSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retreive and return the authenticated user."""
        return self.request.user
