from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', event_home, name='home'),
    path('power-swing-classic/', golf, name='golf'),
    path('love-of-art-fundraiser/', art, name='art'),
    path('ticket-update-cart/', ticket_cart_update, name="ticket-update-cart"),
    path('ticket/<ticket_id>/', ticket, name="ticket-detail"),
    path('power-swing-classic/buy-tickets/', golf_checkout, name='golf-checkout'),
    path('power-swing-classic/sponsor/', golf_sponsor_checkout, name='golf-sponsor-checkout'),
    path('love-of-art-fundraiser/buy-tickets/', art_checkout, name='art-checkout'),
    path('love-of-art-fundraiser/sponsor/', art_sponsor_checkout, name='art-sponsor-checkout'),
]
