"""
Admin page settings for the application.
"""

from django.contrib import admin
from core import models

admin.site.register(models.User)
