"""
URL configurations for the user API.
"""

from django.urls import path
from user.views import (
    CreateUserApiView,
    CreateAuthTokenView,
    GetUpdateUserDetailsView,
)


app_name = 'user'

urlpatterns = [
    path('sign-up/', CreateUserApiView.as_view(), name='sign-up'),
    path('token/', CreateAuthTokenView.as_view(), name='token'),
    path('me/', GetUpdateUserDetailsView.as_view(), name='me'),
]
