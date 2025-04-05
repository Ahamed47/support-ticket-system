"""
URL configuration for the supportdesk project.

This file defines the URL patterns for the supportdesk application. 
It includes the paths for the Django admin interface and the app-specific URLs.
"""

from django.contrib import admin
from django.urls import path, include  # Make sure 'include' is imported

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('supportticketssystem.urls')),  # Include your app's URLs here
]
