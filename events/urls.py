from django.urls import path
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', event_home, name='home'),
    path('ticket-update-cart/', ticket_cart_update, name="ticket-update-cart"),
    path('ticket-donation-update-cart/', ticket_cart_donation_update, name="ticket-update-donation-cart"),
    path('ticket/<ticket_id>/', ticket, name="ticket-detail"),
    path('<slug>/', event_detail, name='detail'),
    path('<slug>/buy-tickets/', event_ticket_checkout, name='ticket-checkout'),
    path('<slug>/sponsor/', event_sponsor_checkout, name='sponsor-checkout'),
    ]
