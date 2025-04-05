"""
Views for the Support Ticket System.

This module contains views for handling user registration, login,
creating, updating, and deleting tickets, and adding notes to tickets.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import DeleteView, UpdateView
from django.views import View
from django.views.generic import CreateView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from .models import Ticket, Note
from .forms import UserRegisterForm, UserLoginForm, TicketForm, NoteForm



## Home Page
def home(request):
    """
    View for the home page of the support ticket system.
    Renders the landing page for the application.
    """
    return render(request, "supportticketssystem/home.html")

@never_cache
def register(request):
    """
    Handles user registration. If the request is a POST, it validates
    and saves the registration form. On success, the user is redirected 
    to the login page.
    """
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! Please log in.")
            return redirect("login")  # Redirect to login page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegisterForm()
    return render(request, "supportticketssystem/register.html", {"form": form})

@never_cache
def user_login(request):
    """
    View for handling user login.
    Validates the user's credentials and logs them in if successful.
    Redirects to the ticket list after successful login.
    If login fails, displays an error message.
    """
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("ticket-list")  # Redirect to ticket list after login
            else:
                messages.error(request, "Invalid username or password.")
                return render(
                    request,
                    "supportticketssystem/register.html",
                    {"form": form}
                )
        else:
            return render(
                request,
                "supportticketssystem/login.html",
                {"form": form}
            )
    else:
        form = UserLoginForm()
    return render(request, "supportticketssystem/login.html", {"form": form})

# List all tickets (Only for logged-in users)
@method_decorator([login_required, never_cache], name="dispatch")
class TicketListView(View):
    """
    View for listing the user's tickets. Only accessible to authenticated users.
    Displays all tickets related to the logged-in user.
    """
    def get(self, request):
        """Handles GET requests to display the list of tickets for the logged-in user."""
        tickets = Ticket.objects.filter(user=request.user)  # Show only tickets of logged-in user
        return render(request, "supportticketssystem/ticket_list.html", {"tickets": tickets})

# Create New Ticket
@method_decorator([login_required, never_cache], name="dispatch")
class TicketCreateView(View):
    """
    View for creating a new ticket. Only accessible to authenticated users.
    Provides a form to submit a new support ticket and saves it to the database.
    """
    def get(self, request):
        """Handles GET requests to display a form for creating a new ticket."""
        form = TicketForm()
        return render(request, "supportticketssystem/ticket_form.html", {"form": form})

    def post(self, request):
        """Handles POST requests to save a new ticket and associate it with the logged-in user."""
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user  # Assign ticket to logged-in user
            ticket.save()
            return redirect("ticket-list")
        return render(request, "supportticketssystem/ticket_form.html", {"form": form})

@method_decorator([login_required, never_cache], name="dispatch")
class NoteCreateView(CreateView):
    """
    View for creating a new note for a ticket. Only accessible to authenticated users.
    Allows the user to add notes to a specific ticket and associate the note with the ticket.
    """
    model = Note
    template_name = "note_form.html"  # Make sure this template exists
    fields = ['content']  # Add any other fields you need

    def form_valid(self, form):
        ticket = get_object_or_404(Ticket, id=self.kwargs['ticket_id'])
        form.instance.ticket = ticket
        return super().form_valid(form)

@method_decorator([login_required, never_cache], name="dispatch")
class TicketDetailView(View):
    """
    View for displaying the details of a specific ticket.
    Allows users to view a ticket's information and add notes to the ticket.
    Only accessible to authenticated users.
    """
    model = Ticket
    template_name = 'supportticketssystem/ticket_detail.html'

    def get(self, request, **kwargs):
        """Handles GET requests to display the details of a specific ticket and its notes."""
        ticket = get_object_or_404(Ticket, pk=kwargs['pk'])
        notes = Note.objects.filter(ticket=ticket).order_by('-created_at')
        form = NoteForm()

        return render(request, self.template_name, {
            'ticket': ticket,
            'note_form': form,
            'notes': notes,  # Pass the notes to the template
        })

    def post(self, request, **kwargs):
        """Handles POST requests to add a note to a specific ticket and handle AJAX responses."""
        ticket = get_object_or_404(Ticket, pk=kwargs['pk'])
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.ticket = ticket  # Associate the note with the ticket
            note.user = request.user  # Set the user field to the currently logged-in user
            note.save()

            # Check if it's an AJAX request using the header 'X-Requested-With'
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'message': 'Note added successfully',
                    'new_note_content': note.content
                })
            else:
                return redirect('ticket-detail', pk=ticket.pk)
        return render(
            request,
            self.template_name,
            {'ticket': ticket, 'note_form': form}
        )

class TicketDeleteView(DeleteView):
    """
    View for deleting a ticket. Only accessible to authenticated users.
    Allows the user to delete a support ticket from the system.
    """
    model = Ticket
    template_name = 'supportticketssystem/ticket_confirm_delete.html'
    success_url = reverse_lazy('ticket-list')

class TicketUpdateView(UpdateView):
    """
    View for updating an existing ticket. Only accessible to authenticated users.
    Allows the user to update the details of a support ticket.
    """
    model = Ticket
    form_class = TicketForm  # Use the same form as create, but pre-filled with data
    template_name = "supportticketssystem/ticket_update_form.html"  # New update template
    success_url = reverse_lazy("ticket-list")  # Redirect after successful update
