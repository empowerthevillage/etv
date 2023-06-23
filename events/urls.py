from django.urls import path
from .views import *

urlpatterns = [
    path('', event_home, name='home'),
    path('art-gallery/', full_gallery_home, name="full-gallery-home"),
    path('art-email/', art_email_view),
    path('gallery-get-next/', gallery_get_next, name="gallery-next"),
    path('gallery-search-available/', gallery_search_available, name="gallery-search-available"),
    path('gallery-search/', gallery_search, name="gallery-search"),
    path('art-presale/', gallery_home, name="gallery-home"),
    path('loa-presale-cart/', gallery_cart_home, name="presale-cart-home"),
    path('loa-gallery-cart/', full_gallery_cart_home, name="gallery-cart-home"),
    path('email-view/', email_view, name="email-view"),
    path('ticket-search/', ticket_search),
    path('ticket-update-cart/', ticket_cart_update, name="ticket-update-cart"),
    path('ticket-donation-update-cart/', ticket_cart_donation_update, name="ticket-update-donation-cart"),
    path('ticket-donation-remove/', ticket_cart_donation_remove, name="ticket-donation-remove"),
    path('ticket-ad-update-cart/', ticket_cart_ad_update, name="ticket-update-ad-cart"),
    path('checkin/', checkin, name="checkin"),
    path('check-in-success/', checkin_success),
    path('check-in-history/', view_checkins),
    path('new-check-in/', new_checkin),
    path('rules-agreement/', pitch_rules_agreement),
    path('village-ventures/', pitch_registration),
    path('ticket/<ticket_id>/', ticket, name="ticket-detail"),
    path('<slug>/', event_detail, name='detail'),
    path('<slug>/buy-tickets/', event_ticket_checkout, name='ticket-checkout'),
    path('<slug>/sponsor/', event_sponsor_checkout, name='sponsor-checkout'),
    ]
