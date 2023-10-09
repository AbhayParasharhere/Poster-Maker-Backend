"""
URL configurations for the user API.
"""

from django.urls import path
from user.views import (
    CreateUserApiView,
    CreateAuthTokenView,
    GetUpdateUserDetailsView,
    UserImageViewSet,
)


app_name = 'user'

urlpatterns = [
    path('sign-up/', CreateUserApiView.as_view(), name='sign-up'),
    path('token/', CreateAuthTokenView.as_view(), name='token'),
    path('me/', GetUpdateUserDetailsView.as_view(), name='me'),
    path('upload-background-image/',
         UserImageViewSet.as_view({'post': 'upload_background_image'}),
         name='user-background-upload-image'),
]
