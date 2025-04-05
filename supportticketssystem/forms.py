"""
This module contains the form classes for the Support Ticket System.

- TicketForm: A form for creating and updating tickets, with validation for title
- and description length.
- NoteForm: A form for creating notes related to tickets.
- UserRegisterForm: A form for user registration using Django's UserCreationForm.
- UserLoginForm: A form for user login with username and password fields.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Ticket, Note


User = get_user_model()


class TicketForm(forms.ModelForm):
    """
    A form for creating and updating tickets. It validates the title and description fields.
    """
    class Meta:
        """
        Meta class for TicketForm. Defines the model associated with the form
        and specifies the fields to be included in the form.
        """
        model = Ticket
        fields = ['title', 'description', 'status']

    def clean_title(self):
        """
        Validates the title length. The title must be less than 60 characters.
        """
        title = self.cleaned_data.get('title')
        if len(title) > 60:
            raise forms.ValidationError('Title must be less than 60 characters.')
        return title

    def clean_description(self):
        """
        Validates the description length. The description must be less than 300 characters.
        """
        description = self.cleaned_data.get('description')
        if len(description) > 300:
            raise forms.ValidationError('Description must be less than 300 characters.')
        return description

class NoteForm(forms.ModelForm):
    """
    A form for creating notes related to a specific ticket. 
    It includes a single field for the content of the note.
    """
    class Meta:
        """
        Meta class for NoteForm. Defines the model associated with the form
        and specifies the 'content' field to be included in the form.
        """
        model = Note
        # fields = ["text"]
        fields = ['content']  # Ensure this matches your model definitio

class UserRegisterForm(UserCreationForm):
    """
    A form for user registration. Inherits from Django's UserCreationForm and includes
    an additional email field.
    """
    email = forms.EmailField()

    class Meta:
        """
        Meta class for UserRegisterForm. Defines the model associated with the form
        and specifies the fields ('username', 'email', 'password1', 'password2') to
        be included in the form.
        """
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(forms.Form):
    """
    A form for user login, with fields for username and password.
    """
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
