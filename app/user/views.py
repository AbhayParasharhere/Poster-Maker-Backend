"""
Views for the user API.
"""

from django.utils.translation import gettext as _

from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework import (
    viewsets,
    authentication,
    permissions,
    generics,
    status,
)

from rest_framework.settings import api_settings

from rest_framework.response import Response

from rest_framework.decorators import action

from user.serializers import (
    AuthTokenSerializer,
    UserSerializer,
    UserTextDetailSerializer,
    UserImageSerializer,
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


class UserImageViewSet(viewsets.ModelViewSet):
    """Views for image upload to the user model."""
    http_method_names = ['post']
    serializer_class = UserImageSerializer

    authentication_classes = [authentication.TokenAuthentication]
    permissions_classes = [permissions.IsAuthenticated]

    @action(methods=['POST'], detail=True, url_path='upload-background-image')
    def upload_background_image(self, request, pk=None):
        """Upload a background image to the user."""
        user = self.request.user
        serializer = self.get_serializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            msg = _("Provided background image could not be validated.")
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        return self.request.user
