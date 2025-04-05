"""
Admin configuration for the Support Ticket System.

This module registers the Ticket, Note, and CustomUser models with the Django admin interface 
to allow for easy management through the admin panel.
"""

from django.contrib import admin
from .models import Ticket, Note, CustomUser

admin.site.register(Ticket)
admin.site.register(Note)
admin.site.register(CustomUser)
