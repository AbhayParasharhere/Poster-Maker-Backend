"""
URL configurations for the user API.
"""

from django.urls import path
from user.views import CreateUserApiView

app_name = 'user'

urlpatterns = [
    path('sign-up/', CreateUserApiView.as_view(), name='sign-up'),
]
