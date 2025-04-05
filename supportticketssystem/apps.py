"""
Django app configuration for the Support Ticket System.

This module defines the configuration for the 'supportticketssystem' app, 
including the default auto field type and app name.
"""

from django.apps import AppConfig


class SupportticketssystemConfig(AppConfig):
    """
    Configuration for the Support Ticket System app.

    This class specifies the default auto field type and the name of the app, 
    which helps Django know how to configure the app within the project.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'supportticketssystem'
