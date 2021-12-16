from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', event_home, name='home'),
    path('power-swing-classic/', golf, name='golf'),
    path('love-of-art-fundraiser/', art, name='art'),
    path('ticket-update-cart/', ticket_cart_update, name="ticket-update-cart"),
    path('ticket/<ticket_id>/', ticket, name="ticket-detail"),
]
