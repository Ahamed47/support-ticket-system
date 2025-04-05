"""
URL routing for the support ticket system. This file maps views to URL paths for 
the application, including user authentication, ticket management, and note creation.
"""

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache

from .views import (
    home,
    register,
    user_login,
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    NoteCreateView,
    TicketUpdateView,
    TicketDeleteView
)

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('tickets/', TicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('tickets/<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('tickets/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('tickets/<int:pk>/', TicketDetailView.as_view(), name='ticket-detail'),
    path('tickets/<int:ticket_id>/add-note/', NoteCreateView.as_view(), name='note-create'),
    path('logout/', never_cache(auth_views.LogoutView.as_view(next_page='login')), name='logout'),
]
