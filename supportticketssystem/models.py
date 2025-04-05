"""
This module contains the models for the Support Ticket System.

- CustomUser: Extends Django's AbstractUser to include a unique email field and a staff flag.
- Ticket: Represents a support ticket with attributes like ticket number, title, description,
- status, and associated user.
- Note: Represents a note attached to a specific ticket, created by a user.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models

# CustomUser model extends AbstractUser to include an email field.
class CustomUser(AbstractUser):
    """
    Custom user model to extend the built-in Django user model.
    Adds a unique email field and a staff status.
    """
    email = models.EmailField(unique=True)  # Ensure email is unique
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

# Ticket model represents support tickets created by users.
class Ticket(models.Model):
    """
    Ticket model for managing support tickets. Each ticket has a title, description, status,
    and a unique ticket number generated automatically.
    """
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]

    ticket_number = models.CharField(max_length=20, unique=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """Generate unique ticket number if not set."""
        if not self.ticket_number:
            last_ticket = Ticket.objects.order_by('-id').first()
            if last_ticket and last_ticket.ticket_number.startswith("TICKET-"):
                last_number = int(last_ticket.ticket_number.split("-")[1])
                self.ticket_number = f"TICKET-{last_number + 1:04d}"
            else:
                self.ticket_number = "TICKET-0001"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.ticket_number} - {self.title} ({self.get_status_display()})"

# Note model stores notes related to specific tickets.
class Note(models.Model):
    """
    Note model for storing notes on specific tickets. Each note is associated with a ticket
    and created by a user.
    """
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="notes")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note on {self.ticket.ticket_number} by {self.user.username}"
