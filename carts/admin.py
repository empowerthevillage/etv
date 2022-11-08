from django.contrib import admin
from .models import *
from accounts.admin import admin_site

admin_site.register(Cart)
admin_site.register(FullGalleryCart)
admin_site.register(cartItem)
admin_site.register(TicketCart)
admin_site.register(ticketItem)
admin_site.register(ticketDonation)
admin_site.register(ticketAd)